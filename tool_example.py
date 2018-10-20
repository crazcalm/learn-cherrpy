"""
tool_example.py:

This is an example of a how to create a tool that holds state.
"""

import time
import os.path

import cherrypy

CONFIG = os.path.join(os.path.dirname(__file__), "example.conf")

class TimingTool(cherrypy.Tool):
    """
    TimingTool: This tool times how long a request takes by starting
    a timer before the handler runs and ends the timer right after the
    request is finalized (result has been returned).
    """
    def __init__(self):
        """
        __init__: Init registers this tool with cherrypy.
        Note: self.start_timer is the callback method the cherrypy will call.
        Note: self.start_timer is being hooked to the before_handler.
        """
        cherrypy.Tool.__init__(self, 'before_handler',
            self.start_timer,
            priority=95)

    def _setup(self):
        """
        _setup: is a method that is called automatically whenever
        a tool get applied to a request.
        """
        cherrypy.Tool._setup(self)

        # This is needed to add the self.end_timer method to the
        # before_finalize (hook).
        cherrypy.request.hooks.attach('before_finalize',
                                      self.end_timer,
                                      priority=5)

    def start_timer(self):
        """
        start_timer: A method used to start the timer
        """
        cherrypy.request._time = time.time()

    def end_timer(self):
        """
        end_timer: A method used to report the time lapse or duration
        of the request.
        """
        duration = time.time() - cherrypy.request._time
        cherrypy.log("Page handler took %.4f" % duration)

cherrypy.tools.timeit = TimingTool()


class Root(object):
    """
    Root: A generic class used to create a web endpoint to use the
    TimerTool.
    """
    @cherrypy.expose
    @cherrypy.tools.timeit()
    def index(self):
        """
        index: is the localhost:8089 web route end point.
        """
        return "hello world"


if __name__ == "__main__":
    cherrypy.quickstart(Root(), config=CONFIG)