from flask import Flask, render_template, request, redirect, session, url_for, json, flash
from Database.database import Database

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route("/", methods=["POST", "GET"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    
   
    return render_template("test.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = Database()
        u_id = db.verify_password(username, password)
        db.close()
        if not u_id:
            flash("Invalid Crendentials!/Account does not exist!", "danger")
            return redirect(url_for("login"))
        session["user"] = u_id
        db = Database()
        intensity = db.get_user_stress(session["user"])
        db.close()
        if intensity != None:
            session['intensity'] = intensity
            return redirect(url_for("test_forum", intensity=intensity))
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]
        if " " in username or confirm_password != password:
            flash("Passwords don't match/Spaces not allowed in username!", "warning")
            return redirect(url_for("register"))
        db = Database()
        db.add_user(username, password)
        db.close()
        flash("User created!", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "user_data" not in session:
        return redirect(url_for("home"))
    user_data = session["user_data"]
    classes = user_data['classes']
    activities = user_data['activities']
    class_suggestions = user_data['ClassSuggestions']
    activity_suggestions = user_data['ActvitySuggestions']
    synopsis = user_data['Synposis']
    db = Database()
    username = db.get_username(session["user"])
    db.close()
    # print(user_data)
    #classes = user_data["UserData"]["classes"]
    #activities = user_data["UserData"]["activities"]
    return render_template("profile.html", username=username, classes=classes, activities=activities, class_suggestions=class_suggestions, activity_suggestions=activity_suggestions, synopsis=synopsis)


@app.route("/forum/<intensity>")
def test_forum(intensity):
    if session['intensity'] != intensity or 'user' not in session:
        return redirect(url_for("home"))
    stats = {}
    db = Database()
    posts = db.get_posts(intensity)
    for x in range(len(posts)):
        posts[x]["user_id"] = db.get_username(posts[x]["user_id"])
    
    if posts == None:
        stats["post_count"] = 0
    else:
        stats["post_count"] = len(posts)
    members = db.get_users(intensity)
    if members == None:
        stats["member_count"] = 0
    else:
        stats["member_count"] = len(members)
    db.close()

    return render_template("test_forum.html", intensity=intensity, posts=posts, stats=stats, user_id=session["user"])
    

@app.route("/forum/<intensity>/<post_id>", methods=["POST", "GET"])
def post(intensity, post_id):
    if request.method == "POST":
        comment = request.form["comment"]
        print(comment)
        db = Database()
        db.add_comment(post_id, session["user"], comment)
        db.close()

    db = Database()
    post_info = db.get_post_desc(post_id)
    name = db.get_username(post_info["user_id"])
    comments = db.get_comments(post_id)
    db.close()
    full_desc = post_info["full_desc"]
    title = post_info["title"]

    return render_template("post.html", name=name, full_desc=full_desc, comments=comments, title=title)


@app.route("/forum")
def forum():
    if "intensity" not in session:
        return redirect(url_for("home"))
    
    return redirect(url_for("test_forum", intensity=session["intensity"]))

@app.route("/forum/<intensity>/<user_id>/publish", methods=["POST", "GET"])
def user_post(intensity, user_id):
    if "user" not in session or session["user"] != int(user_id):
        return redirect(url_for("test_forum", intensity=intensity))
    
    db = Database()
    name = db.get_username(user_id)
    db.close()

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["paragraph-text"]
        db = Database()
        db.add_post(user_id, title, body)
        db.close()

        return redirect(url_for("test_forum", intensity=intensity))

    return render_template("user-post.html", name=name)


@app.route("/tag-user", methods=["POST"])
def tag_user():
    data = request.get_json()
    user_id = session["user"]
    print(data)
    intensity = data['Intensity']
    user_data = data["UserData"]
    session["user_data"] = user_data
    db = Database()
    if db.check_if_already_tagged(user_id):
        db.alter_stress_level(user_id, intensity)
        session['intensity'] = data['Intensity']
    else:
        db.tag_user(user_id, intensity)
        session['intensity'] = intensity
    db.close()
    return json.dumps({"success":True}), 200



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")