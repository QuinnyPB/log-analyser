
class LogAnalyser:
  def __init__(self, filename: str):
    self.filename = filename
    self.content = []
    self.warns, self.infos, self.errors, self.anomalies, self.total_times, self.total_dates = 0, 0, 0, 0, 0, 0
    self.dates, self.times, self.events, self.anomalous_events = {}, {}, {}, {}
  
    
  def read_file(self):
    with open(self.filename, 'r') as file:
      for line in file.readlines():
        self.content.append(line)
        
        
  def add_dates(self, date: str):
    if date not in self.dates:
      self.dates[date] = 1
    else:
      self.dates[date] += 1
        
  # will record only down to the minute
  def add_times(self, time: str):
    shortened_time = time[:-2]
    if shortened_time not in self.times:
      self.times[shortened_time] = 1
    else:
      self.times[shortened_time] += 1
      
      
  def add_events(self, event: str):
    if event not in self.events:
      self.events[event] = 1
    else:
      self.events[event] += 1
        
        
  def record_anomaly(self, line: str):
    if line not in self.anomalous_events:
      self.anomalous_events[line] = 1
    else:
      self.anomalous_events[line] += 1
      
    self.anomalies += 1  
    return
  
  
  def parse_line(self, line: str) -> tuple:
    """
    Parses and separates log line into corresponding components\n
    :param self: 
    :param line: one line of log information from .txt
    :type line: str
    
    :return: date, time, type, event
    :rtype: tuple
    """
    components = line.split(" ")
    if len(components) < 4: # incomplete log, record it and disqualify
      self.record_anomaly(line)          
      return None
    # print(components)
    date, time, type = components[:3]
    return date, time, type, " ".join(components[3:])
    
  
  def examine_content(self):
    """
    Initiates examination of log file content and analyses statistics\n
    """
    for i, line in enumerate(self.content):
      components = self.parse_line(line)
      if not components:
        continue
      date, time, type, event = components      
      self.add_dates(date)
      self.add_times(time)
      self.add_events(event)      
      match type:
        case "[INFO]":
          self.infos += 1          
        case "[WARN]":
          self.warns += 1          
        case "[ERROR]":
          self.errors += 1                
        case _:
          self.anomalies += 1          


  def print_stats(self):
    print(f"\nWarnings: {self.warns},\nInfos: {self.infos},\nErrors: {self.errors},\nAnomalies: {self.anomalies}\n")
    
    
  def print_count_stats(self):
    # sort the times by highest count
    sorted_times = sorted(self.times.items(), key=lambda x: x[1], reverse=True)
    print(f"Top 10 busiest times = {sorted_times[:10]}\n")
    sorted_events = sorted(self.events.items(), key=lambda x: x[1], reverse=True)
    print(f"Unique events: {sorted_events}\n")
    print(f"Total unique events = {len(self.events)}\n")


  def assert_flags(self):
    print(self.dates)
    # print(self.times) 
    self.print_count_stats()
    assert self.infos == 704, "Incorrect Infos found"
    assert self.warns == 210, "Incorrect Warnings found"
    assert self.errors == 87, "Incorrect Errors found"
    assert self.anomalies == 0, "Incorrect Anomalies found"
    return
  
  def output_results(self):
    
    return
  