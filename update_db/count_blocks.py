# 指定されたidのプロジェクトのsb3ファイルを読み取り、ブロック数とかを返すわよ

import sqlite3
import shutil
import zipfile
import os
import json

def count_blocks(project_id):
    # そもそもbasic_infoテーブルに指定されたidのデータが存在しない場合はFalseを返す

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(f"select * from basic_info where project_id = {project_id}")
    result = cursor.fetchall()

    if result == []:
        return "error: No such project in 'basic_info' table"

    # sb3ファイルからjsonファイルを取り出す

    sb3_filename = result[0][6]
    shutil.copy(f"sb3_files/{project_id}/{sb3_filename}", f"json_files/{project_id}.zip")

    with zipfile.ZipFile(f"json_files/{project_id}.zip") as z:
        z.extract("project.json", f"json_files/{project_id}")

    os.remove(f"json_files/{project_id}.zip")
    
    # project.jsonを解読してブロック数を返すわよ

    with open(f"json_files/{project_id}/project.json") as json_file:
        data = json.loads(json_file.read())
    
    targets = data["targets"]

    background = targets[0]

    global_variables = list(background["variables"].keys())
    lists = list(background["lists"].keys())

    exclude_blocks = ["looks_costume", "procedures_prototype", "sensing_keyoptions"]

    counter = 0

    for target in targets:
        # スプライト毎にブロックをカウントしていく

        counter = 0

        blocks = target["blocks"]

        if target["isStage"]:
            local_variables = []
        else:
            local_variables = (target["variables"].keys())

        for block_id in blocks:
            block = blocks[block_id]

            if "opcode" in block:
                if block["opcode"] not in exclude_blocks and ("menu" not in block["opcode"] or block["opcode"] == "looks_costumenumbername"):
                    counter += 1

                    #print(" ",block["opcode"])

                    # ---- just for test of timer ----

                    if "clone" in block["opcode"]:
                       print(block["opcode"])

                    # --------------------------------
            
            # 変数やリストのブロックが入力らんに埋め込んである場合も正しくカウントする

            for global_variable in global_variables:
                if global_variable in json.dumps(block["inputs"]):
                    counter += 1

            for local_variable in local_variables:
                if local_variable in json.dumps(block["inputs"]):
                    counter += 1
            
            for _list_ in lists:
                if _list_ in json.dumps(block["inputs"]):
                    counter += 1
            
            
    
        print(counter)
        
            
            
            









print(count_blocks("508681860"))