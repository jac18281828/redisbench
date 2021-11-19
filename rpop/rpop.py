import redis
import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        h = sys.argv[1]
        with redis.Redis(host=h, port=6379, db=1) as rcli:
            q = 'anyq'
    
#            rcli.lpush(q, 123)
#            rcli.lpush(q, 445)

            result = rcli.rpop(q, 45)
            print(result)
