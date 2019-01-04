#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assistant.GoogleAPI import GoogleAPI

def main():

    googleAPI = GoogleAPI()
    for index in range(6):
        print 'Gkey:', index
        print googleAPI.get_authorization_key()
        # time.sleep(1)

if __name__ == '__main__':
    main()
