import redis
import sys
import json
import time

SENTINEL = b'########END########'

if __name__ == '__main__':

    if len(sys.argv) == 2:
        h = sys.argv[1]
        print('Connecting %s' % h)        

        queue_key = 'Z0' + ':' + 'dispatchqueue'

        with redis.Redis(host=h, port=6379, db=1) as r:
            time.sleep(10)
            r.rpush(queue_key, b'start')
            print('Starting')
            count = 0
            start = time.time()
            is_running = True
            while is_running:
                txn = r.blpop(queue_key, timeout=1)
                if txn is not None:
                    payload = txn[1]
                    if len(txn[1]) == len(SENTINEL) and list(txn[1]) == list(SENTINEL):
                        is_running = False
                    else:
                        count += 1

        print('%d events' % count)
        runtime = time.time() - start
        print('%f/s' % (count/runtime))
    else:
        print('%s hostname' % sys.argv[0])
        sys.exit(1)
