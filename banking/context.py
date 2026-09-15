from datetime import datetime
from pathlib import Path

class TransactionLogger:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
        self.file = open(self.filename, "a", encoding="utf-8")
        return self

    def write(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file.write(f"{timestamp} | {message}\n")

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
        return False