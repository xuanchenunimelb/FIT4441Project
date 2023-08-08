# import json
# from Scheme_client import BlockchainDBclient


# from eth_account.messages import encode_defunct
# from eth_utils.curried import to_hex, to_bytes

# string = '00000op=0?id=222'
# stripped_string = string.lstrip('0')

# print(stripped_string)

# import secrets

# token2 = secrets.token_bytes(32) 

# print(token2) 
# print(len(token2))
# from web3 import Web3, HTTPProvider
# ganache_url = "HTTP://127.0.0.1:7545"
# w3 = Web3(Web3.HTTPProvider(ganache_url))
# print(w3.eth.get_balance("0x6fCe5a8549d9ee44ab8C53D2c7F6b10feFB4B772"))
import hmac
hmac.new(b'chen', digestmod='MD5').digest()