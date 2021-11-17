import redis
import sys
import json
import time

if __name__ == '__main__':

    if len(sys.argv) == 2:
        h = sys.argv[1]
        print('Connecting %s' % h)        

        queue_key = 'Z0' + ':' + 'dispatchqueue'

        with redis.Redis(host=h, port=6379, db=1) as r:
            r.lpush(queue_key, b'start')
            print('Starting')
            count = 0
            start = time.time()
            is_running = True
            while is_running:
                txn = r.brpop(queue_key, timeout=1)
                if txn is not None:
                    if list(txn[1]) == list(b'########END########'):
                        is_running = False
                    else:
                        count += 1

        print('%d events' % count)
        runtime = time.time() - start
        print('%f/s' % (count/runtime))
    else:
        print('%s hostname' % sys.argv[0])
        sys.exit(1)
