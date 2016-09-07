import traceback

from bs4 import BeautifulSoup, SoupStrainer
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
import re
import time
from urllib import unquote

log = CPLog(__name__)


class HdtorrentsIt(TorrentProvider, MovieProvider):

    urls = {
        'test': 'https://hdtorrents.it/',
        'login': 'https://hdtorrents.it/takelogin.php',
        'login_check': 'https://hdtorrents.it/my.php',
        'search': 'https://hdtorrents.it/browse.php?%s',
        'baseurl': 'https://hdtorrents.it/%s',
        'details': 'https://hdtorrents.it/details.php?id=%s'
    }

    # HDTorrents.it movie search categories
    # 1: Bluray Disk
    # 2: 1080 remux
    # 3: 1080 rip
    # 4: 720 rip
    # 5: Bluray 3D
    # 6: Bluray SBS 3D
    # 7: Bluray HalfSBS 3D
    # 8: Bluray OverUnder 3D
    # 9: Bluray HalfOverUnder 3D
    # 10: 1080 HEVC rip
    # 11: 720 HEVC rip
    # 12: 4K UltraHD

    cat_ids = [
        ([5, 6, 7, 8, 9], ['3d']),
        ([1], ['bd50']),
        ([3, 2, 10], ['1080p']),
        ([4, 11], ['720p']),
        ([3, 4, 10, 11], ['brrip']),
        ([12], ['2160p'])
    ]
    cat_backup_id = 4

    http_time_between_calls = 1  # Seconds
    login_fail_msg = 'Errore di entrare'
    only_tables_tags = SoupStrainer('tbody')


    def buildUrl(self, title, media, cat):
        query = tryUrlencode({
            'search': title,
            'cat': cat
         })
        return query

    def _searchOnTitle(self, title, movie, quality, results):
        for cat in self.getCatId(quality):
            # reset search categories bug
            self.getHTMLData(self.urls['search'] % time.time())

            url = self.urls['search'] % self.buildUrl(title, movie, cat)
            log.debug("Searching for quality: %s (id: %s)" % (quality['label'], cat))

            data = self.getHTMLData(url)

            if data:
                html = BeautifulSoup(data, 'html.parser', parse_only = self.only_tables_tags)

                try:
                    result_table = html.find('tbody', {"id": "highlighted"})
                    if not result_table or 'non abbiamo trovato nulla' in data.lower():
                        log.info("No torrents found for %s on HDTorrents.it", title)
                        continue

                    entries = result_table.find_all('tr')
                    for result in entries:

                        all_cells = result.find_all('td')

                        torrent = all_cells[1].find_all('a')[2]

                        torrent_id = re.sub(r'download.php\?id=([0-9]+)&name.*', r'\1', torrent['href'])

                        torrent_name = unquote(re.sub(r'download.php\?id=[0-9]+&name=(.*).torrent', r'\1', torrent['href']))

                        torrent_size = self.parseSize(all_cells[2].getText())
                        torrent_seeders = tryInt(re.sub(r'([0-9]+) \(\+[0-9]+\)\n \| ([0-9]+) \(\+[0-9]+\)\n',r'\1', all_cells[3].getText()))
                        torrent_leechers = tryInt(re.sub(r'([0-9]+) \(\+[0-9]+\)\n \| ([0-9]+) \(\+[0-9]+\)\n',r'\2', all_cells[3].getText()))
                        torrent_url = self.urls['baseurl'] % torrent['href']
                        torrent_detail_url = self.urls['details'] % torrent_id

                        result = {
                            'id': torrent_id,
                            'name': torrent_name,
                            'size': torrent_size,
                            'seeders': torrent_seeders,
                            'leechers': torrent_leechers,
                            'url': torrent_url,
                            'detail_url': torrent_detail_url,
                        }

                        log.debug("New result %s", result)
                        results.append(result)

                except:
                    log.error('Failed getting results from %s: %s', (self.getName(), traceback.format_exc()))

    def getLoginParams(self):
        return {
            'username': self.conf('username'),
            'password': self.conf('password'),
            'ssl': 'yes',
        }

    def loginSuccess(self, output):
        return 'logout.php' in output.lower()

    loginCheckSuccess = loginSuccess
