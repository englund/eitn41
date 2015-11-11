import random
import hashlib

def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True

def gen_random_prime(max_length = 1000):
    while True:
        n = random.randint(1, max_length)
        if is_prime(n):
            return n

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def euler_phi(n):
    tot, pos = 0, n - 1
    while pos > 0:
        if gcd(pos, n) == 1: tot += 1
        pos -= 1
    return tot

def gen_unique_random_primes():
    p = gen_random_prime()
    q = gen_random_prime()
    while q == p:
        q = gen_random_prime()
#    n = p * q
#    phi_n = n - (p + q - 1)
#    e = random.randint(2, phi_n - 1)
#    while gcd(e, phi_n) != 1:
#        e = random.randint(2, phi_n - 1)

    return p, q

def h(a, b = ''):
    a = hashlib.md5(str(a)).hexdigest()
    b = hashlib.md5(str(b)).hexdigest()
    ab = hashlib.md5(a + b).hexdigest()
    return int(ab, 16)

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

class Client:
    def __init__(self, p, q, identity):
        self.identity = identity
        k = 10
        n = p * q
        self.quadruples = []
        for i in xrange(0, 2 * k):
            # a, c, d, r
            s = set(random.randint(1, 1000) for _ in xrange(0, 3))
            r = random.randint(1, 1000)
            while gcd(r, n) != 1:
                 r = random.randint(1, 1000)
            s.add(r)
            self.quadruples.append(s)
        self.x = []
        self.y = []
        self.b = []
        for a, c, d, r in self.quadruples:
            xi = h(a, c)
            yi = h(a ^ self.identity, d)
            self.x.append(xi)
            self.y.append(yi)
            self.b.append(r^3 * h(xi, yi) % n)

    def creationvalues(self, r):
        return [self.quadruples[i] for i in r]

    def withdraw(self, sig, b_indexes):
        s = 1
        for i in b_indexes:
            s *= h(self.x[i], self.y[i]) ^ modinv(3, n)
        return s
            


class Bank:
    def gen_r(self, b):
        k = len(b) / 2
        r = set()
        while len(r) < k:
            i = random.randint(0, 2 * k - 1)
            if i not in r:
                r.add(i)
        return r

    def controlb(self, identity, cv, r, b, n):
        r_prim = []
        for ai, ci, di, ri in cv:
            xi = h(ai, ci)
            yi = h(ai ^ identity, di)
            r_prim.append(ri^3 * h(xi, yi) % n)
        b_prim = [b[i] for i in r]
        return b_prim == r_prim

    def blind_sig(self, b, n):
        d = modinv(3, n)
        sig = 1
        for x in b:
            sig *= x^d
        return sig % n



if __name__ == '__main__':
    p, q = gen_unique_random_primes()
    n = p * q
    alice = Client(p, q, 1337)
    bank = Bank()
    r = bank.gen_r(alice.b)
    cv = alice.creationvalues(r)
    
    # check that it is ok
    bank.controlb(alice.identity, cv, r, alice.b, n)

    b_remaining_indexes = set(i for i in xrange(0, len(r) * 2)) - r
    b_remaining = [alice.b[i] for i in b_remaining_indexes]
    sig = bank.blind_sig(b_remaining, n)
    print alice.withdraw(sig, b_remaining_indexes)
