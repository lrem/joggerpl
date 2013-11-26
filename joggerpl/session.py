"""
An abstraction over the HTML interface of the Jogger.pl control panel.
"""


import mechanize
import re


class Session(object):
    """
    Represents a session of the control panel.
    """
    # pylint: disable=E1102
    # cause pylint fails at mechanize

    def __init__(self):
        self.browser = mechanize.Browser()

    def login(self, user, password):
        """
        Attempt to log in using the given credentials.
        """
        bro = self.browser
        bro.open('http://jogger.pl')
        bro.select_form(nr=0)
        bro.form['login_jabberid'] = user
        bro.form['login_jabberpass'] = password
        bro.form.find_control(id="login_session").items[0].selected = True
        bro.submit()
        assert '<body id="dashboard" class="logged">' \
               in bro.response().read(), \
               'Login error'

    def open(self, url):
        """
        Open the page at the specified `url`.
        """
        return self.browser.open(url)

    def follow(self, url=None, text=None):
        """
        Follow the link that matches given href url and link text,
        given as regular expressions.
        """
        rec = re.compile
        return self.browser.follow_link(url_regex=rec(url),
                                        text_regex=rec(text))

    def find_link(self, url=None, text=None):
        """
        Returns URL of the link that matches given href url and link text,
        given as regular expressions.
        """
        url = re.compile(url) if url else None
        text = re.compile(text) if text else None
        return self.browser.find_link(url_regex=url, text_regex=text).url
