from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
import re

class Pet:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.address = data["address"]
        self.image = ""
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO pets (first_name, last_name, address, image, user_id) VALUES (%(first_name)s, %(last_name)s, %(address)s, NULL, %(user_id)s);"
        print("Ran save function")
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM pets WHERE id = %(id)s;"
        pet_from_id = connectToMySQL("pet_care_organizer").query_db(query, data)
        if len(pet_from_id) < 1:
            return False
        return cls(pet_from_id[0])

    @classmethod
    def all_pets_by_user(cls, data):
        query = "SELECT * FROM pets WHERE user_id = %(user_id)s;"
        pets_from_id = connectToMySQL("pet_care_organizer").query_db(query, data)
        if len(pets_from_id) < 1:
            return False
        return pets_from_id

    @staticmethod
    def update(data):
        query = "UPDATE pets SET first_name = %(first_name)s, last_name = %(last_name)s, address = %(address)s WHERE id = %(id)s;"
        print("Updating ", data["id"])
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @staticmethod
    def delete(data):
        query = "DELETE FROM jobs WHERE pet_id = %(id)s;"
        print("Deleting all Jobs with pet_id ", data["id"])
        connectToMySQL("pet_care_organizer").query_db(query, data)
        query = "DELETE FROM pets WHERE id = %(id)s;"
        print("Deleting Pet ", data["id"])
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @staticmethod
    def verify_pet(data):
        is_valid = True
        if not len(data["first_name"]) >= 1:
            flash("First name must be at least one character.")
            is_valid = False
        if not len(data["last_name"]) >= 1:
            flash("Last name must be at least one character.")
            is_valid = False
        if not len(data["address"]) >= 1:
            flash("Address must be at least one character.")
            is_valid = False
        return is_valid