class EventBus:
    """
    Implements the Observer Pattern for publishing event envelopes to subscribers.

    The bus stays decoupled by knowing only about subscribers and envelope objects.
    It does not import event types or services, so new events and subscribers can be
    added without changing this class.
    """

    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def publish(self, envelope):
        print(f"EventBus delivering event: {envelope.event_type}")

        for subscriber in self._subscribers:
            subscriber.on_event(envelope)
