# File Name: main.py
# Author: Samuel Lewis

#$ TO-DO List $#
#[] TO-DO List Item
#[*] Completed TO-DO List Item

#* Libraries *#

import os
import requests
import mysql.connector as mysql
import json

#= Classes =#

class MySQL:
    class InBound:
        def __init__(self, sql_host: str, sql_usr: str, sql_pwd: str, sql_db: str):
            """
            Initial information needed to access the MySQL database.
            :param sql_host: IP address of the MySQL server.
            :param sql_usr: Username used to log in to the MySQL server.
            :param sql_pwd: Password used to log in to the MySQL server.
            """
            self.sql_host = sql_host
            self.sql_usr = sql_usr
            self.sql_pwd = sql_pwd
            self.sql_db = sql_db

        def usrReq(self, req_type: str):
            """
            Used to connect to the MySQL database and gathers a set of request types.
            :param req_type: The Set of Request types to pull from the MySQL database.
            """
            # Establishes connection between The J.A.R.V.I.S. Project Client and MYSQL Database
            conn = mysql.connect(
                host=self.sql_host,
                user=self.sql_usr,
                password=self.sql_pwd,
                database=self.sql_db,
            )
            cursor = conn.cursor()
            query = f"SELECT REQUEST FROM user_requests WHERE REQUESTTYPE='{req_type}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                json_data = row[0]  # Assuming the JSON data is in the first column
                parsed_data = json.loads(str(json_data))  # Parse JSON to a Python dictionary
                requestList = parsed_data.get('request', [])
                return requestList
            conn.close()
            return None

        def jarRep(self, rep_type: str):
            """
            Used to connect to the MySQL database and gathers a set of response types.
            :param rep_type: The Set of Response types to pull from the MySQL database.
            """
            conn = mysql.connect(
                host=self.sql_host,
                user=self.sql_usr,
                password=self.sql_pwd,
                database=self.sql_db,
            )
            cursor = conn.cursor()
            query = f"SELECT RESPONSE FROM jarvis_responses WHERE RESPONSETYPE='{rep_type}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                json_data = row[0]  # Assuming the JSON data is in the first column
                parsed_data = json.loads(str(json_data))  # Parse JSON to a Python dictionary
                responseList = parsed_data.get('responses', [])
                return responseList
            conn.close()
            return None

        def atVal(self, at_assignment: int):
            """
            Used to connect to the MySQL database and get the assignment value of an April Tag
            :param at_assignment: The April Tag value to pull from the MySQL database.
            """
            conn = mysql.connect(
                host=self.sql_host,
                user=self.sql_usr,
                password=self.sql_pwd,
                database=self.sql_db,
            )
            cursor = conn.cursor()
            query = f"SELECT AssignmentTask FROM april_tag_assignments WHERE TagID='{at_assignment}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                AssignmentTask = row[0]
                return AssignmentTask
            conn.close()
            return None

#! Main Program !#

#~ the main program goes here



#- UNASSIGNED COLOR -#
#| UNASSIGNED COLOR |#
#? UNASSIGNED COLOR ?#
#+ UNASSIGNED COLOR +#
#: UNASSIGNED COLOR :#
#; UNASSIGNED COLOR ;#
#% UNASSIGNED COLOR %#
#@ UNASSIGNED COLOR @#
