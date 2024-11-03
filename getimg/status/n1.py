from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NStatusChecker:

    def __init__(self):
        
        self.driver = None
        
        self.point_str = "EpisodeListList__title--lfIzU"

    def get_current_url(self, title_id):

        return f'https://comic.naver.com/webtoon/list?titleId={title_id}'

    def get_current(self, url):

        try:
            self.driver = webdriver.Chrome()
        except:
            print("Failed to load webdriver")
            return
 
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 10)
        except:
            raise Exception("Failed to get response")

        try:
            paras = driver.find_elements(By.CLASS_NAME, self.point_str)
        except:
            print("Failed to retrieve current")
            self.driver.quit()
            self.driver = None
            return

        num_list = []
        for p in paras:
            num_list.append(self.extract_number(p.text))
        
        ret = max(num_list)

        self.driver.quit()
        self.driver = None

        return ret
    
    def get_current_with_title_ids(self, title_ids:list):
        
        try:
            self.driver = webdriver.Chrome()
        except:
            print("Failed to load webdriver")
            return

        current_list = []
        for tid in title_ids:
            try:
                self.driver.get(self.get_current_url(tid))
                wait = WebDriverWait(self.driver, 10)
            except Exception as e:
                print(f"Failed to get response regarding {tid}, ({e}) ")
                current_list.append(-1)
                continue

            try:
                paras = self.driver.find_elements(By.CLASS_NAME, self.point_str)
            except:
                print(f"Failed to retrieve current regarding {tid}")
                current_list.append(-1)
                continue
            
            print(self.point_str)
            print(paras)

            num_list = []
            for p in paras:
                num_list.append(self.extract_number(p.text))

            print(num_list)
            ret = max(num_list)
            current_list.append(ret)

        self.driver.quit()
        self.driver = None
        return current_list

            
    def extract_number(self, current):
        sidx = -1
        eidx = 0
        assert isinstance(current, str), "String must be provided."
        try:
            for idx,v in enumerate(current):
                if v.isdigit() and sidx == -1:
                    sidx = idx
                
                if not v.isdigit() and idx > sidx and sidx == -1:
                    eidx = idx
        except:
            raise ValueError("Invalid current seems to be provided ")
        return int(current[sidx:eidx-1])

            





































