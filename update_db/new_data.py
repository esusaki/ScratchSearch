# 指定されたIDのプロジェクトのデータを、DBに入れるわよ

from scratch_api import get_info
from download_sb3 import download_sb3
import datetime

import sqlite3

def new_data(target_id):

    # DBにすでに存在するかたしかめ、すでに存在する場合はFalseを返す

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(f"select * from basic_info where project_id = '{target_id}'")
    result = cursor.fetchall()

    if result != []:
        return "error: data already exists"

    # apiに問い合わせて基本的な情報を得る

    info = get_info(target_id)

    if info == False:
        return "error: project not found"
    
    #print(info)
    
    # 次にsb3ファイルのダウンロード作業を行う

    downloaded_file = download_sb3(target_id)

    if downloaded_file == False:
        return "error : failed to download sb3"

    # DBに新しい行を挿入する

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    title, user_name, thumbnail_URL, loves, favorites = info["title"], info["username"], info["thumbnail"], info["loves"], info["favorites"]

    title = title.replace("'", "''")
    downloaded_file = downloaded_file.replace("'", "''")

    cursor.execute(f"insert into basic_info values ('{target_id}', '{title}', '{user_name}', '{thumbnail_URL}', '{loves}', '{favorites}', '{downloaded_file}', '{current_date}')")

    connection.commit()

    return True

with open ("update_db/target_id.txt") as f:
    links = f.read().split("\n")

for link in links:
    id = link.split("projects/")[-1].rstrip("/")
    
    print(id, new_data(id))