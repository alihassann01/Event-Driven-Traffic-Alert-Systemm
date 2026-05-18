from collections import deque


class EventBus:
    """
    Implements the Observer Pattern for publishing event envelopes to subscribers.

    The bus stays decoupled by knowing only about subscribers and envelope objects.
    It does not import event types or services, so new events and subscribers can be
    added without changing this class. It also supports a bounded queue mode for
    flood scenarios; when a queue is full, the least important queued event is
    evicted before a more important incoming event is accepted.
    """

    DEFAULT_EVENT_PRIORITIES = {
        "VehicleDetectedEvent": 1,
        "TrafficClearedEvent": 2,
        "SpeedViolationEvent": 3,
        "EmergencyVehicleEvent": 4,
        "CongestionAlertEvent": 5,
    }

    def __init__(self, max_queue_size=None, auto_flush=True, event_priorities=None):
        self._subscribers = []
        self._queues = {}
        self.max_queue_size = max_queue_size
        self.auto_flush = auto_flush
        self.event_priorities = event_priorities or self.DEFAULT_EVENT_PRIORITIES

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)
        self._queues[subscriber] = deque()

    def unsubscribe(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)
            self._queues.pop(subscriber, None)

    def publish(self, envelope):
        print(f"EventBus queued event: {envelope.event_type}")

        for subscriber in self._subscribers:
            self._enqueue(subscriber, envelope)

        if self.auto_flush:
            self.flush()

    def flush(self, subscriber=None):
        subscribers = [subscriber] if subscriber else list(self._subscribers)

        for current_subscriber in subscribers:
            queue = self._queues.get(current_subscriber)
            if queue is None:
                continue

            while queue:
                envelope = queue.popleft()
                print(f"EventBus delivering event: {envelope.event_type}")
                current_subscriber.on_event(envelope)

    def pending_count(self, subscriber):
        return len(self._queues.get(subscriber, ()))

    def _enqueue(self, subscriber, envelope):
        queue = self._queues[subscriber]

        if self.max_queue_size is None or len(queue) < self.max_queue_size:
            queue.append(envelope)
            return

        lowest_index, lowest_priority = self._least_important_queued_event(queue)
        incoming_priority = self._priority(envelope)

        if incoming_priority >= lowest_priority:
            del queue[lowest_index]
            queue.append(envelope)
        else:
            print(f"EventBus dropped low-priority event: {envelope.event_type}")

    def _least_important_queued_event(self, queue):
        lowest_index = 0
        lowest_priority = self._priority(queue[0])

        for index, queued_envelope in enumerate(queue):
            priority = self._priority(queued_envelope)
            if priority < lowest_priority:
                lowest_index = index
                lowest_priority = priority

        return lowest_index, lowest_priority

    def _priority(self, envelope):
        return self.event_priorities.get(envelope.event_type, 1)
