import os
import sys
import time
import serial.tools.list_ports

def find_mtk_port():
    # High-speed scan of active Windows COM ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        port_desc = port.description.lower()
        port_hwid = port.hwid.lower()
        
        # Looks for any MediaTek signatures or standard vendor IDs (e.g., VID 0e8d)
        if "mediatek" in port_desc or "preloader" in port_desc or "mcom" in port_desc or "0e8d" in port_hwid:
            return port.device
    return None

def main():
    print("=========================================")
    print("    NOKIA HIGH-SPEED HARDWARE CATCHER    ")
    print("=========================================")
    print("\n[STEP 1] Keep your phone completely UNPLUGGED and POWERED OFF.")
    print("[STEP 2] Press and hold BOTH Volume Up + Volume Down buttons.")
    print("[STEP 3] Plug in the USB cable and do NOT let go of the keys.\n")
    print("Monitoring hardware buses at ultra-high speed...")

    device_port = None
    timeout = 45  # Increased total scan window to 45 seconds
    start_time = time.time()

    # REMOVED the time.sleep(1) delay so it loops hundreds of times per second
    while (time.time() - start_time) < timeout:
        device_port = find_mtk_port()
        if device_port:
            print(f"\n[SUCCESS] INTERCEPTED DEVICE ON PORT: {device_port}")
            print("Hardware link established successfully.")
            break
    
    if not device_port:
        print("\n[TIMEOUT] The 2-second device connection window was missed.")
        print("Please ensure your volume buttons are held down *before* the USB cable goes in.")

    print("\n=========================================")
    input("\nExecution finished. Press ENTER to close this tool...")

if __name__ == "__main__":
    main()
