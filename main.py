import subprocess
import os
import sys
import time

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def run_fastboot(args):
    fastboot_path = get_resource_path("fastboot.exe")
    if not os.path.exists(fastboot_path):
        print("[ERROR] fastboot.exe missing from application files.")
        return None
    try:
        # Runs command and captures output
        result = subprocess.run([fastboot_path] + args, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        print(f"[ERROR] Execution failed: {e}")
        return None

def main():
    print("=========================================")
    print("      FASTBOOT AUTOMATION UTILITY        ")
    print("=========================================")
    print("Status: Waiting for device in Fastboot mode...\n")

    # 1. Loop until a device is detected
    while True:
        output = run_fastboot(["devices"])
        if output and output.strip():
            print(f"[FOUND] Device Connected:\n{output.strip()}\n")
            break
        time.sleep(2) # Check every 2 seconds

    # 2. Execute erasure loop
    partitions = ["frp", "config", "persist"]
    print("Starting partition wipe sequence...")
    
    for part in partitions:
        print(f" -> Erasing target block: {part}...")
        res = run_fastboot(["erase", part])
        if res:
            print(res.strip())
    
    print("\nWipe sequence complete.")

    # 3. Reboot the device
    print("Sending reboot command...")
    res = run_fastboot(["reboot"])
    if res:
        print(res.strip())

    print("\nOperation finished. Closing in 5 seconds...")
    time.sleep(5)

if __name__ == "__main__":
    main()
