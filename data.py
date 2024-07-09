import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("select * from basic_info;")

projects = cursor.fetchall()

test_data = []

for project in projects:
    project_dict = {}

    project_dict = {"title":project[1], "project_URL": "scratch.mit.edu/projects/" + project[0], "thumbnail_URL":project[3], "user_name":project[2]}

    test_data.append(project_dict)

