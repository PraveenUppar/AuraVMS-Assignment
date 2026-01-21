import pytest
from app.models.post import Post, PostStatus
from app.workflow.state_machine import approve_post, reject_post, InvalidStateTransition

def test_pending_to_approved():
    post = Post(
        id=1,
        title="Test",
        content="Content",
        author="writer"
    )
    approve_post(post)
    assert post.status == PostStatus.APPROVED

def test_pending_to_rejected():
    post = Post(
        id=1,
        title="Test",
        content="Content",
        author="writer"
    )
    reject_post(post)
    assert post.status == PostStatus.REJECTED

def test_cannot_reject_approved_post():
    post = Post(
        id=1,
        title="Test",
        content="Content",
        author="writer",
        status=PostStatus.APPROVED
    )
    with pytest.raises(InvalidStateTransition):
        reject_post(post)

def test_cannot_approve_rejected_post():
    post = Post(
        id=1,
        title="Test",
        content="Content",
        author="writer",
        status=PostStatus.REJECTED
    )
    with pytest.raises(InvalidStateTransition):
        approve_post(post)