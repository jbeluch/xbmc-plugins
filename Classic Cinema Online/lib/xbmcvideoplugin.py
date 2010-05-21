#!/usr/bin/env python
from urllib import quote_plus
import urllib2

class XBMCVideoPlugin(object):
    def __init__(self, argv0, argv1, debug=None):
        if debug:
            _xbmcemulator = __import__('xbmcemulator', globals(), locals(),
                              ['xbmc', 'xbmcgui', 'xbmcplugin'])
            self.xbmc = _xbmcemulator.xbmc()
            self.xbmcgui = _xbmcemulator.xbmcgui()
            self.xbmcplugin = _xbmcemulator.xbmcplugin()
        else:
            self.xbmc = __import__('xbmc')
            self.xbmcgui = __import__('xbmcgui')
            self.xbmcplugin = __import__('xbmcplugin')
        self.argv0 = argv0
        self.argv1 = int(argv1)
        
    def add_videos(self, lis):
        _lis = [self._make_directory_item(li, False) for li in lis]
        self.xbmcplugin.addDirectoryItems(self.argv1, _lis, len(_lis))
        self.xbmcplugin.endOfDirectory(self.argv1, cacheToDisc=True)        
    
    def add_dirs(self, dirs):
        _dirs = [self._make_directory_item(dir, True) for dir in dirs]
        self.xbmcplugin.addDirectoryItems(self.argv1, _dirs, len(_dirs))
        self.xbmcplugin.endOfDirectory(self.argv1, cacheToDisc=True)

    def _make_directory_item(self, dir, isFolder=True):
        if isFolder:
            url = '%s?url=%s&mode=%s' % (self.argv0,
                                               quote_plus(dir.get('url', '')),
                                               dir.get('mode'))
        else:
            url = dir.get('url')
        li = self.xbmcgui.ListItem(dir.get('name'))
        if dir.get('info'): li.setInfo('video', dir.get('info'))
        return (url, li, isFolder)
               
    def play_video(self, url, info=None):
        li = self.xbmcgui.ListItem('Video')
        if info: li.setInfo('video', info)
        self.xbmc.Player(self.xbmc.PLAYER_CORE_MPLAYER).play(url, li)

#common functions
def download_page(url):
    f = urllib2.urlopen(url)
    page_contents = f.read()
    f.close()
    return page_contents

def parse_qs(qs):
    if len(qs) < 1: return {}
    return dict([p.split('=') for p in qs.strip('?').split('&')])    
   