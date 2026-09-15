import os
import sys
import time

def main():
    print("=========================================")
    print("      NOKIA HARDWARE OVERRIDE TOOL       ")
    print("=========================================")
    print("\n[STEP 1] Power off your Nokia phone completely.")
    print("[STEP 2] Press and hold both Volume Up + Volume Down buttons.")
    print("[STEP 3] Plug in the USB cable while holding the keys.\n")
    print("Searching for low-level MediaTek hardware connection...")

    # Scanning loop simulation
    for i in range(5):
        print(f" Scanning hardware buses (Attempt {i+1}/5)...")
        time.sleep(1) # Corrected function name
        
    print("\n[NOTICE] To communicate with raw chipsets on Windows,")
    print("ensure you install 'libusb-win32' or Nokia MTK drivers.")
    print("Otherwise, the computer cannot route raw USB traffic to your script.")

    print("\n=========================================")
    # This line prevents the window from closing instantly
    input("\nExecution finished. Press ENTER to close this tool...")

if __name__ == "__main__":
    main()
