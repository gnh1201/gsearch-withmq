#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

def main(args):
    from gsmod import search
    for url in search(args[1], stop=20):
        print(url)

    return 0

if __name__ == '__main__':
    import sys
    import os
    #sys.path.append(os.path.abspath("./gsm.py"))
    sys.exit(main(sys.argv))
