import threading
from datetime import datetime
import os
import queue

class Logger:
    _instance = None
    _lock = threading.Lock()  # Lock for singleton creation

    def __new__(cls, *args, **kwargs):
        with cls._lock:  # Ensure thread-safe singleton
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_file="app.log", max_size=1024, backup_count=5):
        if not hasattr(self, "initialized"):  # Initialize only once
            self.log_file = log_file
            self.max_size = max_size
            self.backup_count = backup_count
            self.log_queue = queue.Queue()  # Queue for asynchronous logging
            self.running = True  # Flag to control the logger thread
            self.logger_thread = threading.Thread(target=self._process_logs, daemon=True)
            self.logger_thread.start()  # Start the logging thread
            self.initialized = True

    def _process_logs(self):
        """Background thread for writing logs asynchronously."""
        while self.running or not self.log_queue.empty():
            try:
                log_message = self.log_queue.get(timeout=0.1)  # Get log from the queue
                self._write_log(log_message)
            except queue.Empty:
                continue  # If the queue is empty, keep looping

    def _write_log(self, log_message):
        """Handles writing logs to the file."""
        self.rotate_logs()  # Check for log rotation
        with open(self.log_file, "a") as file:
            file.write(log_message + "\n")

    def log(self, message, level="INFO"):
        """Adds a log message to the queue."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        thread_name = threading.current_thread().name
        log_message = f"[{timestamp}] [{thread_name}] {level}: {message}"
        self.log_queue.put(log_message)  # Enqueue the log message

    def rotate_logs(self):
        """Rotates the log file if it exceeds the maximum size."""
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_size:
            for i in range(self.backup_count, 0, -1):  # Rotate backups
                old_file = f"{self.log_file}.{i - 1}" if i > 1 else self.log_file
                new_file = f"{self.log_file}.{i}"
                if os.path.exists(old_file):
                    os.rename(old_file, new_file)

    def shutdown(self):
        """Stops the logger thread and flushes remaining log messages."""
        self.running = False  # Signal the logger thread to stop
        self.logger_thread.join()  # Wait for the thread to finish

def worker_thread(logger, thread_id):
    for i in range(5):
        logger.log(f"Log message {i} from thread {thread_id}", level="INFO")

if __name__ == "__main__":
    logger = Logger()  # Create the singleton logger

    # Create multiple threads
    threads = []
    for i in range(3):  # Simulate 3 threads
        t = threading.Thread(target=worker_thread, args=(logger, i), name=f"Thread-{i}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # Wait for all threads to complete

    logger.shutdown()  # Ensure all logs are written before exiting
    print("Logging completed. Check the app.log file for output.")
