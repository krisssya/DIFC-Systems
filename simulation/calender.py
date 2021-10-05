from DIFC_base import *

class client_thread(DIFC_principle):

    def __init__(self):
        super().__init__()
        self.calender = None
        self.memory = []

    def add_calender(self, cal):
        self.cal = cal

    def arrange_meeting(self, cal, server):
        if not self.auth(cal, server):
            raise NoPermission()
        server.memory.append(cal)

    def query_result(self):
        data = self.memory[0]
        data = self.read_data(data)
        return data

class server_thread(DIFC_principle):

    def __init__(self):
        super().__init__()
        self.memory = []

    def arrange_meeting(self):
        a = self.read_data(self.memory[0])
        b = self.read_data(self.memory[1])
        c = a & b

        d = calender(c)
        self.classify(list(self.memory[0].label_s)[0], d)
        self.endorse(list(self.memory[0].label_i)[0], d)
        self.memory[0] = d

        e = calender(c)
        self.classify(list(self.memory[1].label_s)[0], e)
        self.endorse(list(self.memory[1].label_i)[0], e)
        self.memory[1] = e


    def send_data(self, to, data):
        if not self.auth(data, to):
            raise NoPermission()
        to.memory.append(data)

class network(DIFC_data_object):

    def __init__(self):
        super().__init__()
        self.label_i = set()
        self.label_s = set()
        self.memory = []

class calender(DIFC_data):

    def __init__(self, data) -> None:
        super().__init__(data)
        self.data = data


if __name__ == "__main__":
    alice = client_thread()
    alice.gen_tag(0)
    alice.gen_tag(1)
    alice.classify(0, alice)
    alice.endorse(1, alice)
    alice_calender = calender({"1pm", "2pm", "3pm"})
    alice.classify(0, alice_calender)
    alice.endorse(1, alice_calender)

    bob = client_thread()
    bob.gen_tag(2)
    bob.gen_tag(3)
    bob.classify(2, bob)
    bob.endorse(3, bob)
    bob_calender = calender({"10pm", "12pm", "1pm"})
    bob.classify(2, bob_calender)
    bob.endorse(3, bob_calender)

    server = server_thread()

    alice.transfer_capacity(0, 1, server)
    alice.transfer_capacity(1, 1, server)
    server.classify(0, server)
    alice.arrange_meeting(alice_calender, server)


    bob.transfer_capacity(2, 1, server)
    bob.transfer_capacity(3, 1, server)
    server.classify(2, server)
    bob.arrange_meeting(bob_calender, server)

    server.arrange_meeting()

    server.send_data(alice, server.memory[0])
    server.send_data(bob, server.memory[1])

    print("alice: we meet at", alice.query_result())
    print("bob: we meet at", bob.query_result())

    eve = client_thread()
    net = network()


    try:
        server.send_data(alice_calender, net)
    except NoPermission as n:
        print("server doesn't have permission to export other's calender")

    try:
        eve.read_data(server.memory[0])
    except NoPermission as n:
        print("Eve cannot read the arrangement")

        



