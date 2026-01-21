from app.models.post import Post
from app.storage.json_store import JsonPostStore

def test_json_store_add_and_load(tmp_path):
    path = tmp_path / "posts.json"
    store = JsonPostStore(path)

    post = Post(
        id=1,
        title="Test",
        content="Persistence works",
        author="writer"
    )

    store.add(post)

    posts = store.load_all()

    assert len(posts) == 1
    assert posts[0].title == "Test"
    assert posts[0].author == "writer"
