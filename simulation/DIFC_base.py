from exceptions import *

Label = set
Tag = int

tag_pool = set()

class DIFC_principle(object):
    
    def __init__(self):
        self.label_s = set()
        self.label_i = set()
        self.capadd_local = set()
        self.caprmv_local = set()

    def gen_tag(self, tag):
        global tag_pool
        if tag in tag_pool:
            raise TagAlreadyUsed()
        else:
            tag_pool |= {tag}
            self.capadd_local |= {tag}
            self.caprmv_local |= {tag}

    def classify(self, tag, obj):
        if tag in self.capadd_local:
            obj.label_s |= {tag}
        else:
            raise NoCapacity()
    
    def declassify(self, tag, obj):
        if tag in self.caprmv_local:
            obj.label_s -= {tag}
        else:
            raise NoCapacity()

    def endorse(self, tag, obj):
        if tag in self.capadd_local:
            obj.label_i |= {tag}
        else:
            raise NoCapacity()

    def dedorse(self, tag, obj):
        if tag in self.caprmv_local:
            obj.label_i -= {tag}
        else:
            raise NoCapacity()

    def transfer_capacity(self, tag, op, to):
        if op:
            if tag in self.capadd_local:
                to.capadd_local |= {tag}
            else:
                raise NoPermission()
        else:
            if tag in self.caprmv_local:
                to.caprmv_local |= {tag}
            else:
                raise NoPermission()

    def auth(self, frm, to):
        return frm.label_s <= to.label_s and to.label_i <= frm.label_i

    def create_data(self, data):
        return DIFC_data(data)

    def read_data(self, data):
        if not self.auth(data, self):
            raise NoPermission()
        return data.data

    def write_data(self, data, content):
        if not self.auth(self, data):
            raise NoPermission()
        data.data = content

class DIFC_data(object):
    
    def __init__(self, data) -> None:
        self.label_s = set()
        self.label_i = set()
        self.data = data

    def auth(self, user):
        if not self.label_s <= user.label_s and user.label_i <= self.label_i:
            raise NoPermission()

    def get(self, user):
        self.auth(user)
        return self.data

class DIFC_data_object(object):
    
    def __init__(self, label_s = set(), label_i = set(), object = []) -> None:
        self.label_s = label_s
        self.label_i = label_i
        self.object = object

    def auth(self, user):
        if not self.label_s <= user.label_s and user.label_i <= self.label_i:
            raise NoPermission()