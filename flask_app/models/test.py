# a cursor is the object we use to interact with the database
import pymysql.cursors


from flask import session, flash
import re

# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', # change the user and password as needed
                                    password = 'rootroot', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        # establish the connection to the database
        self.connection = connection

    # the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 

# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)

class Job:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.time_st = data["time_st"]
        self.time_end = data["time_end"]
        self.payment = data["payment"]
        self.completed = data["completed"]
        self.poster_user_id = data["poster_user_id"]
        self.completer_user_id = data["completer_user_id"]
        self.pet_id = data["pet_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO bands (name, user_id, genre, city) VALUES (%(name)s, %(user_id)s, %(genre)s, %(city)s);"
        print("Ran save and join functions")
        band_id = connectToMySQL("pet_care_organizer").query_db(query, data)
        data2 = {
            "user_id" : data["user_id"],
            "band_id" : band_id
        }
        query = "INSERT INTO user_band_relationships (user_id, band_id) VALUES (%(user_id)s, %(band_id)s);"
        return connectToMySQL("pet_care_organizer").query_db(query, data2)

    @classmethod
    def get_job(cls, data):
        query = "SELECT * FROM bands WHERE id = %(id)s;"
        band_from_id = connectToMySQL("pet_care_organizer").query_db(query, data)
        if len(band_from_id) < 1:
            return False
        return cls(band_from_id[0])

    @staticmethod
    def get_all_jobs():
        query = "SELECT * FROM jobs LEFT JOIN pets ON jobs.pet_id = pets.id LEFT JOIN users as x ON jobs.poster_user_id = x.id LEFT JOIN users as y ON jobs.completer_user_id = y.id ORDER BY time_st DESC;"
        results = connectToMySQL('pet_care_organizer').query_db(query)
        print(results)
        return None
        # pass
        # job_list = []
        # for row_from_db in results:
        #     job_data = {
        #         "id" : row_from_db["id"],
        #         "name" : row_from_db["name"],
        #         "first_name" : row_from_db["first_name"],
        #         "last_name" : row_from_db["last_name"],
        #         "user_id" : row_from_db["user_id"],
        #         "genre" : row_from_db["genre"],
        #         "part_of_band" : part_of_band
        #     }
        #     band_list.append(band_data)
        # return band_list

    @staticmethod
    def verify_job(data):
        is_valid = True
        if not len(data["name"]) > 1:
            flash("Name must be at least two characters.")
            is_valid = False
        if not len(data["genre"]) > 1:
            flash("Genre must be at least two characters.")
            is_valid = False
        if not len(data["city"]) >= 1:
            flash("The home city cannot be blank.")
            is_valid = False
        return is_valid

    @staticmethod
    def update(data):
        query = "UPDATE bands SET name = %(name)s, genre = %(genre)s, city = %(city)s WHERE id = %(id)s;"
        print("Updating ", data["id"])
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @staticmethod
    def mark_completed(data):
        query = ""

    @staticmethod
    def mark_completer_null(data):
        query = ""

    @staticmethod
    def change_completer(data):
        query = ""

    @staticmethod
    def delete(data):
        query = "DELETE FROM user_band_relationships WHERE band_id = %(id)s;"
        print("Deleting Band ", data["id"], " and removing any members.")
        connectToMySQL("pet_care_organizer").query_db(query, data)
        query = "DELETE FROM bands WHERE id = %(id)s;"
        return connectToMySQL("pet_care_organizer").query_db(query, data)

    @staticmethod
    def clear_by_pet_id(data):
        query = ""

Job.get_all_jobs()
print("a")
