from collections import defaultdict


class Index(object):
    def __init__(self, store=None):
        if store is None:
            store = dict()
        self.store = store
        self.deadlines = defaultdict(list)

    def update(self, event):
        """Adds an event to the index"""
        if event.state != 'expired':
            event_key = event.index_key
            self.store[event_key] = event
            self.deadlines[event.deadline].append(event_key)
            return event
        else:
            return None

    def get(self, host, service):
        """Finds an event in the index."""
        event_key = (host, service)
        return self.store.get(event_key)

    def delete(self, event):
        """Deletes any event in the index with a matching host and service.

        Returns the deleted event, if found; None, otherwise.
        """
        event_key = event.index_key
        deleted_event = self.store.pop(event_key, None)
        if deleted_event is not None:
            self.deadlines[event.deadline].remove(event_key)
        return deleted_event

    def expire(self, expiry_time=None):
        """Removes all expired events from the index.

        Returns a list of events removed from the index.
        """
        expired_events = []
        max_deadline = int(expiry_time)
        deadlines = filter(lambda(deadline): deadline <= max_deadline,
                           self.deadlines.keys())

        for deadline in deadlines:
            expired_event_keys = self.deadlines[deadline]

            for expired_event_key in expired_event_keys:
                event = self.get(*expired_event_key)
                self.store.pop(expired_event_key)
                expired_events.append(event)

            del self.deadlines[deadline]

        return expired_events

    def clear(self):
        """Resets the index"""
        self.store.clear()
        self.deadlines.clear()

    def search(self, query):
        """Returns a list of events matching a query AST."""
        raise NotImplementedError()

    def __len__(self):
        return len(self.store)

    def __nonzero__(self):
        return True
