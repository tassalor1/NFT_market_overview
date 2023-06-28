import os
import sys

# Run all scripts
def run_script(script_path):
    os.system(f"python {script_path}")

if __name__ == "__main__":
    scripts = ["reddit_data_fetching.py", "reddit_data_preprocessor.py", "reddit_model.py"]
    for script in scripts:
        run_script(script)
    print("Script succesfully ran")

'''
- Comment on all code
- scrape new medium
,'''