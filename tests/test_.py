from log_analyser.analyser import LogAnalyser
from pathlib import Path

def test_log_stats():
  project_root = Path(__file__).parent.parent
  log_file = project_root / "log_large.txt"
  analyser = LogAnalyser(str(log_file))
  analyser.read_file()  
  analyser.examine_content()
  analyser.print_stats()
  analyser.print_count_stats()
  
  assert analyser.infos == 704, "Incorrect Infos found"
  assert analyser.warns == 210, "Incorrect Warnings found"
  assert analyser.errors == 87, "Incorrect Errors found"
  assert analyser.anomalies == 0, "Incorrect Anomalies found"
  
  