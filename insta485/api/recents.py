"""Recent post returner."""
import flask
import insta485


@insta485.app.route('/api/v1/p/', methods=["GET", "POST"])
def get_recent_posts():
    """Return some posts."""
    # Boot if not in session
    if "logname" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    logname = flask.session["logname"]
    connection = insta485.model.get_db()

    # Get variable arguments
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=1, type=int)

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

    for fol in following:
        following_users.append(fol["username2"])
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
            if index < 1 + (page - 1) * size:
                index+=1
            else:
                del post["owner"]
                post["url"] = "/api/v1/p/" + str(post["postid"]) + "/"
                final_posts.append(post)
                index+=1
        if count >= size:
            break
    

    nextpage = ""
    if len(posts) > size:
        nextpage = "/api/v1/p/" + "?size=" + str(size) + "&page=" + str(page)

    context = {
        "next": nextpage,
        "results": final_posts,
        "url": "/api/v1/p/",
    }

    return flask.jsonify(**context)
