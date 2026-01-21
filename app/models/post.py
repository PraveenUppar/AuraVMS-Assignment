from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PostStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Post:
    id: int
    title: str
    content: str
    author: str
    status: PostStatus = PostStatus.PENDING
    image: Optional[str] = None