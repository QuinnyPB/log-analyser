from log_analyser.analyser import *
import typer

def main():
  analyser = LogAnalyser()
  analyser.examine_content()
  analyser.print_all_stats()
  analyser.print_anomalous_logs()
  analyser.output_to_file()

if __name__ == "__main__":
  main()