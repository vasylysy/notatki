from flask import render_template, redirect, url_for, request, flash
import hashlib

from flask_login import login_user, login_required, logout_user, current_user

from app import db, app, manager
from models import Notebook, Notes, User, load_user
from app.crypt import verify_password, encrypt_password, strength_password

global auth
auth = [False]


@app.route("/")
def redirect_to_home():
    return redirect(url_for("login_p"))


@app.route("/signin", methods=["GET", "POST"])
def login_p():
    login = request.form.get('login')
    password = request.form.get('password')

    if request.method == "POST":
        if not login:
            return render_template("login.html", message="User Name cannot be blank")
        elif not password:
            return render_template("login.html", message="Password cannot be blank")
        user = User.query.filter_by(login=login).first()
        if not user:
            return render_template("login.html", message="User Name does not exist")
        elif verify_password(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            return render_template("login.html", message="Password is incorrect")
    return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('redirect_to_home'))


@app.route("/signup", methods=["GET", "POST"])
def register_p():
    login = request.form.get('login')
    password = request.form.get('password')
    password1 = request.form.get('password1')

    if request.method == "POST":
        if not login:
            return render_template("register.html", message="User Name cannot be blank")
        elif User.query.filter_by(login=login).first():
            return render_template("register.html", message="User Name already exists")
        elif not password or not password1:
            return render_template("register.html", message="Password fields cannot be blank")
        elif password != password1:
            return render_template("register.html", message="Passwords must be same")
        elif strength_password(password) < 3:
            return render_template("register.html", message="Too week")
        hash_pwd = encrypt_password(password)
        new_user = User(login=login, password=hash_pwd)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html")


@app.route("/notes")
@app.route("/index")
def honey():
    return redirect("https://www.youtube.com/watch?v=BBGEG21CGo0")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    all_notebooks = Notebook.query.filter_by(user_id=current_user.get_id()).all()

    length = len(all_notebooks)
    i = 0

    while i < length:
        auth.append(False)
        i += 1

    for i in all_notebooks:
        auth.append(False)

    if not all_notebooks:
        notebook_available = False
    else:
        notebook_available = True

    return render_template("index.html", notebooks=all_notebooks, notebook_available=notebook_available)


@app.route("/notebook/create", methods=["GET", "POST"])
@login_required
def create_notebook():
    uid = current_user.get_id()
    if request.method == "POST":
        if request.form["name"] and not request.form["name"].isspace():
            if request.form["password"] and not request.form["password"].isspace():
                db.session.add(Notebook(user_id=uid, name=request.form["name"],
                                        password=hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest()))
            else:
                db.session.add(Notebook(user_id=uid, name=request.form["name"]))
            db.session.commit()
            return redirect("/home")
        else:
            return render_template("create_notebook.html", message="Name cannot be blank")
    else:
        return render_template("create_notebook.html")


@app.route("/notebooks/<int:notebook_id>/delete", methods=["GET", "POST"])
@login_required
def delete_notebook(notebook_id):
    uid = int(current_user.get_id())
    required_id = int(Notebook.query.get(notebook_id).user_id)
    if required_id is uid:
        if request.method == "POST":
            if Notebook.query.get(notebook_id).password is not None:
                if hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest() == Notebook.query.get(
                        notebook_id).password:
                    Notebook.query.filter_by(id=notebook_id).delete()
                    Notes.query.filter_by(notes_notebook=notebook_id).delete()
                    db.session.commit()
                    return redirect("/home")
                else:
                    return render_template("delete_notebook.html", name=Notebook.query.get(notebook_id).name,
                                           id=notebook_id, password=True,
                                           message="The Password is Incorrect")
            else:
                Notebook.query.filter_by(id=notebook_id).delete()
                Notes.query.filter_by(notes_notebook=notebook_id).delete()
                db.session.commit()
                return redirect("/home")
        else:
            if Notebook.query.get(notebook_id).password is None:
                password = False
            else:
                password = True
            return render_template("delete_notebook.html", name=Notebook.query.get(notebook_id).name, id=notebook_id,
                                   password=password)
    else:
        return redirect(url_for('honey'))


@app.route("/notebooks/<int:notebook_id>/note/<int:note_id>/delete", methods=["GET", "POST"])
@login_required
def delete_note(notebook_id, note_id):
    uid = int(current_user.get_id())
    required_id = int(Notebook.query.get(notebook_id).user_id)
    if required_id is uid:
        if request.method == "POST":
            Notes.query.filter_by(id=note_id).delete()
            db.session.commit()
            return redirect("/notebooks/" + str(notebook_id))
        else:
            return render_template("delete_note.html", notebook=Notebook.query.get(notebook_id).id,
                                note=Notes.query.get(note_id).id)
    else:
        return redirect(url_for('honey'))


