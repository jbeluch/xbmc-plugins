#!/usr/bin/env python
from lib.xbmcvideoplugin import XBMCVideoPlugin, download_page, parse_qs
from lib.BeautifulSoup import BeautifulSoup as BS, SoupStrainer as SS
from urlparse import urljoin
from urllib import unquote_plus
import re

class ClassicCinema(XBMCVideoPlugin):
    base_url = 'http://www.classiccinemaonline.com/1/index.php'
    
    def get_genres(self, url):
        """Return the available genres from the homepage."""
        html = download_page(url)
        ul_tags = BS(html, parseOnlyThese=SS('ul', {'class': 'menu'}))
        dirs = [{'name': a.span.string,
                 'url': urljoin(self.base_url, a['href'] + '&limit=0'),
                 'mode': '1'} for a in ul_tags.findAll('a')]
        self.add_dirs(dirs)
    
    def get_movies(self, url):
        """Return the available movies from a genre page."""
        html = download_page(url)
        parse_trs = SS('tr', {'class': re.compile('sectiontableentry')})
        tr_tags = BS(html, parseOnlyThese=parse_trs)
        dirs = [{'name': tag.td.text + '. ' + tag.a.text,
                 'url': urljoin(self.base_url, tag.a['href']),
                 'mode': '2'} for tag in tr_tags]
        self.add_dirs(dirs)
        
    def play_movie(self, url):
        """Play a movie from a given url."""
        html = download_page(url)
        
        #grab the docid in order to construct the google video url
        m = re.search('googleplayer.swf\?docid=(.+?)&', html)
        
        #visit the google video page and parse out the download link
        url = 'http://video.google.com/videoplay?docid=%s' % m.group(1)
        html = download_page(url)
        m = re.search("download_url:'(.+?)'", html)
        
        #replace escaped speical chars with actual character
        url = re.sub(r'\\x3d', '=', m.group(1))
        url = re.sub(r'\\x26', '&', url)
        self.play_video(url)
        
    def run(self, mode, url):
        """Run the plugin script for a given mode and url."""
        #'must pass default values for mode and url, mode is '0', url is ''
        mode_functions = {'0': self.get_genres,
                          '1': self.get_movies,
                          '2': self.play_movie}
        mode_functions[mode](url)
        
if __name__ == '__main__':
    # If xbmc calls the script sys will already be an imported
    # module.  If it is run outside of xbmc, sys must be imported
    try: sys
    except NameError: import sys
    
    #parse command line parameters into a dictionary
    params = parse_qs(sys.argv[2])
    
    #create new app
    app = ClassicCinema(sys.argv[0], sys.argv[1], params.get('debug'))
    
    #run the app
    app.run(params.get('mode', '0'),
            unquote_plus(params.get('url', app.base_url)))
