import pyautogui
import time
import tkinter as tk
from tkinter import ttk
import threading

# Global variable to control the typing process
pause_typing = False
stop_typing = False

def write_code(code, typing_speed):
    """
    This function takes the user input code and types it at the specified typing speed.
    Typing is done in the background to keep the GUI responsive.
    """
    global pause_typing, stop_typing
    
    # Wait for the user to switch to the desired window
    print("You have 5 seconds to switch to the target window.")
    time.sleep(5)

    # Process the code line by line
    for i, line in enumerate(code.split('\n')):
        if stop_typing:
            break
        
        # Pause typing if requested
        while pause_typing:
            time.sleep(0.1)  # Wait while paused
            
        stripped_line = line.lstrip()  # Remove leading whitespace from each line
        pyautogui.typewrite(stripped_line, interval=typing_speed)
        pyautogui.press('enter')
        time.sleep(typing_speed)  # Delay between lines

def start_typing_thread():
    """
    This function retrieves user input from the GUI and initiates the auto-typing process in a separate thread.
    """
    global stop_typing
    stop_typing = False
    
    # Retrieve the code and typing speed from the user inputs
    code = text_area.get("1.0", tk.END)
    typing_speed = speed_scale.get()

    # Create a thread for typing so the GUI remains responsive
    typing_thread = threading.Thread(target=write_code, args=(code, typing_speed))
    typing_thread.start()

def pause_resume_typing():
    """
    This function toggles the pause and resume state of typing.
    """
    global pause_typing
    pause_typing = not pause_typing  # Toggle pause state
    if pause_typing:
        pause_button.config(text="Resume Typing")
    else:
        pause_button.config(text="Pause Typing")

def stop_typing_process():
    """
    This function stops the typing process.
    """
    global stop_typing
    stop_typing = True

# Create the main application window
app = tk.Tk()
app.title("Auto Typer with Background Typing and Pause Feature")

# Create a text area for code input
label_code = tk.Label(app, text="Enter your text or code to type:")
label_code.pack()

text_area = tk.Text(app, wrap="word", height=15, width=50)
text_area.pack()

# Create a speed control using a slider
label_speed = tk.Label(app, text="Typing Speed (seconds per character):")
label_speed.pack()

speed_scale = ttk.Scale(app, from_=0.05, to=1.0, orient="horizontal", length=200, value=0.25)
speed_scale.pack()

# Create a button to start typing
start_button = tk.Button(app, text="Start Typing", command=start_typing_thread)
start_button.pack()

# Create a button to pause/resume typing
pause_button = tk.Button(app, text="Pause Typing", command=pause_resume_typing)
pause_button.pack()

# Create a button to stop typing
stop_button = tk.Button(app, text="Stop Typing", command=stop_typing_process)
stop_button.pack()

# Run the Tkinter event loop
app.mainloop()