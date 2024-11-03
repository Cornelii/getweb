from getimg.utils.getimg import get_tags, write_img_from_url
from getimg.utils.utils import dir_check_and_create, gen_seq
from tqdm import tqdm
import os
from typing import List, Dict, Union, Any, Annotated, Literal
from dataclasses import dataclass
#from typing_extensions 

_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

@dataclass
class NToken:

    title:str=None
    title_id:int=None
    url_no:int=None
    

class NVendor:

    def __init__(self, ntoken=None, headers=None):
        self._token = ntoken
        if headers is None:
            self.headers = _DEFAULT_HEADERS
        else:
            self.headers = headers
        self.pdict = {
            "alt" : "comic content"
        }
        self._COMMON_PATH_NAME = os.environ.get("GETWEB_DOWN_PATH",".")

    def set_title(self, title):
        self.title = title

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token
    
    def get_url(self, title_id, no):
        return f"https://comic.naver.com/webtoon/detail?titleId={title_id}&no={no}"

    def __call__(self, *arg, **kwargs):
        titleId = kwargs.get("titleId", None)
        no = kwargs.get("no", None)
        path = kwargs.get("path",self._COMMON_PATH_NAME)

        title = titleId
        if titleId is None or no is None:
            if self._token is not None:
                no = self._token.url_no
                titleId = self._token.title_id
                title = self._token.title
            else:
                raise ArgumentException("Invalid Argument or Token")
        
        url = self.get_url(titleId, no)
        seq = gen_seq(0)
        
        dir_check_and_create(os.path.join(path,title,str(no)))
        ret_str = (
            f"{title}/{no} from {url}"
        )
        print(ret_str)

        tags = get_tags(url, self.headers, self.pdict)
        
        for tag in tqdm(tags):
            a = seq.__next__()

            write_img_from_url(tag.get("src"), os.path.join(path,title,str(no),f"img{a}.jpg"), self.headers)
            #print(f'\r------------------------------------{a+1}/{len(tags)}', end="")

