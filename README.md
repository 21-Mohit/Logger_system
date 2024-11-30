# **Asynchronous Logger System**

This project implements an **asynchronous logging system** in Python, designed to handle logging operations efficiently in multi-threaded environments. The logger ensures thread safety, supports log rotation based on file size, and processes log messages asynchronously using a dedicated background thread.

---

## **Features**
- **Singleton Design Pattern**: Ensures only one instance of the logger exists.
- **Thread-Safe Logging**: Allows multiple threads to log messages concurrently without conflicts.
- **Asynchronous Logging**: Decouples log writing from application logic, improving performance.
- **Log Rotation**: Automatically rotates log files when they exceed a specified size, maintaining backup logs.
- **Graceful Shutdown**: Ensures all log messages are processed before the program exits.

---

<!-- Getting Started

Prerequisites
Python 3.x installed on your machine.
Installation
Clone the repository:
bash
Copy code
git clone <repository-url>
cd <repository-name>
Install dependencies (if any; this project uses only Python standard libraries).
Usage
Code Overview
The Logger class is implemented as a thread-safe singleton with the following key functionalities:

Initialization:
Specify log file name, maximum file size (in KB), and backup count.
Log Messages:
Use the log() method to log messages with thread-safe operations.
Shutdown:
Call shutdown() to ensure all log messages are processed before exiting.
Example Code
python
Copy code
import threading
from logger import Logger  # Assuming logger.py contains the Logger class

def worker_thread(logger, thread_id):
    for i in range(5):
        logger.log(f"Log message {i} from thread {thread_id}", level="INFO")

if __name__ == "__main__":
    logger = Logger(log_file="app.log", max_size=1024, backup_count=5)

    # Create and start worker threads
    threads = []
    for i in range(3):  # Example with 3 threads
        t = threading.Thread(target=worker_thread, args=(logger, i), name=f"Thread-{i}")
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Gracefully shut down the logger
    logger.shutdown()

    print("Logging completed. Check the app.log file for output.")
Logger Workflow
Thread-Safe Singleton:

Uses __new__ with a threading lock to ensure only one instance of Logger exists.
Asynchronous Logging:

Messages are added to a thread-safe queue using the log() method.
A background thread processes and writes logs to the file.
Log Rotation:

When the log file exceeds the specified size, it rotates:
The current log file is renamed to app.log.1.
Existing backup files are shifted up (e.g., app.log.1 becomes app.log.2).
Graceful Shutdown:

The shutdown() method stops the logger thread after processing all pending log messages.
Testing
Multi-Threaded Logging
Simulate multiple threads writing log messages concurrently.
Check the log file (app.log) to verify the correctness of messages and thread names.
Log Rotation
Set a small max_size (e.g., 1 KB) to test log rotation functionality.
Ensure rotated logs (app.log.1, app.log.2, etc.) are created correctly.
Asynchronous Behavior
Observe that the main application does not block while the logger processes messages in the background.
Potential Enhancements
Dynamic Log Levels:
Allow filtering log messages based on levels (e.g., DEBUG, INFO, ERROR).
Multiple Destinations:
Extend to log messages to multiple outputs (e.g., console, remote server).
Batch Processing:
Write multiple log messages to the file in a single I/O operation to improve efficiency.
Configurable Queue Size:
Add a maximum size to the queue to prevent memory issues under heavy load.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributions
Contributions are welcome! Please open an issue or submit a pull request for enhancements or bug fixes. -->