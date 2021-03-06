from DIFC_base import *

class Inode(DIFC_data_object):

    DIRECTORY = 0
    FILE = 1
    SOCKET = 2
    
    def __init__(self, name, type, label_s=set(), label_i=set(), object={}) -> None:
        super().__init__(label_s=label_s, label_i=label_i, object=object)
        self.name = str(name)
        self.type = type

    def ls(self, user):
        self.auth(user)
        if self.type == 0:
            content = [i.name+'\t'+str(i.type) for i in self.object.values()]
            for i in content:
                print(i)
        else:
            print(self.object)

    def cd(self, user, name):
        self.auth(user)
        return self.object[name]

    def newfile(self, user, name, dataObj, s=None, i=None):
        self.auth(user)
        if not s: s = user.get_label_s()
        if not i: i = user.get_label_i()
        if name not in self.object.keys():
            inode = Inode(name, 1, s, i, dataObj)
            self.object[name] = inode
        else:
            raise FileException("File already exists")

    def remove(self, user, name):
        self.auth(user)
        inode = self.object[name]
        inode.auth(user)
        del self.object[name]

    def mkdir(self, user, name, s=None, i=None):
        self.auth(user)
        if not s: s = user.get_label_s()
        if not i: i = user.get_label_i()
        if name not in self.object.keys():
            inode = Inode(name, 0, s, i, {})
            self.object[name] = inode
        else:
            raise FileException("File already exists")

    def rmdir(self, user, name):
        self.auth(user)
        inode = self.object[name]
        inode.auth(user)
        del self.object[name]

if __name__ == "__main__":
    filesys = Inode("/", 0)
    user = DIFC_principle()
    filesys.mkdir(user, "bin")
    filesys.mkdir(user, "tmp")
    filesys.mkdir(user, "usr")
    filesys.mkdir(user, "etc")
    filesys.ls(user)
    usr = filesys.cd(user, "usr")
    usr.mkdir(user, "krisya")

    
