import redis
import sys
import json
import time
import logging

class DataPuller:

    PULLER_KEY = 'puller::count'

    def __init__(self, h:str):
        logging.info('Connecting %s' % h)                
        self.rcli = redis.Redis(host=h, port=6379, db=1)
        self.id = -1
        self.rcli.set(self.PULLER_KEY, 0) # shouldn't be required 


    def getId(self):
        if self.id < 0:
            n_puller = self.rcli.incr(self.PULLER_KEY)
            self.id = int(n_puller)-1
        return self.id


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
                return
            time.sleep(0.125)

    def set_ready(self):
        ready_key = self.get_ready_key(self.getId())
        logging.info('%s ready' % ready_key)
        self.rcli.set(ready_key, 1)

    def is_ready(self):
        ready_key = self.get_ready_key(self.getId())
        rdy = self.rcli.get(ready_key)
        if rdy is not None and int(rdy) == 1:
            return True
        else:
            logging.warning('Pusher %d is not ready' % self.getId())

    def pull(self):
        queue_key = 'Z' + str(self.getId()) + ':' + 'dispatchqueue'
        logging.info('Starting')
        count = 0
        start = time.time()
        while self.is_ready():
            txn = self.rcli.brpop(queue_key, timeout=1)
            if txn is not None:
                payload = txn[1]
                count += 1

        logging.info('%d events' % count)
        runtime = time.time() - start
        logging.info('%f/s' % (count/runtime))
    

if __name__ == '__main__':

    if len(sys.argv) == 2:
        h = sys.argv[1]
        logging.basicConfig(level=logging.INFO)
        puller = DataPuller(h)
        time.sleep(10)
        id = puller.getId()
        logging.info('Id is %d' % id)
        # wait a bit for others to start and notify
        puller.set_ready()
        puller.await_ready()
        puller.pull()

        
    else:
        logging.error('%s hostname' % sys.argv[0])
        sys.exit(1)
