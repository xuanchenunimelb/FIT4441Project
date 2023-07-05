# import json
# from Scheme_client import BlockchainDBclient


# from eth_account.messages import encode_defunct
# from eth_utils.curried import to_hex, to_bytes

# string = '00000op=0?id=222'
# stripped_string = string.lstrip('0')

# print(stripped_string)

import secrets

token2 = secrets.token_bytes(32) 

print(token2) 
print(len(token2))