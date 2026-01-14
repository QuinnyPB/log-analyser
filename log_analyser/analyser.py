import re
import os
import io
import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
tk.Tk().withdraw() # part of the import if you are not using other tkinter functions


#
class LogAnalyser:  
  """
  This class performs analysis of log files. If no argument is given 'filename', then a GUI window is used for file selection. Data format is [DATE, TIME, TYPE, EVENT]. Check README for more info.
  """
  def __init__(self, filename=None):
    self.output_endpoint = io.StringIO()
    self.warns, self.infos, self.errors, self.anomalies, self.total_times, self.total_dates = 0, 0, 0, 0, 0, 0
    self.dates, self.times, self.events, self.anomalous_events = dict(), dict(), dict(), dict()
    self.sorted_times, self.sorted_events = [], []
    self.filename = filename    
    
    
  def set_file(self, new_file: str):
    """
    Takes a file directory in form of string. examine_content() must be run next to process log data.
    """
    self.filename = new_file        
        
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
        
  def add_anomaly(self, line: str):
    if line not in self.anomalous_events:
      self.anomalous_events[line] = 1
    else:
      self.anomalous_events[line] += 1
      
    self.anomalies += 1  
    return
  
  def parse_line(self, line: str) -> tuple:
    """
    Parses and separates log line into corresponding components\n
    :param line: one line of log information from .txt
    :type line: str
    
    :return: date, time, type, event
    :rtype: tuple
    """
    components = line.split(" ")
    if len(components) < 4: # incomplete log, record it and disqualify
      self.add_anomaly(line)          
      return None
    date, time, type = components[:3]
    return date, time, type, " ".join(components[3:])
    
  def is_valid_date(self, date: str):
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    if not re.search(date_pattern, date):
      return False
    return True
  
  def is_valid_time(self, time: str):
    time_pattern = r"\d{2}:\d{2}:\d{2}"
    if not re.search(time_pattern, time):
      return False
    return True
  
  # if no or invalid filename is set, make user choose one
  def find_file(self):
    while True:
      self.filename = select_file()
      # user cancelled process
      if self.filename is None:
        retry = messagebox.askretrycancel("No file selected", "Do you want to try again?")
        self.filename = None
        # allow user to retry finding file or to exit program
        if not retry:
          sys.exit()          
        continue
      
        # user chose incorrect file
      if not self.filename.lower().endswith(".txt"):
        retry = messagebox.askretrycancel("Incorrect File Type", "This program currently can only work with '.txt' file types. Try again?")
        if not retry:
          sys.exit()
        continue      
      break
         
  def examine_content(self):
    """
    Initiates examination of log file content and analyses statistics\n
    """
    if not self.filename:
      self.find_file()
        
    with open(self.filename, 'r') as file:
      for line in file:
        components = self.parse_line(line)
        if not components:
          continue 
        
        date, time, type, event = "", "", "", ""
        try:
          date, time, type, event = components
        except Exception as e:
          print(f'Could not assign to variables from log: {line}, error={e}')   
        
        # check if components and date/time are valid, else record as anomaly and skip
        if not self.is_valid_date(date) or not self.is_valid_time(time) or not type or not event:
          self.add_anomaly(line)
          continue                   
          
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
            self.add_anomaly(line)
    self.sorted_times = sorted(self.times.items(), key=lambda x: x[1], reverse=True)
    self.sorted_events = sorted(self.events.items(), key=lambda x: x[1], reverse=True)
    
                  
  def print_all_stats(self):
    self.print_sums()
    self.print_sorted_times()
    self.print_sorted_events()
    
  def print_sums(self):
    # print all sums:
    print(f"\nWarnings: {self.warns},\nInfos: {self.infos},\nErrors: {self.errors},\nAnomalies: {self.anomalies}\n")
    
  def print_sorted_times(self):
    # sort the times by highest count
    print(f"Top 10 busiest times:")
    print(*self.sorted_times[:10], sep="\n", end="\n\n")

  def print_sorted_events(self):
        # all unique events
    print(f"Total unique events = {len(self.events)}")
    print(f"All event types/count:")
    print(*self.sorted_events, sep="\n", end="\n\n")    
    
  def print_anomalous_logs(self):
    print("All Anomalies:")
    for log in self.anomalous_events:
      print(f"Anomalous Log: {self.anomalous_events[log]} times, {log}", end="")
      
  def to_string_sums(self) -> str:
    return f"\nWarnings: {self.warns},\nInfos: {self.infos},\nErrors: {self.errors},\nAnomalies: {self.anomalies}\n"
      
  def to_string_sorted_events(self) -> str:
    output = f"Total unique events = {len(self.events)}\n\n"
    output += "All event types/count:\n"
    output += "\n".join(map(str, self.sorted_events)) + "\n\n"
    return output
  
  def to_string_sorted_times(self) -> str:
    output = "Top 10 busiest times:\n"
    output += "\n".join(map(str, self.sorted_times[:10])) + "\n\n"
    return output
  
  def to_string_anomalous_logs(self) -> str:
    return "All Anomalies:\n" + "".join(map(str, self.anomalous_events)) + "\n"
  
  def output_to_file(self):
    """
    Outputs data to .txt file
    """
    output_filename = self.filename[:-4]+"_results.txt"
    with open(output_filename, 'w+') as output_file:
      output_file.write(f"Summary of log file '{self.filename}'\n")
      try:
          output = self.to_string_sums()
          output += self.to_string_sorted_times()
          output += self.to_string_sorted_events()
          output += self.to_string_anomalous_logs() 
      except Exception as e:
        print(f'ERROR: Could not convert data to strings: output={output}, error={e}')

      try:
        output_file.write(output)
        messagebox.showinfo(title="Analysis complete", message=f"Results have been stored in {output_filename}")
      except Exception as e:
        print(f'ERROR: Could not write data to file! error={e}')
      

def select_file() -> str:
  allowed_file_types = (('Text Files', '*.txt'), ('All Files', '*.*'))
  choice = askopenfilename(
    title='Choose a log file', 
    initialdir=os.getcwd(), 
    filetypes=allowed_file_types
  )
  print("File: ", choice)
  return choice
  