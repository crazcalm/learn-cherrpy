"""
Running this test: `py.test testing_example.py`

Note: Need to have pytest installed.
Note: I have not tried using unittest to write/run a test yet.
Note: This example if from the cherrypy docs (They only have one testing example)
"""

import pdb
import os.path

import cherrypy
from cherrypy.test import helper

CONFIG = os.path.join(os.path.dirname(__file__), "example.conf")

class Root(object):
    @cherrypy.expose
    def echo(self, message):
        cherrypy.response.headers['Content‐Type'] = 'text/html;charset=utf‐8'
        return message

class SimpleCPTest(helper.CPWebCase):
    def setup_server():
        cherrypy.tree.mount(Root(), config=CONFIG)

    setup_server = staticmethod(setup_server)

    def test_message_should_be_returned_as_is(self):
        self.getPage("/echo?message=Hello%20world")
        self.assertStatus('200 OK')

        pdb.set_trace()  # Step through and look at the `k.lower() == lowkey` line.
        self.assertHeader('Content‐Type', 'text/html;charset=utf‐8')
        self.assertBody('Hello world')

    def test_non_utf8_message_will_fail(self):
        """
        CherryPy defaults to decode the query‐string
        using UTF‐8, trying to send a query‐string with
        a different encoding will raise a 404 since
        it considers it's a different URL.
        """
        self.getPage("/echo?message=A+bient%F4t",
                     headers=[
                         ('Accept‐Charset', 'ISO‐8859‐1,utf‐8'),
                         ('Content‐Type', 'text/html;charset=ISO‐8859‐1')
                         ]
                    )
        self.assertStatus('404 Not Found')
