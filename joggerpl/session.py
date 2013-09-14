"""
An abstraction over the HTML interface of the Jogger.pl control panel.
"""


import mechanize


class Session(object):
    """
    Represents a session of the control panel.
    """

    def __init__(self):
        self.browser = mechanize.Browser()

    def login(self, user, password):
        """
        Attempt to log in using the given credentials.
        """
        br = self.browser
        br.open('http://jogger.pl')
        br.select_form(nr=0)
        br.form['login_jabberid'] = user
        br.form['login_jabberpass'] = password
        br.form.find_control(id="login_session").items[0].selected = True
        br.submit()
