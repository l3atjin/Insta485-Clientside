"""REST API for likes."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/',
                    methods=['POST', 'GET', 'DELETE'])
def get_likes(postid_url_slug):
    """Return likes on postid."""
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

    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    # Set Connection
    logname = flask.session["logname"]

    # Delete request
    if flask.request.method == 'POST':
        cur = connection.execute(
            "SELECT * "
            "FROM likes "
            "WHERE postid = ?",
            (postid_url_slug, )
        )
        likes = cur.fetchall()

        logname_likes = 0

        for like in likes:
            if like["owner"] == logname:
                logname_likes = 1
            break

        if not logname_likes:
            connection.execute(
                "INSERT INTO likes(owner, postid) "
                "VALUES(?, ?) ",
                (logname, postid_url_slug, )
            )

            context = {
                "logname": logname,
                "postid": postid_url_slug,
            }
            return flask.jsonify(**context), 201
        context = {
            "logname": logname,
            "message": "Conflict",
            "postid": postid_url_slug,
            "status_code": 409,
        }
        return flask.jsonify(**context), 409

    # Delete request
    if flask.request.method == 'DELETE':
        cur = connection.execute(
            "DELETE FROM likes "
            "WHERE owner=? AND postid=? ",
            (logname, postid_url_slug,)
        )
        if cur:
            return '', 204

    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE postid = ?",
        (postid_url_slug, )
    )
    likes = cur.fetchall()
    logname_likes = 0

    for like in likes:
        if like["owner"] == logname:
            logname_likes = 1
            break

    context = {
        "logname_likes_this": logname_likes,
        "likes_count": len(likes),
        "postid": postid_url_slug,
        "url": flask.request.path,
    }

    return flask.jsonify(**context)
