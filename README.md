# REDIS Benchmarkk

## Use Redis as a FIFO Queue

1. Python client injects 500,000 messages as encoded json on REDIS key
2. Another client performs a blocking pop of each message and counts the event rate

### Hardware

Timing is performed on MacBook Pro running Docker from a Debian stable-slim base image.

#### using i7 2019 MacBook Pro (Unscientific)
#### Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz

### Caveat 

This is a 'best effort' benchmark.   The goal of this work is to produce a ballpark estimate of queue performance for Redis.  Only slight effort has been made to tune the results.

## Results

```
pusher_1  | Starting
pusher_1  | 500000 sent
pusher_1  | 2192.232956/s
puller_1  | Connecting redis
puller_1  | Starting
puller_1  | 500000 events
puller_1  | 2192.236769/s
```

Redis is limiting throughput to around 2000 messages each second


