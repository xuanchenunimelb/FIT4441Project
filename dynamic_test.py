from client import Client
from node import Node
import json
import numpy as np
import time
import sys
import datetime
import os
import random
import pickle

#读取kw-file关系
f_Kw_File_Use = open('C:/D/FIT4441_Honours_Thesis/CompareModel/Kw_File_Use.txt','rb')
Kw_File_Use = pickle.load(f_Kw_File_Use)
####所有keyword列表
kw_list=[]
# print(Kw_File_Use)
for kw in Kw_File_Use:
    kw_list.append(kw)

#读取file-kw关系
f_file_to_file = open('C:/D/FIT4441_Honours_Thesis/CompareModel/file_to_file.txt','rb')
file_to_file=pickle.load(f_file_to_file)
# print('file to file',file_to_file)
####所有文件的ID列表
list_file_ID=[]
for file in file_to_file:
    list_file_ID.append(file)

print(len(kw_list))
# print(Kw_File_Use['chen4000'][1])

# update_cost_gas = 0
# client = Client()
# update_cost_gas += client.update("1", "cat", "111")
# update_cost_gas += client.update("1", "cat", "1111")

# print('update_cost_gas', update_cost_gas)


# sc_address = client.query("cat")
# json.dump( sc_address, open( "json/sc_address.json", 'w' ) )
# sc_address = json.load( open( "json/sc_address.json" ) )
# node = Node()
# node.query(sc_address)
# client.getqueryresult(sc_address)