from web3 import Web3, HTTPProvider
from eth_account.messages import encode_defunct
from time import sleep
from solcx import compile_standard, install_solc
import json

ganache_url = "HTTP://127.0.0.1:7545"
account_address = "0x89356f84A449f8E58d07A3ccF3d92DA57538284c"
account_private_key = "0x7c8db4ed6bd1fc1bc7587bcb8354fe043deee25b825793c23314b5ce63357957"

w3 = Web3(Web3.HTTPProvider(ganache_url))
def to_32byte_hex(val):
    return Web3.to_hex(Web3.to_bytes(val).rjust(32, b'\0'))

class EthereumDBclient:
    def __init__(self):
        print("Ethereum network connected: ", w3.is_connected())
        print("Current block #:", w3.eth.block_number)




    def send_msg_to_blockchain(self, msg):
        encoded_msg = msg.encode()
        signed_txn = w3.eth.account.sign_transaction(dict(
            nonce=w3.eth.get_transaction_count(account_address),
            gasPrice=w3.eth.gas_price,
            gas=100000,
            to=account_address,
            value=1,
            data=encoded_msg,
          ),
          account_private_key,
        )
        tx_sent = False
        while (tx_sent == False):
            try:
                sent_tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                tx_sent = True
            except(ValueError):
                print("Too fast. Sleeping...")
                sleep(20)
        tx_data = self.await_transaction_receipt(sent_tx)
        hash = tx_data['transactionHash']
        print("Message successfully sent. Hash: ", hash.hex())
        return hash.hex(), tx_data['gasUsed']


    def await_transaction_receipt(self, tx, i=0):
        try:
            receipt = w3.eth.get_transaction_receipt(tx)
            return receipt
        except Exception as e:
            if (i > 120):
                raise Exception("Transaction was not confirmed after time limit.")
            sleep(1)
            if (i % 20 == 0):
                print("Waited " + str(i) + " seconds for tx to confirm...")
                print(e)
            return self.await_transaction_receipt(tx, i+1)

    def get_decoded_msg(self, hash):
        tx_data = w3.eth.get_transaction(hash)
    
        input = tx_data['input']

        if (input[:2] != '0x'):
            raise Exception("Invalid hex string found in transaction")

        decoded_data = bytes.fromhex(input[2:]).decode('utf-8')
        
        return decoded_data

    def sign_proof(self, proof):
        msg = Web3.solidity_keccak(['string'], [proof])
        message = encode_defunct(hexstr=msg.hex())
        # message = encode_defunct(text=proof)
        signed_message = w3.eth.account.sign_message(message, private_key=account_private_key)
        return_val = {}
        ec_recover_args = {}
        ec_recover_args["msghash"] = Web3.to_hex(signed_message.messageHash)
        ec_recover_args["v"] = signed_message.v
        ec_recover_args["r"] = to_32byte_hex(signed_message.r)
        ec_recover_args["s"] = to_32byte_hex(signed_message.s)
        return_val["message"] = message
        return_val["signed_message"] = ec_recover_args
        return return_val
    
    def send_sc_to_blockchain(self, c):
        with open("query.sol", "r") as file:
            query_sc_file = file.read()

        install_solc("0.8.17")

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"Query.sol": {"content": query_sc_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": [
                                "abi",
                                "metadata",
                                "evm.bytecode",
                                "evm.bytecode.sourceMap",
                            ]  # output needed to interact with and deploy contract
                        }
                    }
                },
            },
            solc_version="0.8.17",
        )

        with open("compiler_output.json", "w") as file:
            json.dump(compiled_sol, file)

        # get bytecode
        bytecode = compiled_sol["contracts"]["Query.sol"]["Query"]["evm"][
            "bytecode"
        ]["object"]

        # get abi
        abi = json.loads(
            compiled_sol["contracts"]["Query.sol"]["Query"]["metadata"]
        )["output"]["abi"]

        # Create the contract in Python
        Query = w3.eth.contract(abi=abi, bytecode=bytecode)
        # Get the latest transaction
        nonce = w3.eth.get_transaction_count(account_address)
        # build transaction
        transaction = Query.constructor(c).build_transaction(
            {"chainId": w3.eth.chain_id, "gasPrice": w3.eth.gas_price, "from": account_address, "nonce": nonce}
        )
        # Sign the transaction
        sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=account_private_key)
        print("Deploying Contract!")
        # Send the transaction
        transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
        # Wait for the transaction to be mined, and get the transaction receipt
        print("Waiting for transaction to finish...")
        transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
        print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

        # query = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)
        # store_contact = query.functions.addContact(
        #     "name", "+2348112398610"
        # ).buildTransaction({"chainId": chain_id, "from": account_address, "gasPrice": w3.eth.gas_price, "nonce": nonce + 1})

        # # Sign the transaction
        # sign_store_contact = w3.eth.account.sign_transaction(
        #     store_contact, private_key=account_private_key
        # )
        # # Send the transaction
        # send_store_contact = w3.eth.send_raw_transaction(sign_store_contact.rawTransaction)

        # transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

        # print(query.functions.retrieve().call())

        return transaction_receipt.contractAddress

    def call_sc(self, sc_address):
        try:
            compiled_sol = json.load( open( "compiler_output.json" ) )
        except:
            print("no compiler_output file")

        # get abi
        abi = json.loads(
            compiled_sol["contracts"]["Query.sol"]["Query"]["metadata"]
        )["output"]["abi"]

        # Create the contract in Python
        query = w3.eth.contract(address=sc_address, abi=abi)

        print(query.functions.get_c().call())
