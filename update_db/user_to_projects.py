
import requests
from bs4 import BeautifulSoup
import json



def user_to_projects(user_id):
    

    res = requests.get(f"https://scratch.mit.edu/users/{user_id}/projects/")

    source = res.text

    soup = BeautifulSoup(source, "html.parser")

    pagenation = soup.find_all(class_ = "page-links")


    paths = ["?page=1"]

    if len(pagenation) > 0:
        links = pagenation[0].find_all("a")

        for link in links:
            paths.append(link["href"])
    
    paths = set(paths)

    print(paths)

    for path in paths:

        res_each_page = requests.get(f"https://scratch.mit.edu/users/{user_id}/projects/{path}")

        soup_each_page = BeautifulSoup(res_each_page.text, "html.parser")

        projects_area =  soup_each_page.find(class_ = "media-grid")
        
        projects = projects_area.find_all(class_ = "project thumb item")

        project_ids = []

        for project in projects:
            project_id = project.find("a")["href"].split("projects/")[-1].rstrip("/")

            res_project_info = requests.get(f"https://api.scratch.mit.edu/projects/{project_id}")

            project_info = json.loads(res_project_info.text)

            loves, favorites = project_info["stats"]["loves"], project_info["stats"]["favorites"]

            if loves >= 10 and favorites >= 10:
                project_ids.append(project_id)
            
        return project_ids
        
    #print(projects)


user_name = "Chumie"
ans = user_to_projects(user_name)

with open(user_name + ".txt", mode = "w") as f:
    f.write("\n".join(ans))

# MOMO_KURA