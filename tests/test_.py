from log_analyser.analyser import *

def test_log_stats():
  # user_input = select_file()  
  analyser = LogAnalyser()
  # analyser.set_file(user_input)  
  analyser.examine_content()
  analyser.print_all_stats()
  analyser.print_anomalous_logs()
  
  assert analyser.infos == 704, "Incorrect Infos found"
  assert analyser.warns == 210, "Incorrect Warnings found"
  assert analyser.errors == 87, "Incorrect Errors found"
  assert analyser.anomalies == 6, "Incorrect Anomalies found"
  
  