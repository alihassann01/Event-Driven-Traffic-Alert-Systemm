# Traffic Alert System — CEP Assignment 3 & 4

## Overview
Event-Driven Traffic Alert System built with Python.
Course: Software Design and Architecture | BSSE 4A | Dr. Nida Adnan

## Team
- [Your Name] — Backend Core Engine (EventBus, Idempotency, Tests)
- [Partner Name] — Data & Services (Events, Envelope, Subscribers, UI)

## How to Run
```bash
python main.py
```

## How to Run Tests
```bash
pytest tests/test_idempotency.py -v
```

## Project Structure
```
traffic_alert_system/
├── core/
│   ├── events.py            # 4 event type classes
│   ├── event_envelope.py    # EventEnvelope 7 fields
│   ├── event_bus.py         # EventBus publish/subscribe
│   ├── idempotent_base.py   # Duplicate protection base
│   └── subscribers.py       # IEventSubscriber + 4 services
├── tests/
│   └── test_idempotency.py  # pytest duplicate event test
├── report/
│   └── UML_Diagram.png      # Observer Pattern UML
├── ui/
│   └── dashboard.html       # Live event feed (optional)
└── main.py                  # Entry point
```

## Design Patterns Used
- Observer Pattern (EventBus + IEventSubscriber)
- Event Envelope Pattern
- Idempotent Receiver Pattern
