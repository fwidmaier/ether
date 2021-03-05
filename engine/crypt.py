class CFileCrypt:
    def morgue(self,data, key, f):
        v = bytearray()
        i = 0
        for d in data:
            v.append(f(d, key[i % len(key)]))
            i += 1
        return bytes(v)

    def encrypt(self,data,key):
        data = self.morgue(data,key[::-1],lambda a,b: a ^ ord(b))
        e = lambda a,b: (a + ord(b)) % 256
        return self.morgue(data,key,e)

    def decrypt(self,data,key):
        d = lambda a,b: (a - ord(b)) % 256
        data = self.morgue(data,key,d)
        data = self.morgue(data,key[::-1],lambda a,b: a ^ ord(b))
        return data
