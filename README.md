A Python CLI tool for parsing and analysing log files. Analysis reveals Sums, Total counts, Maximums, Anomalous Logs, Busiest times, Total Unique Events.

Run main.py to run program.
python main.py

To run test file run following command. Use flag '-s' for output:
python -m pytest -s

LOG INFO:
The logs are formatted as:
DATE TIME TYPE EVENT
DATE= yyyy-mm-dd
TIME= hh:MM:ss
TYPE= [INFO] OR [WARN] OR [ERROR]
EVENT= Any
