from Scheme_client import BlockchainDBclient
# import time
import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
import base58

k_s = "0123456789abcdef".encode()
k_t = "qwertyuiopasdfgh".encode()
# k_p = "abcdef1234567890".encode()
nonce_s = "0".encode()
nonce_t = "1".encode()
# nonce_p = "2".encode()
nonce_w = "3".encode()
salt_1 = "0".encode()
salt_2 = "1".encode()

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

class Client:
    def __init__(self):
        print("client running...")
        self.DB = BlockchainDBclient()

    def query(self, w):

        # PRF 1 sw ← F1(ks, w)
        cipher = AES.new(k_s, AES.MODE_CTR, nonce = nonce_s)
        sw = cipher.encrypt(w.encode())
        # make it 128 bits
        h = MD5.new(sw)
        sw = h.digest()

        # c is the counter for the keyword
        c = 0
        try:
            counter = json.load( open( "counter.json" ) )

            # check if keyword is in counter
            if sw.hex() in counter:
                c = counter[sw.hex()]
            # if not, return
            else:
                print("no such keyword")
                return False
        
        # no counter file, create new file
        except:
            print("no counter file")
            return False



        # PRF 2 st ← F2(kt, w||c)
        cipher = AES.new(k_t, AES.MODE_CTR, nonce = nonce_t)
        concated = "w=" + w + "?c=" + str(c)

        st = cipher.encrypt(concated.encode())
        # make it 128 bits
        h = MD5.new(st)
        st = h.digest()

        # send (sw, st, c,) to the server
        # print("sw",sw)
        message = {"sw":base58.b58encode(sw).decode(),"st": base58.b58encode(st).decode(),"c": c}
        # print("message", message)
        json.dump( message, open( "query.json", 'w' ) )

        # smart contract
        return self.DB.createSC(c)

    def getqueryresult(self, sc_address):
        self.DB.callSC(sc_address)
        

        
    def update(self, op, w, id):

        # PRF 1 sw ← F1(ks, w)
        cipher = AES.new(k_s, AES.MODE_CTR, nonce = nonce_s)
        sw = cipher.encrypt(w.encode())
        # make it 128 bits
        h = MD5.new(sw)
        sw = h.digest()

        # c is the counter for the keyword
        c = 0

        try:
            counter = json.load( open( "counter.json" ) )

            # check if keyword is in counter
            if sw.hex() in counter:
                c = counter[sw.hex()]
            # if not, c = 0
        
        # no counter file, create new file
        except:
            print("no counter file")
            counters = {}
            counters[sw.hex()] = 0
            # Serialize data into file:
            json.dump( counters, open( "counter.json", 'w' ) )

        
        c = c + 1
        
        # print("sw: ", sw)
        # print("sw len: ", len(sw))

        # PRF 2 st ← F2(kt, w||c)
        cipher = AES.new(k_t, AES.MODE_CTR, nonce = nonce_t)
        concated = "w=" + w + "?c=" + str(c)
        # print(concated)
        st = cipher.encrypt(concated.encode())
        # make it 128 bits
        h = MD5.new(st)
        st = h.digest()

        # print("st: ",st)
        # print("st len: ", len(st))

        if c == 1 :
            # HASH 2 H2(sw||st)
            hash_object_2 = SHA256.new( sw + st + salt_2 )
            # print ("The hash 2 is: ",hash_object_2.digest())
            # print(len(hash_object_2.digest()))

            # e ← H2(sw||st) ⊕ 0λ||op||id
            concated = ("op=" + op + "?id=" + id).encode()
            # 0 padding
            concated = "0".encode()*(len(hash_object_2.digest()) - len(concated)) + concated
            # print("concated", concated)
            # print(len(concated))
            # bytes xor
            e = byte_xor(hash_object_2.digest(), concated)
            # print("e", e)

        else:


            # PRF 2 oldst ← F2(kt, w||c−1)
            cipher = AES.new(k_t, AES.MODE_CTR, nonce = nonce_t)
            concated = "w=" + w + "?c=" + str(c - 1)
            # print(concated)
            oldst = cipher.encrypt(concated.encode())
            # make it 128 bits
            h = MD5.new(oldst)
            oldst = h.digest()
            # print ("The oldst is: ",oldst)
            # print(len(oldst))

            # HASH 2 H2(sw||st)
            hash_object_2 = SHA256.new( sw + st + salt_2 )
            # print ("The hash 2 is: ",hash_object_2.digest())
            # print(len(hash_object_2.digest()))

            # e ← H2(sw||st) ⊕ 0λ||op||id
            concated = ("op=" + op + "?id=" + id).encode()
            # print("concated", concated)
            # print(len(concated))

            # 0 padding
            concated = oldst + "0".encode()*(len(hash_object_2.digest()) - len(concated) - len(oldst)) + concated
            # print("concated", concated)
            # print(len(concated))
            # bytes xor
            e = byte_xor(hash_object_2.digest(), concated)
            # print("e", e)
        


        # # PRF 3 kw ← F3(kp, w)
        # cipher = AES.new(k_p, AES.MODE_CTR, nonce = nonce_p)
        # # print("w:"+ w)
        # kw = cipher.encrypt(w.encode())
        # # make it 128 bits
        # h = MD5.new(kw)
        # kw = h.digest()
        # print("kw: ", kw)
        # print("kw len: ", len(kw))

        # PROOF signature
        proof = ("c=" + str(c) + "?op=" + op + "?id=" + id)
        # print("proof: ", proof.encode())

        # sign PROOF with private key
        message_data = self.DB.sign(proof)
        # print(message_data["signed_message"])
        # print(type(message_data["signed_message"]))
        # print("signed_message len: ", len(message_data["signed_message"]))

        # # Encrypt PROOF with kw
        # cipher = AES.new(kw, AES.MODE_CTR, nonce = nonce_w)
        
        # eproof = cipher.encrypt(proof.encode())
        # print("eproof: ", eproof)
        # print("eproof len: ", len(eproof))

        # cipher = AES.new(kw, AES.MODE_CTR, nonce = nonce_w)
        # pt = cipher.decrypt(eproof)
        # print("The eproof plain was: ", pt)

        # HASH 1 ut ← H1(sw||st)
        hash_object_1 = SHA256.new( sw + st + salt_1 )
        ut = hash_object_1.digest()
        # print ("The ut is: ",ut)
        # print(len(ut))
        # print(base58.b58encode(ut))


        # save to blockchain T[ut] ← (e, proof )
        
        self.DB.load_from_file()
        vals = []
        vals.append(base58.b58encode(e).decode())
        # vals.append(base58.b58encode(eproof).decode())
        vals.append(str(message_data["signed_message"]))
        # print("vals: ", vals)
        # print(base58.b58encode(ut))
        self.DB.update(base58.b58encode(ut).decode(), vals)
        self.DB.save_to_file()
        # print(self.DB.root)

        

        # store the counter to file
        
        counter = json.load( open( "counter.json" ) )
        counter[sw.hex()] = c
        json.dump( counter, open( "counter.json", 'w' ) )
        return True