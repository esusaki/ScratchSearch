# 指定されたIDのプロジェクトの基本的な情報を返す（タイトル、いいね数など）

import requests
import json

def get_info(project_id):

    res = requests.get(f"https://api.scratch.mit.edu/projects/{project_id}")

    res_dict = json.loads(res.text)

    if "code" in res_dict:
        if res_dict["code"] == "NotFound":
            return False
    
    else:

        title = res_dict["title"]
        loves = res_dict["stats"]["loves"]
        favorites = res_dict["stats"]["favorites"]
        username = res_dict["author"]["username"]
        thumbnail = res_dict["image"]

        return {"title": title, "loves":loves, "favorites":favorites, "username":username, "thumbnail":thumbnail}

# print(get_info("1037942542"))