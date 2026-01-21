from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from pathlib import Path

from app.storage.json_store import JsonPostStore
from app.parser.txt_md import parse_txt_md
from app.models.post import Post, PostStatus
from app.api.schemas import CreatePostRequest, ReviewActionRequest
from app.workflow.state_machine import approve_post, reject_post
from app.email.notifier import send_review_notification
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(title="Blog Review System")

store = JsonPostStore(Path("data/posts.json"))

from fastapi import Depends
from app.auth.simple_auth import get_current_user


# Writer submits a post
@app.post("/posts")
def create_post(
    author: str = Form(...),
    file: UploadFile = File(...),
    # user=Depends(get_current_user)
):
    # Only writers can submit
    # if user["role"] != "writer":
    #     raise HTTPException(status_code=403, detail="Only writers can create posts.")

    # Validate file type
    if not file.filename.endswith((".txt", ".md")):
        raise HTTPException(status_code=400, detail="Only .txt or .md files are allowed")

    try:
        # Read file content
        raw = file.file.read()
        text = raw.decode("utf-8")

        # Parse the document
        parsed = parse_txt_md(text)

        # Create Post object
        post = Post(
            id=0,
            title=parsed.title,
            content=parsed.content,
            image=parsed.image,
            author=author
        )

        # Store and send notification
        stored = store.add(post)
        send_review_notification(stored)

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "id": stored.id,
        "status": stored.status.value,
        "message": "Post submitted for review"
    }

# Manager reviews a post
@app.post("/posts/{post_id}/review")
def review_post_api(post_id: int, req: ReviewActionRequest,
                    # user=Depends(get_current_user)
                    ):
    # if user["role"] != "manager":
    #     raise HTTPException(status_code=403, detail="Managers only")
    post = store.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        if req.action == "approve":
            approve_post(post)
        elif req.action == "reject":
            reject_post(post)
        else:
            raise ValueError("Invalid action")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    store.update(post)

    return {
        "id": post.id,
        "status": post.status.value,
    }

# View approved posts (public)
@app.get("/posts")
def list_approved_posts():
    posts = store.list_by_status(PostStatus.APPROVED)
    return [
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "image": p.image,
            "author": p.author,
        }
        for p in posts
    ]

# UI routes
@app.get("/")
def home(request: Request):
    posts = store.list_by_status("approved")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "posts": posts}
    )

@app.get("/submit")
def submit_form(request: Request):
    return templates.TemplateResponse("submit.html", {"request": request})

@app.post("/submit")
def submit_post(
    request: Request,
    author: str = Form(...),
    file: UploadFile = File(...)
):
    if not file.filename.endswith((".txt", ".md")):
        return templates.TemplateResponse(
            "submit.html",
            {
                "request": request,
                "message": "Only .txt or .md files are allowed"
            }
        )

    try:
        raw = file.file.read()
        text = raw.decode("utf-8")

        parsed = parse_txt_md(text)

        post = Post(
            id=0,
            title=parsed.title,
            content=parsed.content,
            image=parsed.image,
            author=author
        )

        stored = store.add(post)
        send_review_notification(stored)

        message = "Post submitted for review. Awaiting manager approval."

    except UnicodeDecodeError:
        message = "File must be UTF-8 encoded."
    except Exception as e:
        message = f"Error: {e}"

    return templates.TemplateResponse(
        "submit.html",
        {
            "request": request,
            "message": message
        }
    )



@app.get("/review")
def review_page(
    request: Request,
    user=Depends(get_current_user)
):
    if user["role"] != "manager":
        raise HTTPException(status_code=403)

    posts = store.list_by_status(PostStatus.PENDING)
    return templates.TemplateResponse(
        "review.html",
        {"request": request, "posts": posts}
    )


from fastapi.responses import RedirectResponse

@app.post("/review/{post_id}")
def review_post_ui(
    post_id: int,
    action: str = Form(...),
    user=Depends(get_current_user)
):
    if user["role"] != "manager":
        raise HTTPException(status_code=403)
    post = store.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404)

    if action == "approve":
        approve_post(post)
    elif action == "reject":
        reject_post(post)
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    store.update(post)
    return RedirectResponse("/review", status_code=303)
