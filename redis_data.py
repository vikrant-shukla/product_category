import redis

# Create a connection to the Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Specify the key you want to check
key_to_check = 'product_list'

# Use the GET method to retrieve the value associated with the key
value = redis_client.get(key_to_check)

# Check if the key exists in Redis
if value is not None:
    # If the key exists, decode the value (Redis stores data as bytes)
    decoded_value = value.decode('utf-8')
    print(f"Value for key '{key_to_check}': {decoded_value}")
else:
    print(f"Key '{key_to_check}' does not exist in Redis.")
