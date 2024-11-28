import threading
from datetime import datetime

class Logger:
    _instance = None
    _lock = threading.Lock()  # Lock to ensure thread safety during instance creation

    def __new__(cls, *args, **kwargs):
        with cls._lock:  # Ensure thread safety
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "log_file"):  # Initialize only once
            self.log_file = "app.log"
            self.file_lock = threading.Lock()  # Lock for writing to the file

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        thread_name = threading.current_thread().name
        log_message = f"[{timestamp}] [{thread_name}] {level}: {message}"
        
        with self.file_lock:  # Ensure thread-safe file writing
            with open(self.log_file, "a") as file:
                file.write(log_message + "\n")

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

    print("Logging completed. Check the app.log file for output.")
