import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


# passing the client fixture as an unauthorized client
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/100")

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostLikeResponse(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("cool view", "a very nice place to visit!", True),
    ("paris", "so romantic city", False),
    ("i like pizza", "i love pizza with cheese!!", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    assert res.status_code == 201


def test_unauthorized_user_create_posts(client, test_posts, test_user):
    res = client.get("/posts/", json={"title": "random title",
                     "content": "random content", "published": True})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts, test_user):
    res = client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    # TODO: fetch all post and check if it's length is the length-1
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_posts, test_user):
    res = authorized_client.delete(
        f"/posts/897979")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")

    assert res.status_code == 403


def test_update_post(authorized_client, test_posts, test_user):
    data = {"title": "new title", "content": "new content", "published": True}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert res.status_code == 200


def test_update_other_user_post(authorized_client, test_posts, test_user):
    data = {"title": "new title", "content": "new content", "published": True}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts, test_user):
    data = {"title": "new title", "content": "new content", "published": True}
    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_posts, test_user):
    data = {"title": "new title", "content": "new content", "published": True}
    res = authorized_client.put(f"/posts/88888888888", json=data)

    assert res.status_code == 404
