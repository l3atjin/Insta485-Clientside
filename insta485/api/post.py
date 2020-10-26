"""Return post."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<string:postid_url_slug>/', methods=["GET"])
def get_post(postid_url_slug):
    """Get a Post."""
    """ if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login')) """

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT * "
        "FROM posts "
        "WHERE postid = ?",
        (postid_url_slug, )
    )
    posts = cur.fetchall()

    if len(posts) == 0:
        context = {
            "message": "Not Found",
            "status_code": 403
        }
        return flask.jsonify(**context), 403

    post = posts[0]

    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?",
        (post["owner"], )
    )
    users = cur.fetchall()
    user = users[0]

    context = {
        "age": post["created"],
        "img_url": "/uploads/" + post["filename"],
        "owner": post["owner"],
        "owner_img_url": "/uploads/" + user["filename"],
        "owner_show_url": "/u/" + post["owner"] + "/",
        "post_show_url": "/p/" + str(postid_url_slug) + "/",
        "url": "/api/v1/p/" + str(post["postid"]) + "/",
    }

    return flask.jsonify(**context)
