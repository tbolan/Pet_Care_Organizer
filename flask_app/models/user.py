from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
import re

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        print("Ran save function")
        return connectToMySQL("pet_care_organizer").query_db(query, data)
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        user_from_email = connectToMySQL("pet_care_organizer").query_db(query, data)
        if len(user_from_email) < 1:
            return False
        return cls(user_from_email[0])

    @staticmethod
    def validate_user(data):
        email_format = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if not (len(data["first_name"]) >= 1):
            flash("First name must be at least one character.", "register")
            is_valid = False
        if not (len(data["last_name"]) >= 1):
            flash("Last name must be at least one character.", "register")
            is_valid = False
        if not email_format.match(data["email"]):
            flash("Invalid email format.", "register")
            is_valid = False
        check_emails = User.get_by_email(data)
        if check_emails:
            flash("Email already in use.", "register")
            is_valid = False
        if not len(data["password"]) > 7:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if not data["password"] == data["confirm_password"]:
            flash("Passwords do not match.", "register")
            is_valid = False
        return is_valid