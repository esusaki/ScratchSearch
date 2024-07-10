# 指定されたidのプロジェクトのsb3ファイルを読み取り、ブロック数とかを返すわよ

# !!! このファイルはテスト用なのでGitHubに上げる前に消すやつだわよ !!!

import sqlite3
import shutil
import zipfile
import os
import json

def count_blocks(project_id):

    # project.jsonを解読してブロック数を返すわよ

    # ちなみにproject.jsonも普通に後でGitHubに上げる前に消すやつだわよ

    with open(f"project.json") as json_file:
        data = json.loads(json_file.read())
    
    targets = data["targets"]

    background = targets[0]

    global_variables = list(background["variables"].keys())
    lists = list(background["lists"].keys())

    exclude_blocks = ["looks_costume", "looks_backdrops" , "procedures_prototype", "sensing_keyoptions"]

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
                is_menu_option, is_included_in_prototype = False, False
                
                is_menu_option = ("menu" in block["opcode"] and block["opcode"] != "looks_costumenumbername")
                 
                if block["opcode"] == "argument_reporter_string_number":
                    if block["parent"]:
                        is_included_in_prototype =  (blocks[block["parent"]]["opcode"] == "procedures_prototype")

                if block["opcode"] not in exclude_blocks and (not is_menu_option) and (not is_included_in_prototype):
                    counter += 1

                    print(" ",block["opcode"])

                    # ---- just for test of timer ----

                    #if "clone" in block["opcode"]:
                    #   print(block["opcode"])

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