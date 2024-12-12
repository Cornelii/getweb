import requests as rq
from ..targets.n1 import _DEFAULT_HEADERS


class NStatusChecker:

    def __init__(self):
        pass

    def get_test_url(self, title_id, no):
        return f"https://comic.naver.com/webtoon/detail?titleId={title_id}&no={no}"

    def _binary_search(self, a, b, title_id):

        if a >= b: return a
        if a+1 == b: 
            go_url = self.get_test_url(title_id, b)
            res = rq.get(go_url, headers=_DEFAULT_HEADERS)
            if res.url.find('list?') > 0:
                return a
            else:
                return b    
        m = int((a+b)/2)

        go_url = self.get_test_url(title_id, m)
        res = rq.get(go_url, headers=_DEFAULT_HEADERS)

        if res.url.find('list?') > 0:
            return self._binary_search(a, m-1, title_id)
        else:
            return self._binary_search(m, b, title_id)
    
    def get_current_with_title_ids(self, title_ids:list):

        current_list = []
        for tid in title_ids:
            try:
                ret = self._binary_search(0, 2048, tid)
            except:
                print(f"Failed to retrieve current regarding {tid}")
                current_list.append(-1)
                continue

            current_list.append(ret)

        return current_list



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# class NStatusChecker:

#     def __init__(self):
        
#         self.driver = None
        
#         self.point_str = "EpisodeListList__title--lfIzU"

#     def get_current_url(self, title_id):

#         return f'https://comic.naver.com/webtoon/list?titleId={title_id}'

#     def get_current(self, url):

#         try:
#             self.driver = webdriver.Chrome()
#         except:
#             print("Failed to load webdriver")
#             return
 
#         try:
#             print(f"url:{url}")
#             driver.get(url)
#             wait = WebDriverWait(driver, 10)
#         except:
#             raise Exception("Failed to get response")

#         try:
#             paras = driver.find_elements(By.CLASS_NAME, self.point_str)
#         except:
#             print("Failed to retrieve current")
#             self.driver.quit()
#             self.driver = None
#             return

#         num_list = []
#         for p in paras:
#             num_list.append(self.extract_number(p.text))
        
#         ret = max(num_list)

#         self.driver.quit()
#         self.driver = None

#         return ret
    
#     def get_current_with_title_ids(self, title_ids:list):
        
#         try:
#             self.driver = webdriver.Chrome()
#         except:
#             print("Failed to load webdriver")
#             return

#         current_list = []
#         for tid in title_ids:
#             try:
#                 self.driver.get(self.get_current_url(tid))
#                 wait = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, self.point_str)))
#             except Exception as e:
#                 print(f"Failed to get response regarding {tid}, ({e}) ")
#                 current_list.append(-1)
#                 continue

#             try:
#                 paras = self.driver.find_elements(By.CLASS_NAME, self.point_str)
#             except:
#                 print(f"Failed to retrieve current regarding {tid}")
#                 current_list.append(-1)
#                 continue

#             num_list = []
#             for p in paras:
#                 num_list.append(self.extract_number(p.text))

#             ret = max(num_list)
#             current_list.append(ret)

#         self.driver.quit()
#         self.driver = None
#         return current_list

            
#     def extract_number(self, current):
#         sidx = -1
#         eidx = 0
#         current = current.split('.')[0]
#         assert isinstance(current, str), "String must be provided."
#         try:
#             for idx,v in enumerate(current):
#                 if v.isdigit() and sidx == -1:
#                     sidx = idx
                
#                 if not v.isdigit() and idx > sidx and sidx != -1:
#                     eidx = idx
#                     break
            
#         except:
#             raise ValueError("Invalid current seems to be provided ")
        
#         if eidx == 0:
#             ret = int(current[sidx:])
#         else:
#             ret =  int(current[sidx:eidx])

#         return ret
            





































