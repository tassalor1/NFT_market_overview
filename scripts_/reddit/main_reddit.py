import os
import sys

def run_script(script_path):
    os.system(f"python {script_path}")

if __name__ == "__main__":
    scripts = ["reddit_data_fetching.py", "reddit_data_preprocessor.py", "sentiment_analysis_model.py"]
    for script in scripts:
        run_script(script)
