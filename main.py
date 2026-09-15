import os
import sys
import time
import serial.tools.list_ports # Import serial discovery library

def find_mtk_port():
    # Scans active Windows COM ports for MediaTek hardware signatures
    ports = serial.tools.list_ports.comports()
    for port in ports:
        port_desc = port.description.lower()
        # Look for standard MediaTek chipset driver identifiers
        if "mediatek" in port_desc or "preloader" in port_desc or "mcom" in port_desc:
            return port.device
    return None

def main():
    print("=========================================")
    print("      NOKIA HARDWARE OVERRIDE TOOL       ")
    print("=========================================")
    print("\n[STEP 1] Power off your Nokia phone completely.")
    print("[STEP 2] Press and hold both Volume Up + Volume Down buttons.")
    print("[STEP 3] Plug in the USB cable while holding the keys.\n")
    print("Searching for active MediaTek hardware interface...")

    # Active monitoring loop
    device_port = None
    timeout = 30 # Scan for 30 seconds
    start_time = time.time()

    while (time.time() - start_time) < timeout:
        device_port = find_mtk_port()
        if device_port:
            print(f"\n[SUCCESS] Found device on connection interface: {device_port}")
            print("Initializing hardware handshake sequence...")
            # This is where a real service tool pushes the BROM authentication bypass payload
            break
        time.sleep(1)
    
    if not device_port:
        print("\n[TIMEOUT] No MediaTek device detected.")
        print("Please check your phone's connection and verify that MTK USB drivers are installed.")

    print("\n=========================================")
    input("\nExecution finished. Press ENTER to close this tool...")

if __name__ == "__main__":
    main()
