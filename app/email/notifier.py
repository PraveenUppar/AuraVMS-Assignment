from app.models.post import Post

MANAGER_EMAIL = "manager@example.com"

def send_review_notification(post: Post) -> None:
    snippet = post.content[:100].replace("\n", " ")

    approve_url = f"http://localhost:8000/posts/{post.id}/review"
    reject_url = f"http://localhost:8000/posts/{post.id}/review"

    print("\n=== EMAIL NOTIFICATION ===")
    print(f"To: {MANAGER_EMAIL}")
    print(f"Subject: New post pending review")
    print(f"Title: {post.title}")
    print(f"Snippet: {snippet}")
    print(f"Approve: {approve_url} (action=approve)")
    print(f"Reject:  {reject_url} (action=reject)")
    print("==========================\n")
