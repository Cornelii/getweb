import requests
from bs4 import BeautifulSoup
import os

def get_tags(url, headers, pdict):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img", **pdict)  #alt="comic content"
    else:
        img_tags = None
        
    return img_tags


def write_img_from_url(url:str, save_path, headers={}):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
          for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    else:
        raise Exception(f'Get Failed with the url{url}')





