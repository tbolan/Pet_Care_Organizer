from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
from flask_app.models import pet
import re

a = """
v1.0 Pet Care Organizer App

This app is for pet sitters to organize their upcoming pet jobs; it is not designed to be used for pet owners who want to find a sitter.
It is to allow pet sitters to organize their own upcoming jobs and post jobs they can no longer complete for other pet sitters to take on.

Issues:
-no job history page: can't view completed jobs on web page (only in db) nor can't view payment history
-payment option may not allow cents
-allows duplicates for pets

Assumptions:
-one user per email address
-job poster attribute cannot change and that user is only one who can delete it
-pet_id attribute can be updated
-a user can only see his or her own entered pets
-duplicated pets allowed since it is an organizer for each pet sitter

v2.0 Pet Care Organizer App

Introducing support for pet owners!!!

New features:
-fixes privious issues
-messaging system to receive notice if a pet sitter is no longer able to complete a job
-hierarchy of pet entry priveleges with poster_of_pet_user_id and owner_of_pet_user_id and a link the poster can send to the owner to establish ownership for a pet
-same hierarchy of pet entry priveleges but for job entries
-privacy protections so public jobs will not display the address and owner info until a pet sitter becomes the user to complete that job
-safeguards to prevent updating the job once it is completed
-minimized duplicate pet records and job records for the same real life items
-can update and delete user entries
"""

class Job:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.date = data["date"]
        self.time_st = data["time_st"]
        self.time_end = data["time_end"]
        self.payment = data["payment"]
        self.completed = data["completed"]
        self.poster_user_id = data["poster_user_id"]
        self.completer_user_id = data["completer_user_id"]
        self.pet_id = data["pet_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.pet_name = ""

    @classmethod
    def save(cls, data):
        query = """INSERT INTO jobs 
                (title, description, date, time_st, time_end, payment, completed, poster_user_id, completer_user_id, pet_id) VALUES 
                (%(title)s, %(description)s, %(date)s, %(time_st)s, %(time_end)s, %(payment)s, %(completed)s, %(poster_user_id)s, %(completer_user_id)s, %(pet_id)s);"""
        print("Ran save and join functions")
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM jobs WHERE id = %(id)s;"
        job_from_id = connectToMySQL("pet_care_organizer").query_db(query, data)
        if len(job_from_id) < 1:
            return False
        return cls(job_from_id[0])

    @classmethod
    def get_all_info_by_id(cls, data):
        query = "SELECT * FROM jobs LEFT JOIN pets ON jobs.pet_id = pets.id WHERE jobs.id = %(id)s;"
        job_from_id = connectToMySQL("pet_care_organizer").query_db(query, data)
        print("AAAAAAAAAAAAAAAAA -----------------", job_from_id)
        if len(job_from_id) < 1:
            return False
        return job_from_id[0]

    @staticmethod
    def get_all_jobs():
        query = "SELECT * FROM jobs LEFT JOIN pets ON jobs.pet_id = pets.id ORDER BY time_st DESC;"
        results = connectToMySQL('pet_care_organizer').query_db(query)
        job_list = []
        for row in results:
            temp = Job(row)
            temp.pet_name = row["first_name"]+" "+row["last_name"]
            job_list.append(temp)
        return job_list

    @staticmethod
    def verify_job(data):
        is_valid = True
        if not len(data["title"]) >= 1:
            flash("Title must be at least one character.")
            is_valid = False
        if not len(data["description"]) > 19:
            flash("The description must be at least 20 characters.")
            is_valid = False
        if not len(data["date"]) >= 1:
            flash("Must provide date.")
            is_valid = False
        if not len(data["time_st"]) >= 1:
            flash("Must provide start time.")
            is_valid = False
        if not len(data["time_end"]) >= 1:
            flash("Must provide end time.")
            is_valid = False
        if not len(data["payment"]) >= 1:
            flash("Must provide payment, and it must be a number.")
            is_valid = False
        if not ((data["completed"] == "0") or (data["completed"] == "1")):
            flash("Must specify if completed.  Must either put '0' or '1'")
            is_valid = False
        if not ((data["completer_user_id"] == "0") or (data["completer_user_id"] == "1")):
            flash("Must specify if you need someone to complete this job.  Must either put '0' or '1'")
            is_valid = False
        pet_id_dict_list = pet.Pet.all_pets_by_user({"user_id" : data["poster_user_id"]})
        pet_id_list = []
        for d in pet_id_dict_list:
            pet_id_list.append(d["id"])
        if not len(data["pet_id"]) >= 1:
            flash("You must provide a valid pet ID number.  Please create a pet or find an existing pet's ID number from your pet page.")
            is_valid = False
        try:
            if not (int(data["pet_id"]) in pet_id_list):
                flash("You must provide a valid pet ID number.  Please create a pet or find an existing pet's ID number from your pet page.")
                is_valid = False
        except:
            pass 
        return is_valid

    @staticmethod
    def update(data):
        query = "UPDATE jobs SET title = %(title)s, description = %(description)s, date = %(date)s, time_st = %(time_st)s, time_end = %(time_end)s, payment = %(payment)s, completed = %(completed)s, completer_user_id = %(completer_user_id)s, pet_id = %(pet_id)s WHERE id = %(id)s;"
        print("Updating ", data["id"])
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @staticmethod
    def mark_completed(data):
        query = "UPDATE jobs SET completed = 1 WHERE id = %(id)s;"
        print("Updating ", data["id"])
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @staticmethod
    def mark_completer_null(data):
        query = "UPDATE jobs SET completer_user_id = %(completer_user_id)s WHERE id = %(id)s;"
        print("Updating ", data["id"])
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @staticmethod
    def change_completer(data):
        query = "UPDATE jobs SET completer_user_id = %(user_id)s WHERE id = %(job_id)s;"
        print("Updating ", data["job_id"])
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @staticmethod
    def delete(data):
        query = "DELETE FROM jobs WHERE id = %(id)s;"
        print("Deleting Job ", data["id"])
        return connectToMySQL("pet_care_organizer").query_db(query, data)