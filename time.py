import os
from datetime import datetime, timedelta
import time  # To slow down updates
import keyboard
from dateutil.relativedelta import relativedelta  # For adding months
import threading  # For running truetime in a separate thread

def set_system_time(new_time):
    """Set the Windows system time using PowerShell."""
    formatted_time = new_time.strftime("%Y-%m-%d %H:%M:%S")
    os.system(f'powershell.exe -Command "Set-Date \'{formatted_time}\'"')
    print(f"System time set to: {formatted_time}")

def toggle_time_automatic():
    """Toggle the 'Set time automatically' setting in Windows."""
    # Check the current state of 'Set time automatically'
    result = os.popen('powershell.exe -Command "(Get-ItemProperty -Path HKLM:\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters).Type"').read().strip()
    if result == "NTP":
        # If it's set to automatic (NTP), turn it off
        os.system('powershell.exe -Command "Set-ItemProperty -Path HKLM:\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters -Name Type -Value NoSync"')
        print("'Set time automatically' turned OFF.")
    else:
        # If it's off, turn it on
        os.system('powershell.exe -Command "Set-ItemProperty -Path HKLM:\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters -Name Type -Value NTP"')
        print("'Set time automatically' turned ON.")

def update_truetime():
    """Continuously update the truetime variable."""
    global truetime, reset_truetime
    while True:
        if reset_truetime:
            truetime = datetime.now()
            reset_truetime = False
        else:
            truetime += timedelta(seconds=1)
        time.sleep(1)

print("1 = 2minutes, 2 = 5minutes, 3 = 1day, 4 = 1month, 5 = reset, ESC = exit")

new_time = datetime.now()  # Start with current system time
truetime = datetime.now()  # Initialize truetime
reset_truetime = False  # Flag to reset truetime

# Start the truetime updater thread
threading.Thread(target=update_truetime, daemon=True).start()

while True:
    print("Waiting for key press...")
    key = keyboard.read_key()  # Wait for a specific key press

    if key == "1":  # Pressing '1' adds 2 minutes
        new_time += timedelta(minutes=2)
        print("Adding 2 minutes...")
        set_system_time(new_time)
        time.sleep(0.5)  # Prevent too fast updates

    elif key == "2":  # Pressing '2' adds 5 minutes
        new_time += timedelta(minutes=5)
        print("Adding 5 minutes...")
        set_system_time(new_time)
        time.sleep(0.5)  # Prevent too fast updates

    elif key == "3":  # Pressing '3' adds 1 day
        new_time += timedelta(days=1)
        print("Adding 1 day...")
        set_system_time(new_time)
        time.sleep(0.5)  # Prevent too fast updates

    elif key == "4":  # Pressing '4' adds 1 month
        new_time += relativedelta(months=1)
        print("Adding 1 month...")
        set_system_time(new_time)
        time.sleep(0.5)  # Prevent too fast updates

    elif key == "5":  # Pressing '5' resets truetime
        print("Resetting to truetime...")
        truetime = datetime.now()  # Reset truetime to the exact current time
        reset_truetime = True  # Set the flag to reset truetime
        time.sleep(1)  # Allow the thread to update truetime
        new_time = truetime  # Sync new_time with truetime
        set_system_time(new_time)  # Set the system time to truetime
        print(f"System time reset to truetime: {truetime}")

    elif key == "esc":  # Pressing 'ESC' exits the program
        print("Exiting...")
        break