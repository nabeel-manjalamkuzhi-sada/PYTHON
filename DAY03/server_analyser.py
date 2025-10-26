import re

# Step 1: Define the regex pattern (with named groups for easy access)
pattern = re.compile(
    r'(?P<ip>\S+)\s+'            # IP address
    r'\S+\s+\S+\s+'              # Placeholder fields
    r'\[(?P<time>.*?)\]\s+'      # Timestamp
    r'"(?P<method>\S+)\s+'       # HTTP method
    r'(?P<path>\S+)\s+'          # Path
    r'(?P<protocol>[^"]+)"\s+'   # Protocol
    r'(?P<status>\d{3})\s+'      # Status code
    r'(?P<size>\d+)'             # Response size
)

# Step 2: Create a list to store all log entries
log_entries = []

# Step 3: Read the log file and parse each line
with open("access.log", "r") as file:
    for line in file:
        match = pattern.match(line)
        if match:
            # Store in dictionary directly from groupdict()
            entry = match.groupdict()
            log_entries.append(entry)

# Step 4: Example - print all stored dictionaries
for log in log_entries:
    print(log)
    print(f"IP only: {log['ip']}")  # You can now access specific keys
    print("-" * 40)
