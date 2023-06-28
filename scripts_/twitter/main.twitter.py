import os

def run_script(script_path):
    os.system(f"python {script_path}")

if __name__ == "__main__":
    scripts = ["twitter_data_fetching.py", "twitter_data_preprocessor.py", "twitter_model.py"]
    for script in scripts:
        run_script(script)
    print("Script succesfully ran")
