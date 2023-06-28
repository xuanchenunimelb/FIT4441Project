from Scheme_client import BlockchainDBclient
import time

test_map = {}

def test_build():
    DB = BlockchainDBclient()

    for i in range(0, 3):
        vals = []
        for j in range(0, 2):
            vals.append("val" + str(j) + " of key" + str(i))
        test_map['key' + str(i)] = vals

    print ("test map：", str(test_map))
    print ("Building BlockchainDB ...")
    start_time = time.time()
    total_cost = DB.init_blockchain_DB(test_map)
    stabilization_time = time.time() - start_time
    print("Stabilization time: ", stabilization_time)
    print ("Cost gas:" + str(total_cost))

    for key, vals in test_map.items():
        query_result = DB.query(key)

        try:
            assert set(query_result) == set(vals)
        except:
            print("Test failed. Query result: ", query_result)
            raise
        print("key: ", key, "vals: ", vals, "Query result: ", query_result)


    return DB

def test_update(DB):
    key = "key0"
    val = "['new val',',,,']"
    test_map[key].append(val)
    print ("test map：", str(test_map))
    print ("Updating BlockchainDB ...")
    start_time = time.time()
    total_cost = DB.update(key, val)
    stabilization_time = time.time() - start_time
    print("Stabilization time: ", stabilization_time)
    print ("Cost gas:" + str(total_cost))

    for key, vals in test_map.items():
        query_result = DB.query(key)

        try:
            assert set(query_result) == set(vals)
        except:
            print("Test failed. Query result: ", query_result)
            raise
        print("key: ", key, "vals: ", vals, "Query result: ", query_result)


    return DB

    
#     query_result = DB.query(DB.hash)
#     print(query_result)

if __name__ == '__main__':
    DB = test_build()

    DB = test_update(DB)
