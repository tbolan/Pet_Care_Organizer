from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import job
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/jobs")
def jobs():
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to view the jobs page.", "login")
        return redirect("/")
    all_jobs = job.Job.get_all_jobs()
    if all_jobs == False:
        all_jobs = []
    my_jobs = []
    posted_jobs = []
    for j in all_jobs:
        if j.completed == 1:
            continue
        if (session["id"] == j.poster_user_id) or (session["id"] == j.completer_user_id):
            my_jobs.append(j)
        if j.completer_user_id == None:
            posted_jobs.append(j)
    return render_template("jobs.html", my_jobs=my_jobs, posted_jobs=posted_jobs)

@app.route("/jobs/add")
def job_new():
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to create a new job post.", "login")
        return redirect("/")
    return render_template("jobs_add.html")

@app.route("/jobs/submit", methods = ["POST"])
def job_submit():
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to post a job.", "login")
        return redirect("/")
    if not job.Job.verify_job(request.form):
        return redirect("/jobs/add")
    data = {
        "title" : request.form["title"],
        "description" : request.form["description"],
        "date" : request.form["date"],
        "time_st" : request.form["time_st"],
        "time_end" : request.form["time_end"],
        "payment" : request.form["payment"],
        "completed" : request.form["completed"],
        "poster_user_id" : request.form["poster_user_id"],
        "completer_user_id" : request.form["completer_user_id"],
        "pet_id" : request.form["pet_id"],
    }
    # print(request.form["completer_user_id"], type(request.form["completer_user_id"]))
    # print(data["completer_user_id"], type(data["completer_user_id"]))
    if data["completer_user_id"] == "1":
        data["completer_user_id"] = None
    if data["completer_user_id"] == "0":
        data["completer_user_id"] = data["poster_user_id"]
    job.Job.save(data)
    return redirect("/jobs")

@app.route("/jobs/view/<job_id>")
def job_view(job_id):
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to view a job post.", "login")
        return redirect("/")
    job_entry = job.Job.get_all_info_by_id({"id" : job_id})
    return render_template("jobs_view.html", job_entry=job_entry)

@app.route("/jobs/edit/<job_id>")
def job_edit(job_id):
    if (not (session.get("id", False))) or (not (session.get("id", False) == job.Job.get_by_id({"id" : job_id}).poster_user_id)):
        session.clear()
        flash("Sorry this job must exist and you must be the owner of it to edit.", "login")
        return redirect("/")
    job_entry = job.Job.get_by_id({"id" : job_id})
    return render_template("jobs_edit.html", job_entry = job_entry)

@app.route("/jobs/edit/<job_id>/update", methods = ["POST"])
def job_update(job_id):
    if (not (session.get("id", False))) or (not (session.get("id", False) == job.Job.get_by_id({"id" : job_id}).poster_user_id)):
        session.clear()
        flash("Sorry this job must exist and you must be the owner of it to edit.", "login")
        return redirect("/")
    if not job.Job.verify_job(request.form):
        return redirect("/jobs/edit/"+job_id)
    job.Job.update(request.form)
    return redirect("/jobs")

@app.route("/jobs/complete/<job_id>")
def job_complete(job_id):
    if (not (session.get("id", False))) or (not (session.get("id", False) == job.Job.get_by_id({"id" : job_id}).completer_user_id)):
        session.clear()
        flash("Sorry this job must exist and you must be the signed up to complete it.", "login")
        return redirect("/")
    job.Job.mark_completed({"id" : job_id})
    return redirect("/jobs")

@app.route("/jobs/return/<job_id>")
def job_return(job_id):
    if (not (session.get("id", False))) or (not (session.get("id", False) == job.Job.get_by_id({"id" : job_id}).completer_user_id)):
        session.clear()
        flash("Sorry this job must exist and you must be the signed up to complete it to remove it from your to-do list.", "login")
        return redirect("/")
    job.Job.mark_completer_null({"id" : job_id, "completer_user_id" : None})
    return redirect("/jobs")

@app.route("/jobs/accept/<job_id>")
def job_accept(job_id):
    if not session.get("id", False):
        session.clear()
        flash("Sorry you must login first to take-on a job post.", "login")
        return redirect("/")
    job.Job.change_completer({"user_id" : session["id"], "job_id" : job_id})
    return redirect("/jobs")

@app.route("/jobs/delete/<job_id>")
def job_delete(job_id):
    if (not (session.get("id", False))) or (not (session.get("id", False) == job.Job.get_by_id({"id" : job_id}).poster_user_id)):
        session.clear()
        flash("Sorry this job must exist and you must be the owner of it to edit.", "login")
        return redirect("/")
    job.Job.delete({"id" : job_id})
    return redirect("/jobs")
