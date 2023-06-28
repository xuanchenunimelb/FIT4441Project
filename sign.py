from web3 import Web3, HTTPProvider
from eth_account.messages import encode_defunct
ganache_url = "HTTP://127.0.0.1:7545"
account_private_key = "0x7c8db4ed6bd1fc1bc7587bcb8354fe043deee25b825793c23314b5ce63357957"

w3 = Web3(Web3.HTTPProvider(ganache_url))
message = encode_defunct(text="tryingtosign")
signed_message = w3.eth.account.sign_message(message, private_key=account_private_key)
print(signed_message)
address = w3.eth.account.recover_message(message, signature=signed_message.signature)
print(address)
print(message)
print(message.body.decode())

def to_32byte_hex(val):
  return Web3.to_hex(Web3.to_bytes(val).rjust(32, b'\0'))

ec_recover_args = (msghash, v, r, s) = (
  Web3.to_hex(signed_message.messageHash),
  signed_message.v,
  to_32byte_hex(signed_message.r),
  to_32byte_hex(signed_message.s),
)
print(ec_recover_args)