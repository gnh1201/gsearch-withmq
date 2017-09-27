import time
import redis
import threading

class Listener(threading.Thread):
    def __init__(self, r, channels, finopt, callback):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
        self.finopt = finopt
        self.callback = callback

    def work(self, item, callback):
        print item['channel'], ":", item['data']
        self.callback(item['data']) # find urls by keyword

    def run(self):
        for item in self.pubsub.listen():
            print item
            if item['data'] == "KILL" or (item['data'] == "FIN" and self.finopt == True):
                print self, "unsubscribed and finished"
                self.pubsub.unsubscribe()
                break
            else:
                self.work(item, self.callback)
            time.sleep(3)

