"""Return comments on postid."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/comments/',
                    methods=['GET', 'POST'])
def get_comments(postid_url_slug):
    """Get Comments."""
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    logname = flask.session["logname"]
    connection = insta485.model.get_db()

    # POST request
    if flask.request.method == 'POST':
        data = flask.request.get_json()

        """  cur = connection.execute(
            "SELECT MAX(commentid) "
            "FROM comments "
        )
        maxid = cur.fetchall()
        max = maxid[0] """

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
