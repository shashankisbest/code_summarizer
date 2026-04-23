from abc import ABC, abstractmethod
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"

class Task(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.status = Status.PENDING
    
    @abstractmethod
    def execute(self):
        pass
    
    def mark_complete(self):
        self.status = Status.COMPLETE
    
    def mark_failed(self):
        self.status = Status.FAILED

class DataProcessingTask(Task):
    def execute(self):
        print(f"Executing {self.name}: {self.description}")
        self.mark_complete()

task = DataProcessingTask("ETL", "Extract and load data")
task.execute()
