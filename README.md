# Traffic Alert System - CEP Assignment 3 & 4

## Overview
Event-Driven Traffic Alert System built with Python.
Course: Software Design and Architecture | BSSE 4A | Dr. Nida Adnan

## Team
- [Your Name] - Backend Core Engine (EventBus, Idempotency, Tests)
- [Partner Name] - Data & Services (Events, Envelope, Subscribers, UI)

## How to Install Dependencies
```bash
python -m pip install -r requirements.txt
```

## How to Run
```bash
python main.py
```

## How to Run Tests
```bash
python -m pytest tests -v
```

## Project Structure
```text
traffic_alert_system/
+-- core/
|   +-- events.py            # 4 required events + 5th-event demo
|   +-- event_envelope.py    # EventEnvelope 7 fields
|   +-- event_bus.py         # EventBus publish/subscribe + bounded queue
|   +-- idempotent_base.py   # Duplicate protection base
|   +-- subscribers.py       # IEventSubscriber + 4 idempotent services
+-- tests/
|   +-- test_idempotency.py
|   +-- test_event_extensibility.py
|   +-- test_full_alignment.py
+-- report/
|   +-- CEP_Report.docx
|   +-- UML_Diagram.png
+-- ui/
|   +-- dashboard.html
+-- requirements.txt
+-- main.py
```

## Design Patterns Used
- Observer Pattern (EventBus + IEventSubscriber)
- Event Envelope Pattern
- Idempotent Receiver Pattern
- Bounded Queue with priority-based eviction
