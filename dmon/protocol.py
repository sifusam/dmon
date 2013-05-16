import abc
import json

from event import Event


class UnsupportedProtocolError(BaseException): pass


class EventProtocol(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def read(self, _bytes):
        """
        Return an Event object.

        Parse the passed in bytes and return an Event object.
        """

    @abc.abstractmethod
    def write(self, event):
        """
        Return a serialized byte string appropriate for the wire.
        """


class JSON(EventProtocol):
    """
    A basic JSON protocol implementation.

    This class is meant to be used for debugging and development.
    """

    def read(self, _bytes):
        raw_obj = json.loads(_bytes.decode('utf-8'))
        return Event(**raw_obj)

    def write(self, event):
        ev = {k: getattr(k, event) for k in event._fields}
        return json.dumps(ev).encode('utf-8')


PROTOCOLS = {'json': JSON}


def get_protocol(name):
    try:
        return PROTOCOLS[name.lower()]
    except KeyError as e:
        raise UnsupportedProtocolError("%s is an unsupported protocol" % name)
