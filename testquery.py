from client import Client
from node import Node
import json


if __name__ == '__main__':
    client  = Client()
    sc_address = client.query("cat")
    json.dump( sc_address, open( "sc_address.json", 'w' ) )
    sc_address = json.load( open( "sc_address.json" ) )
    node = Node()
    node.query(sc_address)
    client.getqueryresult(sc_address)