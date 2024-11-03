import os
from dataclasses import dataclass
from getimg.utils.utils import dir_check_and_create

@dataclass
class TokenSpec:
    title:str=None
    token_type:str=None
    title_id:int=None
    current:int=0
    others:str=None

    def __repr__(self):
        if self.others is None:
            return f"{self.title},{self.token_type},{self.title_id},{self.current}"
        else:
            return f"{self.title},{self.token_type},{self.title_id},{self.current},{self.others}"

class StatusDescriptor:

    split_str = "<<SPLIT>>"
    split_bin = bytes(split_str, 'utf-8')

    def __init__(self, status_file_path=None):
        status_file_path = os.environ.get("GETIMG_STATUS_PATH",status_file_path)
        if status_file_path is None:
            raise ValueError("No status path provided")
        else:
            self.status_file_path = status_file_path
            
        dir_check_and_create(os.path.split(status_file_path)[0])
        self.status_list = []
        self.load_status()

    def load_status(self):
        try:
            with open(self.status_file_path, 'rb') as f:
                status = f.readline()
        except:
            print("No status file exists")
            return
        status = status.decode('utf-8').split(self.split_str)

        for stat in status:
            
            tmp = stat.split(',')
            if len(tmp) == 4:
                self.status_list.append(
                    TokenSpec(
                        tmp[0],
                        tmp[1],
                        int(tmp[2]),
                        int(tmp[3])
                    )
                )
            elif len(tmp) > 4:
                self.status_list.append(
                    TokenSpec(
                        tmp[0],
                        tmp[1],
                        int(tmp[2]),
                        int(tmp[3]),
                        ','.join(tmp[-(len(tmp)-4):])
                    )
                )
    def insert_status(self, title, token_type, title_id, current, others=None):
        for stat in self.status_list:
            if stat.title_id == title_id: 
                print(f"title_id ({title_id}) is already on the log")
                return
        self.status_list.append(
            TokenSpec(title, token_type, title_id, current, others)
        )
    
    def update_status(self, key, current):

        if isinstance(key, int):
            for tk in self.status_list:
                
                if tk.title_id == key:
                    tk.current = current
                    
        elif isinstance(key, str):
            for tk in self.status_list:
                if tk.title == key:
                    tk.current = current

    def dump_status(self):
        if self.status_list:
            
            wrt_list = []
            for stat in self.status_list:
                wrt_list.append(bytes(stat.__repr__(), 'utf-8'))
                
            swrt_list = []
            for v in wrt_list:
                swrt_list.append(v)
                swrt_list.append(self.split_bin)
            swrt_list.pop()
            try:    
                with open(self.status_file_path, 'wb') as f:
                    f.writelines(swrt_list)
            except Exception as e:
                print(f"dump failed, ({e})")


