ReqResp
=======
A Request/Response protocol over redis

Protocol
========
```
# Set of consumers to received requests related to "task" topic
<topic>:consumers

# Request data
<topic>:request:<request_id>

# Request queue for that consumer
# <request_id> pushed to that queue
<topic>:<consumer_id>

# Response to the request is stored at
<topic>:response:<request_id>:<consumer_id>
```

Example:
1 producer, 2 consumers
```
monitor

"flushall"

python run_worker.py consumer1
(consumer1) "SADD" "pingpong:consumers" "consumer1"
(consumer1) "BLPOP" "pingpong:consumer:consumer1" "0"

python run_worker.py consumer2
(consumer2) "SADD" "pingpong:consumers" "consumer2"
(consumer2) "BLPOP" "pingpong:consumer:consumer2" "0"

python run.py
# Get consumers list and set request
(producer) "SMEMBERS" "pingpong:consumers"
(producer) "HMSET" "pingpong:request:a8b6b442-874e-4606-9044-65c8bc257207" "data" "ping"

# Notify consumers
(producer) "RPUSH" "pingpong:consumer:consumer1" "a8b6b442-874e-4606-9044-65c8bc257207"
(consumer1) "HGETALL" "pingpong:request:a8b6b442-874e-4606-9044-65c8bc257207"
(consumer1) "HMSET" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer1" "data" "pong"
(consumer1) "BLPOP" "pingpong:consumer:consumer1" "0"

(producer) "RPUSH" "pingpong:consumer:consumer2" "a8b6b442-874e-4606-9044-65c8bc257207"
(consumer2) "HGETALL" "pingpong:request:a8b6b442-874e-4606-9044-65c8bc257207"
(consumer2) "HMSET" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer2" "data" "pong"
(consumer2) "BLPOP" "pingpong:consumer:consumer2" "0"

# Check for responses (blocking poll until all respond)
(producer) "EXISTS" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer1"
(producer) "EXISTS" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer2"

# Get responses
(producer) "HGETALL" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer1"
(producer) "HGETALL" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer2"
```
