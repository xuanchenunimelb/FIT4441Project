from ethereum_client import EthereumDBclient
import base58
import json

class BlockchainDBclient:
    def __init__(self,  root=None):
        self.root = ""
        self.DB = EthereumDBclient()

        if (root != None):
            self.root = root
        # if (filepath != None):
        #     self.load_from_file(filepath)


    def createSC(self, c):
        return self.DB.send_sc_to_blockchain(c)

    def callSC(self, sc_address):
        return self.DB.call_sc(sc_address)

    def callSCR(self, sc_address):
        self.DB.call_sc_r(sc_address)
        
    def resultSC(self, sc_address):
        self.DB.result_sc(sc_address)

    def load_from_file(self):
        try:
            self.root = json.load( open( "json/root.json" ) )
        except:
            print("no root file")

    def save_to_file(self):
        json.dump( self.root, open( "json/root.json", 'w' ) )

    def init_blockchain_DB(self, map):
        cost = 0
        for key, val in map.items():
            cost += self.update(key, val)
        return cost

    def getDBhash():
        return self.root

    def update(self, key, val):

        root = self.root

        if (type(val) == list):
            val_str = ",".join(base58.b58encode(str(x).encode('utf-8')).decode('utf-8') for x in val)
        else:
            val_str = base58.b58encode(val.encode('utf-8')).decode('utf-8')
        
        msg = root + "?" + key + "?" + val_str

        # print("msg: ", msg)


        tx_hash, cost = self.DB.send_msg_to_blockchain(msg)

        self.root = tx_hash

        return cost


    # to be deleted
    def query(self, key):
        vals = []
        root = self.root
        while root != None:
            decoded_msg = self.DB.get_decoded_msg(root)
            decoded_data = {}
            # for param in decoded_msg.split("?"):
            #     data = param.split('=')
            #     decoded_data[data[0]] = data[1]
            param = decoded_msg.split("?")
            decoded_data["o"] = param[0]
            decoded_data["k"] = param[1]
            decoded_data["v"] = param[2]
            if decoded_data['k'] == key:
                for val in decoded_data['v'].split(","):
                    vals.append(base58.b58decode(val).decode('utf-8'))
                return vals
            if (len(decoded_data['o']) == 0):
                root = None
            else:
                root = decoded_data['o']

            
        print("no value fund!")
        return vals
    
    
    def sign(self, proof):
        return self.DB.sign_proof(proof)

    def createSCcounter(self):
        return self.DB.init_counter_blockchain()

    def setSCcounter(self,sc_address, key, c):
        return self.DB.set_c(sc_address, key, c)

    def getSCcounter(self,sc_address, key):
        return self.DB.get_c(sc_address, key)