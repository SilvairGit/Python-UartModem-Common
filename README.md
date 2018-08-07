# FW-MODULO-CI-UARTCommon

This repository contains UARTModem protocol communication-related modules (e.g. UART communication classes, message parsers).

# Installation:
- Run ```python -m pip install . --process-dependency-links```

# Usage:
This repository cannot be used directly. It is used as a dependency in the other projects.

# Modules:
- ```message_factory.py``` - module contains logic for serialization and deserialization UARTModem protocol messages.
- ```message_types.py``` - module contains types required by UARTModem protocol messages.
- ```messages.py``` - module contains classes representing UARTModem protocol messages.
- ```uart_common_classes.py``` - module contains classes related to UART communication.
