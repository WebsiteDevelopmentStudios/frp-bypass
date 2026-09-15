import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import os
import sys

# Function to get correct path for bundled binaries when compiled via PyInstaller
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class FastbootTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Fastboot FRP Utility")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Title Label
        title = tk.Label(root, text="Fastboot Device Service Tool", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # UI Buttons
        self.btn_check = tk.Button(btn_frame, text="1. Check Connection", width=18, command=self.check_device)
        self.btn_check.grid(row=0, column=0, padx=5, pady=5)

        self.btn_wipe = tk.Button(btn_frame, text="2. Wipe FRP Partition", width=18, bg="orange", fg="black", command=self.wipe_frp)
        self.btn_wipe.grid(row=0, column=1, padx=5, pady=5)

        self.btn_reboot = tk.Button(btn_frame, text="3. Reboot Device", width=18, command=self.reboot_device)
        self.btn_reboot.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Log Output Terminal
        log_label = tk.Label(root, text="Activity Log:")
        log_label.pack(anchor="w", padx=20)
        
        self.log_area = scrolledtext.ScrolledText(root, width=55, height=12, font=("Consolas", 10))
        self.log_area.pack(padx=20, pady=5)
        self.log_message("System Ready. Connect your phone in Fastboot mode.")

    def log_message(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def run_fastboot_command(self, args):
        fastboot_path = get_resource_path("fastboot.exe")
        
        if not os.path.exists(fastboot_path):
            self.log_message("ERROR: fastboot.exe missing from application files.")
            return "Error"

        try:
            # Executes fastboot.exe in background without showing a CMD window
            result = subprocess.run([fastboot_path] + args, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Execution failed: {str(e)}"

    def check_device(self):
        self.log_message("Scanning for devices...")
        output = self.run_fastboot_command(["devices"])
        if output.strip():
            self.log_message(f"Found Device:\n{output}")
        else:
            self.log_message("No devices detected. Check drivers and USB connection.")

    def wipe_frp(self):
        confirm = messagebox.askyesno("Confirm Action", "Are you sure you want to run the erasure loop?")
        if not confirm:
            return
            
        self.log_message("Starting partition erasure sequence...")
        
        # Targets the three common variations used by different Android OEMs
        partitions = ["frp", "config", "persist"]
        for part in partitions:
            self.log_message(f"Erasing block: {part}...")
            output = self.run_fastboot_command(["erase", part])
            self.log_message(output.strip())
            
        self.log_message("Sequence complete.")

    def reboot_device(self):
        self.log_message("Sending reboot command...")
        output = self.run_fastboot_command(["reboot"])
        self.log_message(output.strip())

if __name__ == "__main__":
    root = tk.Tk()
    app = FastbootTool(root)
    root.mainloop()
