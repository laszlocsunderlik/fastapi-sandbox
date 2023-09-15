from typing import List

import pytest

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

    sorted_posts = sorted(posts_list, key=lambda post: post.Post.id)
    assert sorted_posts[0].Post.id == test_posts[0].id


def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get(f"/posts/{test_posts}")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get("/posts/999999")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    print(post)
    print("===============___________---------___________===============")
    assert post.Post.id == test_posts[0].id
    print(post.Post.content)
    print("===============___________---------___________===============")
    print(test_posts[0].content)
    assert post.Post.content == test_posts[0].content
    print("===============___________---------___________===============")
    print(post.Post.created_at)
    print("===============___________---------___________===============")
    print(test_posts[0].created_at)
    assert post.Post.created_at == test_posts[0].created_at


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "content for awesome new title", True),
    ("Movies", "My favourite movies are the following...", True),
    ("Pizza", "I love pepperoni", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.content == content
    assert created_post.title == title
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "title", "content": "content"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.content == "content"
    assert created_post.title == "title"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title": "title", "content": "content"})
    assert res.status_code == 401


def test_uanthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    #print(f"TESTPOST_IDDDDDD: {test_posts[0].id}")
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

    # res = authorized_client.get(f"/posts/{test_posts}")
    # assert len(res.json()) == 2


def test_delete_post_non_exists(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/999999999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
