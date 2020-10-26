"""Recent post returner."""
import flask
import insta485


@insta485.app.route('/api/v1/p/', methods=["GET", "POST"])
def get_recent_posts():
    """Return some posts."""
    # Boot if not in session
    # Get variable arguments
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)

    if(page < 0 or size < 0):
        context = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(**context), 403

    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login')), 403

    logname = flask.session["logname"]
    connection = insta485.model.get_db()

    # Get logname followings
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?",
        (logname,)
    )
    # Make container
    following = cur.fetchall()
    following_users = []

    # Add self to container
    for post in following:
        following_users.append(post["username2"])
    following_users.append(logname)

    cur = connection.execute(
        "SELECT postid, owner "
        "FROM posts "
    )
    temposts = cur.fetchall()
    final_posts = []
    posts = []
    index = 1
    count = 0
    for post in temposts:
        posts.append(post)

    posts.reverse()

    for post in posts:
        if post["owner"] in following_users:
            if index < 1 + (page) * size:
                index += 1
            else:
                del post["owner"]
                post["url"] = "/api/v1/p/" + str(post["postid"]) + "/"
                final_posts.append(post)
                index += 1
                count += 1
        if count >= size:
            break

    nextpage = ""
    if len(final_posts) >= size:
        nextpage = "/api/v1/p/" + "?size=" + str(size) + "&page=" + str(page+1)

    context = {
        "next": nextpage,
        "results": final_posts,
        "url": "/api/v1/p/",
    }

    return flask.jsonify(**context)
