#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

def main(args):
    pubname = gsconfig["pubname"]
    client = Listener(r, [pubname], False, findUrlsByKeyword)
    client.start()

    return 0

def findUrlsByKeyword(line):
   from gsmod import search

   strline = str(line)

   pubname = gsconfig["pubname"]
   pausetime = gsconfig["pause"]

   if len(strline) < 3:
      r.publish(pubname, 'NOT INVAILD_COMMAND')
      return 0

   commands = strline.split(' ')

   operator = ''
   keyword = ''

   if len(commands) > 1:
      operator = commands[0]
      keyword = commands[1]
   else:
      operator = strline

   if operator in ['NOT', 'FIN', 'KILL']:
      print "Detected command: ", operator
      return 0

   if keyword == '':
      r.publish(pubname, 'NOT KEYWORD_IS_EMPTY')
      return 0

   if operator == 'SEARCH':
      try:
         for url in search(keyword, tld='co.kr', lang='all', stop=20, pause=pausetime):
            r.publish(pubname, "FOUND " + url)

         # finish signal
         time.sleep(pausetime)
         r.publish(pubname, 'FIN')
      except Exception, e:
         print("Exception occured: " + str(e))
   elif operator == 'FOUND':
      return 0
   else:
      r.publish(pubname, 'NOT UNKNOWN_COMMAND')
      return 0

if __name__ == '__main__':
    import sys
    import os
    import time
    import redis
    from gsredis import Listener

    gsconfig = {
        "pubname": "gsearch",
        "pause": 15.0
    }

    r = redis.Redis()

    #sys.path.append(os.path.abspath("./gsmod.py"))
    #sys.path.append(os.path.abspath("./gsredis.py"))
    sys.exit(main(sys.argv))
