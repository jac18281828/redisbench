import redis
import sys
import json
import time
import logging

NRUN = 250 # len(txndata.json) each ~ 2000

class DataPusher:

    PULLER_KEY = 'puller::count'

    def __init__(self, h:str, file:str):
        logging.info('Connecting %s' % h)                
        self.rcli = redis.Redis(host=h, port=6379, db=1)
        self.file = file
        self.id = -1
        
    def get_ready_key(self, id:int):
        return 'Z' + str(id) + ':' + 'ready'
        
    def get_puller_count(self):
        n_puller = self.rcli.get(self.PULLER_KEY)
        if n_puller:
            return int(n_puller)
        else:
            return 0

    def all_puller_ready(self, n_puller:int):
        for id in range(n_puller):
            ready_key = self.get_ready_key(id)
            value = self.rcli.get(ready_key)
            if value is not None and int(value) == 0:
                logging.debug('Puller %d not ready' % id)
                return False
        return True

    def await_ready(self):
        last_count = 0
        while True:
            n_puller = self.get_puller_count()
            if n_puller == 0 or n_puller != last_count:
                last_count = n_puller
                time.sleep(5)
                continue
            elif self.all_puller_ready(n_puller):
                logging.info('%d puller ready' % n_puller)
                return
            time.sleep(0.125)

    def close_pullers(self):
        n_puller = self.get_puller_count()
        for id in range(n_puller):
            ready_key = self.get_ready_key(id)
            self.rcli.set(ready_key, 0)

    def log_stats(self):
        logging.info('%d sent on %d puller' % (self.count, self.get_puller_count()))
        runtime = time.time() - self.start
        logging.info('%f/s' % (self.count/runtime))

    def push(self):
        n_puller = self.get_puller_count()
        logging.info('Starting push on %d apps' % n_puller)
        self.count = 0
        self.start = time.time()
        for _ in range(NRUN):            
            with open(file, 'r') as txnstream:
                txn = json.load(txnstream)
                for t in txn:
                    queue_index = self.count % n_puller
                    queue_key = 'Z' + str(queue_index) + ':' + 'dispatchqueue'
                    self.rcli.lpush(queue_key, json.dumps(t))
                    self.count += 1
                    len = self.rcli.llen(queue_key)
                    is_log_once = False
                    while len > 500:
                        if not is_log_once:
                            is_log_once = True
                            logging.warning('%s len %d' % (queue_key, len))
                        else:
                            pass
                        if len > 10000:
                            logging.error(' -- Warning Length with Trim! -- ')
                            self.rcli.ltrim(queue_key, 0, 10000)
                    if self.count % 25000 == 0:
                        self.log_stats()
        self.log_stats()

        
if __name__ == '__main__':

    if len(sys.argv) == 3:
        h = sys.argv[1]
        file = sys.argv[2]
        logging.basicConfig(level=logging.INFO)        
        pusher = DataPusher(h, file)
        time.sleep(10)
        pusher.await_ready()
        pusher.push()
        pusher.close_pullers()
    else:
        logging.error('%s hostname filename' % sys.argv[0])
        sys.exit(1)
