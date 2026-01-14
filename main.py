from log_analyser.analyser import *
import typer

def main(input_file: str):
  # analyser = LogAnalyser()
  # analyser.examine_content()
  # analyser.print_all_stats()
  # analyser.print_anomalous_logs()
  # analyser.output_to_file()
  print(f"Hello {input_file}")

if __name__ == "__main__":
  typer.run(main())