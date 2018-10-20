"""
Cherrypy - Plugin Example

Note: This example uses cherrypy's builtin pub/sub system.
Run: python3 plugin_example.py
In browser, go to `http://localhost:8089/publish_example?data="Plugin works"`
"""

import os.path

import cherrypy
from cherrypy.process import plugins

CONFIG = os.path.join(os.path.dirname(__file__), "example.conf")

class ExamplePlugin(plugins.SimplePlugin):
    """
    ExamplePlugin: An example of how to create a plugin.
    """
    def __init__(self, bus, msg):
        """
        Init takes in the cherrypy.engine, which is their bus, and
        an example parameter (msg).
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.prop = msg

    def start(self):
        """
        Start: A required method needed to start your plugin
        """
        self.bus.log('Starting up the plugin')
        self.bus.subscribe("example1", self.callback)

    def stop(self):
        """
        Stop: A required method needed to stop your plugin
        """
        self.bus.log('Stopping the plugin')
        self.bus.unsubscribe("example1", self.callback)

    def callback(self, entity):
        """
        callback: The method that is called when something
        is published on the "example1" channel.

        entity: is an example of how the publisher can pass
        a variable to the subscriber.
        """
        self.bus.log(self.prop + ": " + entity)
        print(self.prop + ": " + entity)


class ExampleSubscriber(object):
    """
    ExampleSubscriber: Example of how to publish to a channel
    """
    @cherrypy.expose
    def publish_example(self, data):
        """
        publish_example: publish_example defines the route
        `localhost:8089/publish_example?data="time to publish"`
        """
        cherrypy.engine.publish('example1', data)
        print("receiced: " + data)


ExamplePlugin(cherrypy.engine, "Example1").subscribe()
ExamplePlugin(cherrypy.engine, "Example2").subscribe()
ExamplePlugin(cherrypy.engine, "Example3").subscribe()


if __name__ == '__main__':
    cherrypy.quickstart(ExampleSubscriber(), '/', config=CONFIG)
