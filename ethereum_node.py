from web3 import Web3, HTTPProvider
from time import sleep
import json

ganache_url = "HTTP://127.0.0.1:7545"
# account_address = "0x89356f84A449f8E58d07A3ccF3d92DA57538284c"
node_account_address = "0x02082a62441bC43aeb23350a570929486Ea14594"

w3 = Web3(Web3.HTTPProvider(ganache_url))

def to_32byte_hex(val):
    return w3.to_bytes(val).rjust(32, b'\0')

class EthereumDBnode:
    def __init__(self):
        print("Ethereum network connected: ", w3.is_connected())
        print("Current block #:", w3.eth.block_number)

    def get_decoded_msg(self, hash):
        tx_data = w3.eth.get_transaction(hash)
    
        input = tx_data['input']

        if (input[:2] != '0x'):
            raise Exception("Invalid hex string found in transaction")

        decoded_data = bytes.fromhex(input[2:]).decode('utf-8')
        
        return decoded_data

    def send_to_sc(self, sc_address, ops, ids, vs, rs, ss):
        try:
            compiled_sol = json.load( open( "json/compiler_output.json" ) )
        except:
            print("no compiler_output file")

        # get abi
        abi = json.loads(
            compiled_sol["contracts"]["Query.sol"]["Query"]["metadata"]
        )["output"]["abi"]

        # Create the contract in Python
        query = w3.eth.contract(address=sc_address, abi=abi)

        # print("ops:", ops)
        # print("ids:", ids)
        # print("vs:", vs)
        # print("rs:", rs)
        # print("ss:", ss)


        # ops = [int(num).to_bytes(32, byteorder='big') for num in ops]

        # ids = [int(num).to_bytes(32, byteorder='big') for num in ids]

        rs = [bytes.fromhex(rs_string[2:]) for rs_string in rs]

        ss = [bytes.fromhex(ss_string[2:]) for ss_string in ss]

        
        # print("ops:", ops)
        # print("ids:", ids)
        # print("vs:", vs)
        # print("rs:", rs)
        # print("ss:", ss)
        print("Sending transaction to upload_result()\n")
        tx_hash = query.functions.upload_result(ops, ids, vs, rs, ss).transact({'from': node_account_address})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Transaction receipt mined:")
        print(receipt)

        return receipt['gasUsed']
    
    

