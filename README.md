A Python CLI tool for parsing and analysing log files mimicking server information.

- Counts all types of entries
- Aggregates events and timestamps
- Records and removes anomalies
- Includes pytests

To run program, run main.py
To run test file run following command. Use flag '-s' for output:
python -m pytest -s

LOG INFO:
The logs are formatted as:
DATE TIME TYPE EVENT
DATE= yyyy-mm-dd
TIME= hh:MM:ss
TYPE= [INFO] OR [WARN] OR [ERROR]
EVENT= Any
