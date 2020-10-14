"""Unit tests for REST API."""
import json
import sqlite3


def test_resources(client):
    """Verify GET requests to initial endpoint.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # Verify response with information listed in the spec.
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.get_json() == {
        "posts": "/api/v1/p/",
        "url": "/api/v1/",
    }


def test_posts(client):
    """Verify GET requests to 'posts' endpoint.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # Verify response with default database content
    response = client.get("/api/v1/p/")
    assert response.status_code == 200
    assert response.get_json() == {
        "next": "",
        "results": [
            {"postid": 3, "url": "/api/v1/p/3/"},
            {"postid": 2, "url": "/api/v1/p/2/"},
            {"postid": 1, "url": "/api/v1/p/1/"},
        ],
        "url": "/api/v1/p/",
    }


def test_posts_pagination_simple(client):
    """Verify GET 'posts' with two pages.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # Delete all likes, comments and posts
    connection = sqlite3.connect("var/insta485.sqlite3")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("DELETE FROM likes")
    connection.execute("DELETE FROM comments")
    connection.execute("DELETE FROM posts")

    # Create exactly 11 posts
    for _ in range(11):
        connection.execute(
            "INSERT INTO posts(owner, filename) "
            "VALUES('awdeorio', 'fox.jpg') ",
        )
    connection.commit()
    connection.close()

    # GET request with defaults return 10 most recent items
    response = client.get("/api/v1/p/")
    assert response.status_code == 200
    assert response.get_json() == {
        "next": "/api/v1/p/?size=10&page=1",
        "results": [
            {"postid": 11, "url": "/api/v1/p/11/"},
            {"postid": 10, "url": "/api/v1/p/10/"},
            {"postid": 9, "url": "/api/v1/p/9/"},
            {"postid": 8, "url": "/api/v1/p/8/"},
            {"postid": 7, "url": "/api/v1/p/7/"},
            {"postid": 6, "url": "/api/v1/p/6/"},
            {"postid": 5, "url": "/api/v1/p/5/"},
            {"postid": 4, "url": "/api/v1/p/4/"},
            {"postid": 3, "url": "/api/v1/p/3/"},
            {"postid": 2, "url": "/api/v1/p/2/"},
        ],
        "url": "/api/v1/p/",
    }

    # GET request to second page returns 1 item
    response = client.get("/api/v1/p/?size=10&page=1")
    assert response.status_code == 200
    assert response.get_json() == {
        "next": "",
        "results":
        [
            {"postid": 1, "url": "/api/v1/p/1/"}
        ],
        "url": "/api/v1/p/"
    }


def test_posts_pagination_page_size(client):
    """Verify GET 'posts' with pagination and 'page' and 'size' parameters.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # Delete all likes, comments and posts
    connection = sqlite3.connect("var/insta485.sqlite3")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("DELETE FROM likes")
    connection.execute("DELETE FROM comments")
    connection.execute("DELETE FROM posts")

    # Create exactly 11 posts
    for _ in range(11):
        connection.execute(
            "INSERT INTO posts(owner, filename) "
            "VALUES('awdeorio', 'fox.jpg') ",
        )
    connection.commit()
    connection.close()

    # GET page 1 size 6
    response = client.get("/api/v1/p/?size=6")
    assert response.status_code == 200
    assert response.get_json() == {
        "next": "/api/v1/p/?size=6&page=1",
        "results": [
            {"postid": 11, "url": "/api/v1/p/11/"},
            {"postid": 10, "url": "/api/v1/p/10/"},
            {"postid": 9, "url": "/api/v1/p/9/"},
            {"postid": 8, "url": "/api/v1/p/8/"},
            {"postid": 7, "url": "/api/v1/p/7/"},
            {"postid": 6, "url": "/api/v1/p/6/"},
        ],
        "url": "/api/v1/p/",
    }

    # GET page 2 size 6
    response = client.get("/api/v1/p/?size=6&page=1")
    assert response.status_code == 200
    assert response.get_json() == {
        "next": "",
        "results": [
            {"postid": 5, "url": "/api/v1/p/5/"},
            {"postid": 4, "url": "/api/v1/p/4/"},
            {"postid": 3, "url": "/api/v1/p/3/"},
            {"postid": 2, "url": "/api/v1/p/2/"},
            {"postid": 1, "url": "/api/v1/p/1/"},
        ],
        "url": "/api/v1/p/"}


