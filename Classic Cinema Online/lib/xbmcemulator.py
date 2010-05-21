b#!/usr/bin/env python
#xbmcemulator

class xbmc(object):
    PLAYER_CORE_MPLAYER = 'PLAYER_CORE_MPLAYER'
    
    class Player(object):
        def __init__(self, player):
            print '**Player: %s' % player
                    
        def play(self, url, li):
            print '*play=(url=%s, li=%s)' % (url, li)
            
            
class xbmcgui(object):
    class ListItem(object):
        def __init__(self, name):
            self.name = name
            self.type = None
            self.info = None
            print '**ListItem.__init__: name=%s;' % self.name
        
        def __str__(self):
            return '*ListItem=(name=%s, type=%s, info=%s)' % (self.name,
                                                              self.type,
                                                              str(self.info))
                    
        def setInfo(self, type, info):
            self.type = type
            self.info = info
            print '**ListItem.setInfo: type=%s;\ninfo=%s' % (type, str(info))


class xbmcplugin(object):
    def addDirectoryItems(self, argv1, lis, number_lis=0):
        print '**addDirectoryItems: argv1:%s; number_lis:%s' % (argv1,
                                                                number_lis)
        for url, li, isFolder in lis:
            print '*DirectoryItem=(url=%s, li=%s, isFolder=%s)\n' % (url, li,
                                                                     isFolder)   
    def endOfDirectory(self, argv1, cacheToDisc=True):
        print '**endOfDirectory'
        
    