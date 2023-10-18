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
import numpy as np
import random
#读取kw-file关系
f_Kw_File_Use = open('C:/D/FIT4441_Honours_Thesis/CompareModel/Kw_File_Use.txt','rb')
Kw_File_Use = pickle.load(f_Kw_File_Use)
####所有keyword列表
kw_list=[]
# print(Kw_File_Use)

# for i in range(100):
#     # addfile_kw = kw
#     addfile_ID = str(np.random.randint(1, 1000, dtype=np.int64))  # 生成添加文件ID
#     Kw_File_Use['chen100'].append(addfile_ID)
# print("add file time", end1 - start1)
# print("Kw_File_Use['chen100']",len(Kw_File_Use['chen100']))

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

# print(len(kw_list))
# print(Kw_File_Use['chen400'][1])


client = Client()
###upload

start = datetime.datetime.now()



update_cost_gas = 0

for kw in Kw_File_Use:
    # print(Kw_File_Use[kw])
    for i in range(len(Kw_File_Use[kw])):
        if i != 0:
            # print(kw, Kw_File_Use[kw][i])

            # Update with keyword and id pair
            update_cost_gas += client.update("1", kw, Kw_File_Use[kw][i])
        
    # break


end= datetime.datetime.now()
t = end - start
print('update_cost_time', t)
print('update_cost_gas', update_cost_gas)

###

search_client_cost_gas = 0
search_server_cost_gas = 0
start = datetime.datetime.now()

sc_address, search_client_cost_gas = client.query("design")
json.dump( sc_address, open( "json/sc_address.json", 'w' ) )
sc_address = json.load( open( "json/sc_address.json" ) )
node = Node()
search_server_cost_gas = node.query(sc_address)
client.getqueryresult(sc_address)

end= datetime.datetime.now()
t = end - start
print('search_and verify_design_cost_time', t)
print('search_design_client_gas', search_client_cost_gas)
print('search_design_server_gas', search_server_cost_gas)

