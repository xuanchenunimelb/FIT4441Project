from Scheme_client import BlockchainDBclient
import time

k_s = "0123456789abcdef"

class Client:
    def __init__(self):
        print("client running...")
        
        
    def test_build(map):
        DB = BlockchainDBclient()
        print ("map：", str(map))
        print ("Building BlockchainDB ...")
        start_time = time.time()
        total_cost = DB.init_blockchain_DB(map)
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


        return DB.getDBhash()

    def test_update(DBhash):
        DB =  BlockchainDBclient(DBhash)
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
