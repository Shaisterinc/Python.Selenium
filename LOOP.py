import time
import subprocess

def launch_main_script():
    while True:
        try:
            # Replace with the path to your main script
            result = subprocess.run(["python3", "MAIN.PM.py"], check=True, capture_output=True, text=True)
            print(f"Main script output:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running the script: {e}")
            print(f"Error output: {e.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        time.sleep(30)  # Wait for 15 seconds before launching the script again

if __name__ == "__main__":
    launch_main_script()