@app.route("/notebooks/<int:notebook_id>", methods=["GET", "POST", "DELETE"])
@login_required
def open_notebook(notebook_id):
    uid = int(current_user.get_id())
    required_id = int(Notebook.query.get(notebook_id).user_id)
    if required_id is uid:
        if Notebook.query.get(notebook_id).password is None:
            return render_template("open.html", notes=Notes.query.filter(Notes.notes_notebook == notebook_id),
                                   notebook=Notebook.query.get(notebook_id), open=False)
        else:
            if auth[notebook_id]:
                return render_template("open.html", notes=Notes.query.filter(Notes.notes_notebook == notebook_id),
                                       notebook=Notebook.query.get(notebook_id), open=False)
            else:
                return redirect("/notebooks/" + str(notebook_id) + "/login")
    else:
        return redirect(url_for('honey'))


@app.route("/notebooks/<int:notebook_id>/login", methods=["GET", "POST"])
@login_required
def login_notebook(notebook_id):
    uid = int(current_user.get_id())
    required_id = int(Notebook.query.get(notebook_id).user_id)
    if required_id is uid:
        if request.method == "POST":
            password = hashlib.sha256(request.form["password"].encode('utf-8')).hexdigest()
            if password == Notebook.query.get(notebook_id).password:
                auth[notebook_id] = True
                return redirect("/notebooks/" + str(notebook_id))
            else:
                return render_template("notebook_login.html", notebook=Notebook.query.get(notebook_id),
                                       message="The password is "
                                               "incorrect")
        else:
            return render_template("notebook_login.html", notebook=Notebook.query.get(notebook_id))
    else:
        return redirect(url_for('honey'))


@app.route("/notebooks/<int:notebook_id>/note/create", methods=["GET", "POST"])
@login_required
def create_note(notebook_id):
    uid = int(current_user.get_id())
    required_id = int(Notebook.query.get(notebook_id).user_id)
    if required_id is uid:
        if request.method == "POST":
            if request.form["name"] and not request.form["name"].isspace():
                db.session.add(
                    Notes(name=request.form["name"], content=request.form["content"], notes_notebook=notebook_id))
                db.session.commit()
                return redirect("/notebooks/" + str(notebook_id))
            else:
                return render_template("create_note.html", message="Name cannot be blank", id=notebook_id)
        else:
            return render_template("create_note.html", id=notebook_id)
    else:
        return redirect(url_for('honey'))


@app.route("/notebooks/<int:notebook_id>/note/<int:note_id>", methods=["GET", "POST"])
@login_required
def open_note(notebook_id, note_id):
    uid = int(current_user.get_id())
    required_id = int(Notebook.query.get(notebook_id).user_id)
    if required_id is uid:
        if request.method == "POST":
            Notes.query.get(note_id).name = request.form["title"]
            Notes.query.get(note_id).content = request.form["content"]

            Notes.query.get(note_id).name = request.form["title"]
            Notes.query.get(note_id).content = request.form["content"]

            if request.form["font"] and not request.form["font"].isspace():
                Notes.query.get(note_id).font = request.form["font"]
            if request.form["color"] and not request.form["color"].isspace():
                Notes.query.get(note_id).color = request.form["color"]

            db.session.commit()
            return render_template("open.html", notes=Notes.query.filter(Notes.notes_notebook == notebook_id),
                                   notebook=Notebook.query.get(notebook_id), open=True, opened=Notes.query.get(note_id))

        return render_template("open.html", notes=Notes.query.filter(Notes.notes_notebook == notebook_id),
                               notebook=Notebook.query.get(notebook_id), open=True, opened=Notes.query.get(note_id))
    else:
        return redirect(url_for('honey'))


@app.route("/notebooks/<int:notebook_id>/edit", methods=["GET", "POST"])
@login_required
def edit_notebook(notebook_id):
    uid = int(current_user.get_id())
    required_id = int(Notebook.query.get(notebook_id).user_id)
    if required_id is uid:
        if request.method == "POST":
            if request.form["name"] and not request.form["name"].isspace():
                Notebook.query.get(notebook_id).name = request.form["name"]
                db.session.commit()
                return open_notebook(notebook_id)
            else:
                return render_template("edit_notebook.html", notebook=Notebook.query.get(notebook_id),
                                       message="Name cannot be Blank")

        return render_template("edit_notebook.html", notebook=Notebook.query.get(notebook_id))
    else:
        return redirect(url_for('honey'))


@manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("login_p"))
