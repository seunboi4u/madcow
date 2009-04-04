#!/usr/bin/env python

from optparse import OptionParser
import sys
import os
import logging as log
from utils import find_madcow

prefix, config = find_madcow()
sys.path.insert(0, prefix)

from madcow import DEFAULTS, Madcow
from include.config import Config
from periodic import tweetprinter

defaults = os.path.join(prefix, DEFAULTS)

ANNOYING = (# boing boing
            'xenijardin',
            'doctorow',
            'BoingBoing',

            # generally irritating nonsense
            'kevinrose',
            'meTakingAShit',
            #'TheMime',  # I LIKE THE MIME
            'macworld',
            'tinybuddha',
            'sfearthquakes',
            'PiMPY3WASH',
            'cracked',

            # star wars rp'ers
            'JeanLuc_Picard',
            'LtWorf',
            'wesley_crusher',
            '_Data',
            'Will_Riker',
            'DeannaTroi',
            'Geordi_La_Forge',
            'BeverlyHCrusher',
            'Chief_OBrien',
            'LwaxanaTroi')

def main():
    # dest metavar default action type nargs const choices callback help
    # store[_(const|true|false) append[_const] count callback
    # string int long float complex choice
    optparse = OptionParser()
    optparse.add_option('-a', '--add-annoying', dest='action',
                        default=None, action='store_const', const='add',
                        help='add annoying people')
    optparse.add_option('-d', '--del-annoying', dest='action',
                        action='store_const', const='del',
                        help='delete annoying people')
    optparse.add_option('-l', '--list', dest='action', action='store_const',
                        const='list', help='list friends')
    optparse.add_option('-f', '--friend', metavar='NAME', help='add friend')
    opts, args = optparse.parse_args()

    log.root.setLevel(log.ERROR)
    api = tweetprinter.Main(Madcow(Config(config, defaults), prefix)).api
    friends = api.GetFriends()

    if opts.friend:
        print 'adding %s' % opts.friend
        api.CreateFriendship(opts.friend)

    if not opts.action:
        if opts.friend:
            return 0
        optparse.print_help()
        return 1


    if opts.action == 'list':
        for friend in friends:
            print friend.GetScreenName()

    elif opts.action == 'del':
        for friend in friends:
            name = friend.GetScreenName()
            if name in ANNOYING:
                print 'removing: %s' % name
                api.DestroyFriendship(name)

    elif opts.action == 'add':
        names = [friend.GetScreenName() for friend in friends]
        for name in ANNOYING:
            if name not in names:
                print 'adding: %s' % name
                api.CreateFriendship(name)

    return 0

if __name__ == '__main__':
    sys.exit(main())