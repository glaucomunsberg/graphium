#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from applications.swarm.assistant.GoogleAPI import GoogleAPI

def main():

    googleAPI = GoogleAPI()
    for index in range(52):
        print index
        print 'GKey:', googleAPI.get_authorization()['g_key']
        # time.sleep(1)

if __name__ == '__main__':
    main()
