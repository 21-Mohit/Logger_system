import threading
from datetime import datetime
import os

class Logger:
    _instance = None
    _lock = threading.Lock()  # Lock to ensure thread safety during instance creation

    def __new__(cls, *args, **kwargs):
        with cls._lock:  # Ensure thread safety
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self,log_file = "app.log", max_size = 1024, backup_count = 5):
         if not hasattr(self, "initialized"):  # Ensure initialization happens only once
            self.log_file = log_file
            self.max_size = max_size  # Maximum size in KB
            self.backup_count = backup_count  # Number of backup files to keep
            self.file_lock = threading.Lock()
            self.initialized = True
 

    def rotate_logs(self):
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_size:
            for i in range(self.backup_count, 0, -1):  # Keep up to 5 backups
                old_file = f"{self.log_file}.{i - 1}" if i > 1 else self.log_file
                new_file = f"{self.log_file}.{i}"
                if os.path.exists(old_file):
                    os.rename(old_file, new_file)
                    
                    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        thread_name = threading.current_thread().name
        log_message = f"[{timestamp}] [{thread_name}] {level}: {message}"
        
        with self.file_lock:  # Ensure thread-safe writing
            self.rotate_logs()  # Check for rotation
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
