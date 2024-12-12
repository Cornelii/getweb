# click cli
import click
from getimg.utils.factory import TokenVendorStatusClassFactory
from getimg.status.status import StatusDescriptor


@click.group()
def itask():
    pass

@itask.command()
@click.option('-t', '--title-id', default='_', help="Sync only for given title id")
def sync(title_id):

    sd = StatusDescriptor()
    
    if title_id == '_':
        # preprocessing along with token type
        # sort by token_type
        token_title_dict = {}
        for st in sd.status_list:
            if token_title_dict.get(st.token_type, None) is None:
                token_title_dict[st.token_type] = [st.title_id]
            else:
                token_title_dict[st.token_type].append(st.title_id)

        for token_type, title_id_list in token_title_dict.items():

            Token, Vendor, Status_checker = TokenVendorStatusClassFactory.get_tvs(token_type)

            current_list = Status_checker().get_current_with_title_ids(title_id_list)
            tid_cur_dict = {k:v for k, v in zip(title_id_list, current_list)}
            
            vendor = Vendor()
            for st in sd.status_list:
                print(f"{st.title} synchronizing")
                until = tid_cur_dict.get(st.title_id,-1)
                print(f"Found version: {until}")
                if until == -1: continue
                if st.current == until: continue
                if st.current < until:
                    
                    for i in range(st.current+1, until+1):
                        vendor.token = Token(st.title, st.title_id, i)
                        vendor()
                        sd.update_status(st.title_id, i)
            sd.dump_status()
    else:
        raise NotImplemented("TODO")
        
    pass

@itask.command()
@click.argument('title')
@click.argument('title_id')
@click.argument('token_type')
@click.option('-s','--with-sync', is_flag=False, help="add and sync as well")
def add(title, title_id, token_type, with_sync):
    sd = StatusDescriptor()
    title_id = int(title_id)
    sd.insert_status(title, token_type, title_id, 0)
    sd.dump_status()
    

@itask.command()
def ls():
    sd = StatusDescriptor()
    for st in sd.status_list:
        print(st)

if __name__ == "__main__":
    itask()