from ..getimg import get_tags, write_img_from_url
from ..utils import dir_check_and_create, gen_seq

_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

class N1:

    _COMMON_PATH_NAME = "."
    
    def __init__(self, headers=None, title=None):
        super().__init__()
        if headers is None:
            self.headers = _DEFAULT_HEADERS
        else:
            self.headers = headers
        self.pdict = {
            "alt" : "comic content"
        }

        self.title = None
        if title is not None:
            self.title = title
        self.no = None

    def set_title(self, title):
        self.title = title
    
    def get_url(self, title_id, no):
        return f"https://comic.naver.com/webtoon/detail?titleId={title_id}&no={no}"

    def __call__(self, *arg, **kwargs):
        titleId = kwargs.get("titleId", None)
        no = kwargs.get("no", None)
        self.no = no
        url = self.get_url(titleId, no)
        seq = gen_seq(0)
        dir_check_and_create(f'{self._COMMON_PATH_NAME}/{self.title}/{self.no}/')
        tags = get_tags(url, self.headers, self.pdict)
        for tag in tags:
            a = seq.__next__()
            write_img_from_url(tag.get("src"), f'{self._COMMON_PATH_NAME}/{self.title}/{self.no}/img{a}.jpg', self.headers)
            print(f'\r------------------------------------{a+1}/{len(tags)}', end="")
