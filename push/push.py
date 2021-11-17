import redis
import sys
import json
import time

SENTINEL = b'########END########'

if __name__ == '__main__':

    if len(sys.argv) == 3:
        h = sys.argv[1]
        file = sys.argv[2]

        print('Connecting %s' % h)

        queue_key = 'Z0' + ':' + 'dispatchqueue'

        with redis.Redis(host=h, port=6379, db=1) as r:
            start_wait = True
            while start_wait:
                begin = r.blpop(queue_key, timeout=10)
                if begin is not None:
                    start_wait = False
                else:
                    print('Idle')
            print('Starting')
            for _ in range(100):
                with open(file, 'r') as txnstream:
                    txn = json.load(txnstream)
                    for t in txn:
                        r.rpush(queue_key, json.dumps(t))
                        len = r.llen(queue_key)
                        if len > 500:
                            print('%s len %d' % (queue_key, len))
                            if len > 10000:
                                print(' -- Warning Length with Trim! -- ')
                        if len > 10000:
                            r.ltrim(queue_key, 0, 10000)
            r.lpush(queue_key, SENTINEL)
    else:
        print('%s hostname filename' % sys.argv[0])
        sys.exit(1)
