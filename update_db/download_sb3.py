from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

def download_sb3(project_id):

    # 指定されたidのプロジェクトのSB3ファイルをダウンロードする

    download_path =  f"{os.getcwd()}/sb3_files/{project_id}"

    os.mkdir(download_path)

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : download_path}

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options = options)

    driver.get(f"https://scratch.mit.edu/projects/{project_id}/editor/")

    is_loading = True

    time.sleep(10)

    for i in range(10):
        if "読み込み中" in driver.page_source:
            print("読み込み中...")
            time.sleep(10)
        else:
            is_loading = False
            break

    if is_loading:
        return False
    else:
        file_icon = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[1]/div[3]/img[1]")

        if len(file_icon) != 1:
            return False
        else:
            # print(f"successfully loaded: {project_id}")
                    
            file_icon[0].click()

            time.sleep(5)

            save_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div[1]/div[3]/div/ul/li[3]")

            save_button.click()

            for j in range(10):
                if len(os.listdir(download_path)) > 0:
                    break
                else:
                    time.sleep(5)

    driver.quit()

    # ダウンロードできたらファイルの名前を返す, できなかったらFalseを返す

    download_success = (len(os.listdir(download_path))==1)

    if download_success:
        downloaded_filename = os.listdir(download_path)[0]
        return downloaded_filename
    else:
        return False