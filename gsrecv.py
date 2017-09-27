#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

def main(args):
    print "process ended."
    return 0

def findUrlsByKeyword(keyword):
   from gsmod import search

   if len(str(keyword)) < 3:
      r.publish(pubname, 'NOT')
      return 0

   if keyword in ['NOT', 'FIN', 'KILL']:
      print "Detected command: ", keyword
      return 0

   try:
      for url in search(keyword, tld='co.kr', lang='ko', stop=20):
         r.publish(pubname, url)
   except Exception, e:
      print("Exception occured: " + str(e))

   time.sleep(3.0) # wait 3 seconds
   r.publish(pubname, 'FIN')

if __name__ == '__main__':
    import sys
    import os
    import time
    import redis
    from gsredis import Listener

    pubname = 'gsearch'

    r = redis.Redis()
    client = Listener(r, [pubname], False, findUrlsByKeyword)
    client.start()

    # count of publish
    pubcnt = 0

    #sys.path.append(os.path.abspath("./gsmod.py"))
    #sys.path.append(os.path.abspath("./gsredis.py"))
    sys.exit(main(sys.argv))
