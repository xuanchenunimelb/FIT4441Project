from ethereum_node import EthereumDBnode
import base58
import json


class BlockchainDBnode:
    def __init__(self,  root=None):
        self.root = ""
        self.DB = EthereumDBnode()

        if (root != None):
            self.root = root
        # if (filepath != None):
        #     self.load_from_file(filepath)

    def load_from_file(self):
        try:
            self.root = json.load( open( "json/root.json" ) )
        except:
            print("no root file")

    def save_to_file(self):
        json.dump( self.root, open( "json/root.json", 'w' ) )


    def getDBhash():
        return self.root

    
    def query(self, key):
        vals = []
        root = self.root
        decoded_msg_dict = {}
        while root != None:
            if root in decoded_msg_dict:
                decoded_msg = decoded_msg_dict[root]
            else:
                decoded_msg = self.DB.get_decoded_msg(root)
                decoded_msg_dict[root] = decoded_msg
            
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

    def sendToSC(self, sc_address, ops, ids, vs, rs, ss):
        return self.DB.send_to_sc(sc_address, ops, ids, vs, rs, ss)
        