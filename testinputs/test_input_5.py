import re
from datetime import datetime

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logs = []
    
    def parse_logs(self):
        """Parse log file and extract timestamps and messages."""
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (.+)'
        with open(self.log_file, 'r') as f:
            for line in f:
                match = re.match(pattern, line)
                if match:
                    timestamp, message = match.groups()
                    self.logs.append({'timestamp': timestamp, 'message': message})
    
    def filter_by_date(self, date_str):
        """Filter logs by date."""
        return [log for log in self.logs if log['timestamp'].startswith(date_str)]

analyzer = LogAnalyzer('app.log')
