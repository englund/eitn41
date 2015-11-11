import hashlib

hashes = set()
found = 0
i = 0
while found < 10:
    m = hashlib.sha512(str(i)).hexdigest()[-10:]
    if m in hashes:
        found += 1
        print i, m
    else:
        hashes.add(m)
    i += 1

#hashes = set()
#found = 0
#i = 0
#while found < 10:
#    m = str(hash("h" + str(i)))[-10:]
#    if m in hashes:
#        found += 1
#        print i, m
#    else:
#        hashes.add(m)
#    i += 1
