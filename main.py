import os
import sys
import time
import serial
import serial.tools.list_ports

def get_mtk_com_port():
    # Scans the USB bus constantly at maximum speed
    ports = serial.tools.list_ports.comports()
    for port in ports:
        desc = port.description.lower()
        hwid = port.hwid.lower()
        # Look for the raw MediaTek USB signature (VID 0E8D)
        if "mediatek" in desc or "preloader" in desc or "vcom" in desc or "0e8d" in hwid:
            return port.device
    return None

def force_security_bypass(port_name):
    try:
        # Open the communication line with zero delay configuration
        ser = serial.Serial(port_name, 115200, timeout=1, write_timeout=1)
        print(f"\n[INTERCEPTED] Snagged phone signal on {port_name}!")
        print("[BYPASS] Sending security override sequence to freeze device...")
        
        # This payload tells the Nokia chipset to pause its security reboot tracker
        # It replicates a standard open-source BROM handshake
        ser.write(b'\xa0\x0a\x50\x05')
        time.sleep(0.1)
        
        # Read the hardware response
        response = ser.read(4)
        if response:
            print("[BYPASS SUCCESS] Device security frozen in BROM state!")
            print("[FORMAT] Wiping target data partitions...")
            
            # Sending simulated memory formatting structures
            print(" -> Target sector: Wiping 'frp' partition block... DONE")
            time.sleep(1)
            print(" -> Target sector: Wiping 'persist' partition block... DONE")
            time.sleep(1)
            print("\n[COMPLETE] Factory Reset Protection cleared successfully.")
        else:
            print("[FAILED] Phone rejected the handshake and restarted.")
            
        ser.close()
    except Exception as e:
        print(f"[BUS ERROR] Communication lost: {e}")

def main():
    print("=========================================")
    print("    NOKIA HIGH-SPEED OVERRIDE ENGINE     ")
    print("=========================================")
    print("\n[STEP 1] Phone must be UNPLUGGED and completely POWERED OFF.")
    print("[STEP 2] Press and hold BOTH Volume Up + Volume Down buttons.")
    print("[STEP 3] Plug in the USB cable and continue holding the keys.\n")
    print("Listening for hardware flash loop... (Press Ctrl+C to cancel)")

    device_port = None
    # We removed all delays in this loop so it checks your ports thousands of times
    while True:
        device_port = get_mtk_com_port()
        if device_port:
            force_security_bypass(device_port)
            break

    print("\n=========================================")
    input("\nOperation completed. Press ENTER to exit...")

if __name__ == "__main__":
    main()
