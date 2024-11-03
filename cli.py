# click cli
import click
from getimg.utils.factory import TokenVendorStatusClassFactory
from getimg.status.status import StatusDescriptor

# sync, (title_id)

# using selenium


# add (with_sync) 

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

        Token, Vendor, Status_checker = TokenVendorStatusClassFactory.get_tvs('ntoken')
        title_id_list = []
        
        for st in sd.status_list:
            title_id_list.append(st.title_id)
            

        current_list = Status_checker().get_current_with_title_ids(title_id_list)
        tid_cur_dict = {k:v for k, v in zip(title_id_list, current_list)}
        
        vendor = Vendor()
        print(f"current_list: {current_list}")
        print(f"sd.status_list: {sd.status_list}")
        for st in sd.status_list:
            until = tid_cur_dict.get(st.title_id,-1)
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
    pass

if __name__ == "__main__":
    itask()