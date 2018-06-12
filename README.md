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
topic: ping
```

```
monitor

"flushall"

python run_worker.py consumer1
"SADD" "pingpong:consumers" "consumer1"
"BLPOP" "pingpong:consumer:consumer1" "0"

python run_worker.py consumer2
"SADD" "pingpong:consumers" "consumer2"
"BLPOP" "pingpong:consumer:consumer2" "0"

python run.py
# Get consumers list and set request
"SMEMBERS" "pingpong:consumers"
"HMSET" "pingpong:request:a8b6b442-874e-4606-9044-65c8bc257207" "data" "ping"

# Notify consumers
"RPUSH" "pingpong:consumer:consumer1" "a8b6b442-874e-4606-9044-65c8bc257207"
"HGETALL" "pingpong:request:a8b6b442-874e-4606-9044-65c8bc257207"
"HMSET" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer1" "data" "pong"
"BLPOP" "pingpong:consumer:consumer1" "0"

"RPUSH" "pingpong:consumer:consumer2" "a8b6b442-874e-4606-9044-65c8bc257207"
"HGETALL" "pingpong:request:a8b6b442-874e-4606-9044-65c8bc257207"
"HMSET" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer2" "data" "pong"
"BLPOP" "pingpong:consumer:consumer2" "0"

# Check for responses (blocking poll until all respond)
"EXISTS" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer1"
"EXISTS" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer2"

# Get responses
"HGETALL" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer1"
"HGETALL" "pingpong:response:a8b6b442-874e-4606-9044-65c8bc257207:consumer2"
```
