"""Return comments on postid."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/comments/',
                    methods=['GET', 'POST'])
def get_comments(postid_url_slug):
    """Get Comments."""
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

    logname = flask.session["logname"]

    # POST request
    if flask.request.method == 'POST':
        data = flask.request.get_json()

        connection.execute(
            "INSERT INTO comments(owner, postid, text) "
            "VALUES(?, ?, ?) ",
            (logname, postid_url_slug, data["text"], )
        )

        cur = connection.execute(
            "SELECT MAX(commentid), owner, postid, commentid "
            "FROM comments "
            "WHERE postid = ?",
            (postid_url_slug, )
        )
        comments = cur.fetchall()
        comment = comments[0]
        context = {
            "commentid": comment["commentid"],
            "owner": comment["owner"],
            "owner_show_url": "/u/" + comment["owner"] + "/",
            "postid": postid_url_slug,
            "text": data["text"],
        }
        return flask.jsonify(**context), 201

    # GET request
    cur = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE postid = ?",
        (postid_url_slug, )
    )
    comments = cur.fetchall()

    for comment in comments:
        del comment["created"]
        comment["owner_show_url"] = "/u/" + comment["owner"] + "/"

    context = {
        "comments": comments,
        "url": "/api/v1/p/" + str(postid_url_slug) + "/comments/"
    }

    return flask.jsonify(**context)
