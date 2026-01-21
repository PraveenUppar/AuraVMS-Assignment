import json
from pathlib import Path
from typing import List
from app.models.post import Post, PostStatus

class JsonPostStore:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump({"posts": []}, f)

    # Serialization helper
    def _post_to_dict(self, post: Post) -> dict:
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "image": post.image,
            "status": post.status.value,
            "author": post.author,
        }

    # Deserialization helper
    def _dict_to_post(self, data: dict) -> Post:
        return Post(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            image=data.get("image"),
            status=PostStatus(data["status"]),
            author=data["author"],
        )
    
    def load_all(self) -> List[Post]:
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [self._dict_to_post(p) for p in data.get("posts", [])]
    
    def save_all(self, posts: List[Post]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(
                {"posts": [self._post_to_dict(p) for p in posts]},
                f,
                indent=2
            )

    def _next_id(self, posts: List[Post]) -> int:
        if not posts:
            return 1
        return max(p.id for p in posts) + 1

    def add(self, post: Post) -> Post:
        posts = self.load_all()
        post.id = self._next_id(posts)
        posts.append(post)
        self.save_all(posts)
        return post
    
    def get_by_id(self, post_id: int) -> Post | None:
        posts = self.load_all()
        for post in posts:
            if post.id == post_id:
                return post
        return None
    
    def update(self, updated_post: Post) -> None:
        posts = self.load_all()
        for i, post in enumerate(posts):
            if post.id == updated_post.id:
                posts[i] = updated_post
                self.save_all(posts)
                return
        raise ValueError("Post not found")
    
    def list_by_status(self, status: PostStatus) -> List[Post]:
        posts = self.load_all()
        return [p for p in posts if p.status == status]