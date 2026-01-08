from log_analyser.analyser import LogAnalyser
 
def main(filename):
  analyser = LogAnalyser(filename)
  print(f"main(filename={filename})")  
  analyser.read_file()  
  analyser.examine_content()
  analyser.print_stats()
  return

if __name__ == "__main__":
  # log_file = "log.txt"
  log_file = "log_large.txt"
  main(log_file)