import json

counters = {}

counters["cat"] = 1

counters["person"] = 2

# Serialize data into file:
json.dump( counters, open( "counter.json", 'w' ) )

# Read data from file:
data = json.load( open( "counter.json" ) )

print(data)