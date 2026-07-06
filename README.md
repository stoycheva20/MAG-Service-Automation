# MAG-Service-Automation

Python automation tool developed in 2025 to streamline dealership service reminder workflows.

## Features
- Generates personalized service reminder text messages (so you dont have to type it all out every customer) from an Excel workbook and automatically copies it to your clipboard
- Marks the customers you used my program to make text messages for as "Sent" and highlights processed rows in excel workbook
- Plays a prerecorded voicemail using a keyboard hotkey. (best part) 
- Simple (custom!) Tkinter GUI for daily use.

## Technologies Used
- **Python** – Self-taught specifically to automate repetitive dealership service reminder tasks
- **Tkinter** – Built a desktop GUI so the tool could be used without running code from the terminal
- **xlwings** – for the execel workbook interaction
- **Pyperclip** – Automatically copied personalized reminder messages to the clipboard for faster customer communication
- **Playsound3** – Integrated prerecorded voicemail playback to streamline outbound calling
- **Keyboard** – Added a global hotkey to play voicemail without interrupting the calling workflow(downward arrow key)
- **Pillow (PIL)** – Loaded and displayed images within the application's interface
- **Requests** – Retrieved images from online sources for the GUI(this was unnecessarily tricky)
- **Threading** – Kept the interface responsive while voicemail audio played and background hotkeys remained active

## Purpose
While working one summer as a Service BDC Representative at Midwestern Automotive Group I completed approximately 200 outbound service reminder calls per day, many of which went to voicemail. To reduce repetitive work, I deicded I would teach myself Python and developed this automation tool after work. This repository uses fictional customer data and omits any proprietary company information.

This repository uses fictional customer data but preserves the same spreadsheet structure and workflow as the original project.
