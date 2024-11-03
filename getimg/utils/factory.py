from getimg.targets.n1 import NToken, NVendor
from getimg.status.n1 import NStatusChecker

_CLASS_MAPPING_DICT_ = {
    'ntoken': (NToken, NVendor, NStatusChecker)
}

class TokenVendorStatusClassFactory:

    @classmethod
    def get_tvs(cls, token_type):
        return _CLASS_MAPPING_DICT_.get(token_type)
            