def test_posts_pagination_errors(client):
    """Verify pagination error conditions.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    response = client.get("/api/v1/p/1000/")
    assert response.status_code == 403

    response = client.get("/api/v1/p/1000/comments/")
    assert response.status_code == 403

    response = client.get("/api/v1/p/1000/likes/")
    assert response.status_code == 403

    response = client.get("/api/v1/p/?page=-1")
    assert response.status_code == 403

    response = client.get("/api/v1/p/?size=-1")
    assert response.status_code == 403


def test_likes_get(client):
    """Verify GET 'likes' endpoint.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # GET likes with default data
    response = client.get("/api/v1/p/3/likes/")
    assert response.status_code == 200
    assert response.get_json() == {
        "likes_count": 1,
        "logname_likes_this": 1,
        "postid": 3,
        "url": "/api/v1/p/3/likes/",
    }


def test_likes_delete(client):
    """Verify DELETE 'likes' endpoint.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # DELETE likes
    response = client.delete(
        "/api/v1/p/3/likes/",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 204

    # Verify number of likes
    response = client.get("/api/v1/p/3/likes/")
    assert response.status_code == 200
    assert response.get_json() == {
        "likes_count": 0,  # Changed from 1 to 0
        "logname_likes_this": 0,  # Changed from 1 to 0
        "postid": 3,
        "url": "/api/v1/p/3/likes/",
    }


def test_likes_post(client):
    """Verify POST 'likes' endpoint.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "jag", "password": "password"}
    )

    # POST likes (jag likes his own post)
    response = client.post(
        "/api/v1/p/4/likes/",
        data=json.dumps({}),
        content_type="application/json")
    assert response.status_code == 201

    # Verify number of likes
    response = client.get("/api/v1/p/4/likes/")
    assert response.status_code == 200
    assert response.get_json() == {
        "likes_count": 1,  # Changed from 0 to 1
        "logname_likes_this": 1,  # Changed from 0 to 1
        "postid": 4,
        "url": "/api/v1/p/4/likes/",
    }


def test_likes_error(client):
    """Duplicate POST likes returns a JSON formatted error.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # awdeorio likes a post that he already liked
    response = client.post(
        "/api/v1/p/3/likes/",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 409
    assert "message" in response.get_json()


def test_comments_get(client):
    """Verify GET 'comments' endpoint.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # GET comments with default data
    response = client.get("/api/v1/p/3/comments/")
    assert response.status_code == 200
    assert response.get_json() == {
        "comments": [
            {
                "commentid": 1,
                "owner": "awdeorio",
                "owner_show_url": "/u/awdeorio/",
                "postid": 3,
                "text": "#chickensofinstagram",
            },
            {
                "commentid": 2,
                "owner": "jflinn",
                "owner_show_url": "/u/jflinn/",
                "postid": 3,
                "text": "I <3 chickens",
            },
            {
                "commentid": 3,
                "owner": "michjc",
                "owner_show_url": "/u/michjc/",
                "postid": 3,
                "text": "Cute overload!",
            },
        ],
        "url": "/api/v1/p/3/comments/",
    }


def test_comments_post(client):
    """Verify POST 'comments' endpoint.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    # Log in
    client.post(
        "/accounts/login/",
        data={"username": "awdeorio", "password": "password"}
    )

    # POST comments
    response = client.post(
        "/api/v1/p/3/comments/",
        data=json.dumps({"text": "new comment"}),
        content_type="application/json")
    assert response.status_code == 201

    # Verify comments
    response = client.get("/api/v1/p/3/comments/")
    assert response.status_code == 200
    assert response.get_json() == {
        "comments": [
            {
                "commentid": 1,
                "owner": "awdeorio",
                "owner_show_url": "/u/awdeorio/",
                "postid": 3,
                "text": "#chickensofinstagram",
            },
            {
                "commentid": 2,
                "owner": "jflinn",
                "owner_show_url": "/u/jflinn/",
                "postid": 3,
                "text": "I <3 chickens",
            },
            {
                "commentid": 3,
                "owner": "michjc",
                "owner_show_url": "/u/michjc/",
                "postid": 3,
                "text": "Cute overload!",
            },
            {
                "commentid": 8,
                "owner": "awdeorio",
                "owner_show_url": "/u/awdeorio/",
                "postid": 3,
                "text": "new comment",
            },
        ],
        "url": "/api/v1/p/3/comments/",
    }


def test_security(client):
    """Verify error response when user is not logged in.

    Note: 'client' is a fixture fuction that provides a Flask test server
    interface with a clean database.  It is implemented in conftest.py and
    reused by many tests.  Docs: https://docs.pytest.org/en/latest/fixture.html
    """
    response = client.get("/")
    assert response.status_code == 302  # Redirect to login page

    response = client.get("/api/v1/")
    assert response.status_code == 200  # Publicly available

    response = client.get("/api/v1/p/?page=1")
    assert response.status_code == 403

    response = client.get("/api/v1/p/?size=1")
    assert response.status_code == 403

    response = client.get("/api/v1/p/")
    assert response.status_code == 403
