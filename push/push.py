import redis
import sys
import json
import time

SENTINEL = b'########END########'
NRUN = 1 # 2000 each

def push_redis(h:str, file:str):
    queue_key = 'Z0' + ':' + 'dispatchqueue'
    with redis.Redis(host=h, port=6379, db=1) as r:
        start_wait = True
        while start_wait:
            begin = r.brpop(queue_key, timeout=10)
            if begin is not None:
                start_wait = False
            else:
                print('Idle')
        print('Starting')
        count = 0
        start = time.time()
        for _ in range(NRUN):
            with open(file, 'r') as txnstream:
                txn = json.load(txnstream)
                for t in txn:
                    r.lpush(queue_key, json.dumps(t))
                    count += 1
                    len = r.llen(queue_key)
                    if len > 500:
                        print('%s len %d' % (queue_key, len))
                        if len > 10000:
                            print(' -- Warning Length with Trim! -- ')
                            r.ltrim(queue_key, 0, 10000)
        r.lpush(queue_key, SENTINEL)
        print('%d sent' % count)
        runtime = time.time() - start
        print('%f/s' % (count/runtime))
        sys.stdout.flush()
        
if __name__ == '__main__':

    if len(sys.argv) == 3:
        h = sys.argv[1]
        file = sys.argv[2]
        push_redis(h, file)
    else:
        print('%s hostname filename' % sys.argv[0])
        sys.exit(1)
