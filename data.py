import sqlite3


def search_data(blocks_max, no_clone, no_teigi):


    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(f"select * from total_blocks where blocks_count <= {min(int(blocks_max), 500)} order by blocks_count asc")

    projects = cursor.fetchall()

    #print(projects)

    result_data = []

    for project in projects:
        project_dict = {}

    #    loves = (project[4])

        cursor.execute(f"select * from basic_info where project_id = {project[0]}")

        result = cursor.fetchall()[0]

        loves = result[4]
    
        blocks_count, variables_count, contains_clone, contains_procedure = project[1], project[2], project[3], project[4]

        flag = True

        print([no_clone])

        if contains_clone == "True" and no_clone == "on":
            flag = False

        if contains_procedure == "True" and no_teigi == "on":
            flag = False

        project_dict = {"title":result[1],
                        "project_URL": "https://scratch.mit.edu/projects/" + result[0],
                        "thumbnail_URL":result[3],
                        "user_name":result[2],
                        "loves":loves,
                        "blocks_count":blocks_count,
                        "variables_count":variables_count, 
                        "contains_clone":contains_clone, 
                        "contains_procedure":contains_procedure, }

        if loves >= 10 and  blocks_count > 20 and flag and result[2] != "ScratchCat":
            result_data.append(project_dict)

    return result_data
