from Scheme_node import BlockchainDBnode
# import time
import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, MD5
import base58


nonce_s = "0".encode()
nonce_t = "1".encode()
# nonce_p = "2".encode()
nonce_w = "3".encode()
salt_1 = "0".encode()
salt_2 = "1".encode()

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])



class Node:
    def __init__(self):
        print("node running...")
    
    def query(self, sc_address):
        query = {}
        try:
            query = json.load( open( "query.json" ) )

        # no counter file, create new file
        except:
            print("no query file")
        
        # print("query",query)
        c = query["c"]
        sw = base58.b58decode(query["sw"].encode())
        st = base58.b58decode(query["st"].encode())

        # print(sw)


        S = []
        P = []
        
        ops = []
        ids = []
        vs = []
        rs = []
        ss = []


        DB = BlockchainDBnode()
        DB.load_from_file()

        # get all records
        i = c
        # print("i",i)
        while (i > 0):
            # HASH 1 ut ← H1(sw||st)

            hash_object_1 = SHA256.new( sw + st + salt_1 )
            ut = hash_object_1.digest()

            # (e, signature) ← T[ut]
            query_result = DB.query(base58.b58encode(ut).decode())
            S.insert(0, query_result[1])
            e = base58.b58decode(query_result[0].encode())
            vs.insert(0, eval(query_result[1])['v'])
            rs.insert(0, eval(query_result[1])['r'])
            ss.insert(0, eval(query_result[1])['s'])

            # print("s noencode", query_result[1])
            # print("s noencode", eval(query_result[1])['s'])
            # print(len(eval(query_result[1])['s']))
            # print("s encode", eval(query_result[1])['s'].encode())
            # print(len(eval(query_result[1])['s'].encode()))
            # print("vs", vs)
            # print("rs", rs)
            # print("ss", ss)
            # print("S", S)
            # print(e)


            # HASH 2 H2(sw||st)
            hash_object_2 = SHA256.new( sw + st + salt_2 )
            # st||op||id ← e⊕ H2(sw||st)
            concated = byte_xor(hash_object_2.digest(), e)

            # print("concated: ", concated)
            st = concated[:16]
            # print("st: ", st)
            # print("concated[16:]: ", concated[16:].decode())
            opid = concated[16:].decode().lstrip('0')
            # print("here! ", opid)
            opid = opid.split("?")
            op = int(opid[0].split("=")[1])
            id = int(opid[1].split("=")[1])
            ops.insert(0, op)
            ids.insert(0, id)
            # print("ops", ops)
            # print("ids", ids)

            # print(opid)
            # print(op)
            # print(id)
            # P.insert(0, "?op=" + op + "?id=" + id)
            # print("P", P)
            i = i - 1
            # print("i",i)

            # k_t = "qwertyuiopasdfgh".encode()
            # cipher = AES.new(k_t, AES.MODE_CTR, nonce = nonce_t)
            # concated = "w=" + "cat" + "?c=" + "1"
            # print(concated)
            # oldst = cipher.encrypt(concated.encode())
            # # make it 128 bits
            # h = MD5.new(oldst)
            # oldst = h.digest()
            # print ("The oldst is: ", oldst)
        
        # TODO send to sc
        DB.sendToSC(sc_address, ops, ids, vs, rs, ss)
