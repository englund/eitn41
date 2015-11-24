import random
import rsa
import math

class client:
    def __init__(self,id):
        self.id = id
        self.public_key, self.private_key = rsa.newkeys(128)

    def get_pub(self):
        return self.public_key
    def decrypt(self, message):
        return rsa.decrypt(message, self.private_key)

class message:
    def __init__(self, message, sender, receiver):
        self.message = str(message)
        self.sender = sender
        self.receiver = receiver

    def prepare(self, mix):
        em = rsa.encrypt(self.message.encode('utf8'),
                self.receiver.get_pub()) + "||" + str(self.receiver.id)
        return rsa.encrypt(em, mix.get_pub())

class mix:
    def __init__(self,id):
        self.id = id
        self.public_key, self.private_key = rsa.newkeys(512)
        self.clients = dict()
        self.messages = list()

    def get_pub(self):
        return self.public_key

    def decrypt(self, message):
        m = rsa.decrypt(message, self.private_key).split('||')
        return int(m[1]), m[0]

    def get_messages(self):
        messages = dict()
        for e in self.messages:
            id, m = self.decrypt(e)
            if id not in messages:
                messages[id] = []
            messages[id].append(m)
        self.messages = []
        return messages


    def insert_client(self, client):
        self.clients[client.id] = client 

    def insert_message(self, message):
        self.messages.append(message)
        self.messages.reverse()

if __name__ == "__main__":
    N = 9
    n = 3
    mix = mix(1)

    alice = client(0)
    mix.insert_client(alice)
    bob = client(1)
    mix.insert_client(bob)
    clark = client(2)
    mix.insert_client(clark)
    dave = client(3)
    mix.insert_client(dave)
    erica = client(4)
    mix.insert_client(erica)
    frutti = client(5)
    mix.insert_client(frutti)
    george = client(6)
    mix.insert_client(george)
    hedda = client(7)
    mix.insert_client(hedda)
    ida = client(8)
    mix.insert_client(ida)

    R = []
    mix.insert_message(message('hej', alice, bob).prepare(mix))
    mix.insert_message(message('hej', alice, clark).prepare(mix))
    mix.insert_message(message('hej', clark, dave).prepare(mix))
    R1 = mix.get_messages()
    R.append(set(k for k, v in R1.iteritems()))

    mix.insert_message(message('hej', alice, clark).prepare(mix))
    mix.insert_message(message('hej', bob, erica).prepare(mix))
    mix.insert_message(message('hej', clark, dave).prepare(mix))
    R2 = mix.get_messages()
    R.append(set(k for k, v in R2.iteritems()))

    mix.insert_message(message('hej', alice, bob).prepare(mix))
    mix.insert_message(message('hej', bob, frutti).prepare(mix))
    mix.insert_message(message('hej', frutti, george).prepare(mix))
    R3 = mix.get_messages()
    R.append(set(k for k, v in R3.iteritems()))

    # learning phase
    base = set()
    Rn = R
    for _ in Rn:
        Ri = Rn.pop()
        for j, r in enumerate(Rn):
            if Ri.isdisjoint(Rn[j]):
                base.add(frozenset(Ri))
                base.add(frozenset(Rn[j]))

    # excluding phase
    m = len(base)

    attackable = math.floor(n/N) <= m
    print 'attackable:', attackable

    messages = [
        message('hej', alice, bob).prepare(mix),
        message('hej', bob, hedda).prepare(mix),
        message('hej', frutti, ida).prepare(mix),

        message('hej', alice, clark).prepare(mix),
        message('hej', bob, hedda).prepare(mix),
        message('hej', frutti, ida).prepare(mix)
    ]

    Rj_prim = [set(s) for s in base]
    partners = set()
    k = len(messages) / 3
    for _ in xrange(0, k):
        mix.insert_message(messages.pop())
        mix.insert_message(messages.pop())
        mix.insert_message(messages.pop())
        R4 = mix.get_messages()
        R_prim = set(k for k, v in R4.iteritems())

        counter = 0
        match_Rj_prim = set()
        for i, s in enumerate(Rj_prim):
            if len(R_prim & s) != 0:
                counter += 1
                match_Rj_prim_index = i

        if counter == 1:
            Rj_prim[match_Rj_prim_index] = Rj_prim[match_Rj_prim_index] & R_prim

    partners = [q.pop() for q in Rj_prim]
    print 'alice\'s partners:', partners
