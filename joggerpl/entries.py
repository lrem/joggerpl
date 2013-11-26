"""
Manipulate the entry list.
"""

import pyquery
import re
from mechanize import LinkNotFoundError

MAIN_URL = 'https://login.jogger.pl/entries/browse/'


class EntryList(object):
    """
    Apart from keeping a list of `Entry` objects,
    this allows operating the entry list page of the web interface.
    """

    def __init__(self, session):
        self.session = session
        self.entries = []
        self.update()

    def update(self):
        """
        Pull the complete entry list.
        If the need arises, this can be made lazy.
        """
        self.entries = []
        self._pull_page_rec(MAIN_URL)

    def _pull_page_rec(self, url):
        """
        Pull information from the given URL and recur for the next one.
        """
        print "Pulling", url
        res = self.session.open(url)
        pyq = pyquery.PyQuery(res.get_data())
        lev = lambda s: re.search('\\((\\d)\\)', s).group(1)
        for entry_element in pyq('div.entry'):
            enq = pyquery.PyQuery(entry_element)
            self.entries.append(Entry(enq('h3:first a').attr('href'),
                                      enq('h3:first a').text(),
                                      enq('div.body').html(),
                                      enq('.timestamp').text(),
                                      [l.text for l in
                                          enq('dt:contains(Kategorie)').
                                          next().find('li')],
                                      lev(enq('dt:contains(Poziom)')
                                          .next().text()),
                                      enq('dt:contains(Komentarze)').
                                      next().text()
                                      ))
        try:
            self._pull_page_rec(self.session.find_link(text='Starsze'))
        except LinkNotFoundError:
            print "Next page not found"


class Entry(object):
    """
    Models a single entry.
    """

    def __init__(self, url, title, body, date, categories, level, comments):
        #pylint: disable=R0913
        self.url = url
        self.title = title
        self.body = body
        self.date = date
        self.categories = categories
        self.level = level
        self.comments = comments
