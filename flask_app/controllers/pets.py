from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import pet
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/pets")
def pets():
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to try to add a pet.", "login")
        return redirect("/")
    pet_list = pet.Pet.all_pets_by_user({"user_id" : session["id"]})
    if pet_list == False:
        pet_list = []
    return render_template("pets_view.html", pet_list=pet_list)

@app.route("/pets/add")
def pets_add():
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to try to add a pet.", "login")
        return redirect("/")
    return render_template("pets_add.html")

@app.route("/pets/submit", methods = ["POST"])
def pets_submit():
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to try to add a pet.", "login")
        return redirect("/")
    print(request.form)
    if not pet.Pet.verify_pet(request.form):
        return redirect("/pets/add")
    pet.Pet.save(request.form)
    return redirect("/pets")

@app.route("/pets/edit/<pet_id>")
def pets_edit(pet_id):
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to edit a pet.", "login")
        return redirect("/")
    pet_entry = pet.Pet.get_by_id({"id" : pet_id})
    return render_template("pets_edit.html", pet_entry = pet_entry)

@app.route("/pets/edit/<pet_id>/submit", methods = ["POST"])
def pets_update(pet_id):
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to edit a pet.", "login")
        return redirect("/")
    if not pet.Pet.verify_pet(request.form):
        return redirect("/pets/edit/"+pet_id)
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "address" : request.form["address"],
        "id" : pet_id
    }
    pet.Pet.update(data)
    return redirect("/pets")

@app.route("/pets/delete/<pet_id>")
def pets_delete(pet_id):
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to delete a pet.", "login")
        return redirect("/")
    pet.Pet.delete({"id" : pet_id})
    return redirect("/pets")