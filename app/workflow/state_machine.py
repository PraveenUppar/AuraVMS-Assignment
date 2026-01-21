from app.models.post import Post, PostStatus


class InvalidStateTransition(Exception):
    pass

def approve_post(post: Post) -> None:
    if post.status != PostStatus.PENDING:
        raise InvalidStateTransition(
            f"Cannot approve post in '{post.status}' state"
        )

    post.status = PostStatus.APPROVED

def reject_post(post: Post) -> None:
    if post.status != PostStatus.PENDING:
        raise InvalidStateTransition(
            f"Cannot reject post in '{post.status}' state"
        )

    post.status = PostStatus.REJECTED
