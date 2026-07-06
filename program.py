import time
import xlwings as xw
import pyperclip
import tkinter as tk
from tkinter import messagebox
from playsound3 import playsound
import threading, keyboard, requests
from io import BytesIO
from PIL import Image, ImageTk
from threading import Lock

# === CONFIGURATION ===
EXCEL_FILE   = 'customers.xlsx'   # keep it open in Excel while you run this
VOICEMAIL_FILE = 'voicemail.m4a'
HOTKEY       = 'down'
SPRITE_URL   = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/"
    "master/sprites/pokemon/959.png"
)

GREEN = (144, 238, 144)            # RGB for LightGreen

# === Voicemail playback pause ===
_last_play = 0.0          # epoch seconds
_cooldown  = 5.0          # seconds
_lock      = Lock()

# --- NEW CONST ----------------------------------------------------
SUKI_URL = "https://images.squarespace-cdn.com/content/v1/6598c8e83ff0af0197ff19f9/1711967628022-GQW5X3ITB24EDYQI4XYK/2001-Honda-S2000-Suki-Car-2-Fast-2-Furious-_0004_TED_7070.jpg"      # Suki shot :contentReference[oaicite:0]{index=0}

def fetch_suki() -> bytes:
    r = requests.get(SUKI_URL, timeout=10)
    r.raise_for_status()
    return r.content

# ------------------------------------------------------------------ fetch sprite
def fetch_sprite() -> bytes:
    r = requests.get(SPRITE_URL, timeout=10)
    r.raise_for_status()
    return r.content

# === TEXT GENERATION LOGIC (Excel live, no file lock) =============
def generate_text():
    try:
        # attach to an already-open workbook, or open it if closed
        wb = xw.Book(EXCEL_FILE)
        ws = wb.sheets["active"]                     # first sheet

        # find last used row in column A
        last_row = ws.range('A' + str(ws.cells.last_cell.row)).end('up').row

        for row in range(2, last_row + 1):    # skip header
            status = ws.range(row, 10).value  # column J
            if status != 'Sent':
                name = ws.range(row, 1).value     # column A
                car  = ws.range(row, 6).value     # column F

                if not name or not car:
                    continue

                msg = (
                    f"Good morning {name},\n\n"
                    f"This is Alexandra from Midwestern Automotive Group in Dublin. "
                    f"This is your annual service reminder for your {car}.\n\n"
                    f"If you'd like to schedule, please use the link below:\n\n"
                    f"Online Service Scheduler | Midwestern Auto Group\n\n"
                    f"Thank you for choosing M.A.G!\n\n– Alexandra Stoycheva"
                )

                pyperclip.copy(msg)

                # mark row as sent + highlight
                ws.range(row, 10).value = 'Sent'
                ws.range((row, 1), (row, 10)).color = GREEN

                wb.save()                     # updates the GUI workbook instantly
                messagebox.showinfo("Copied!", f"Message for {name} copied.")
                return

        messagebox.showinfo("Done", "All rows marked 'Sent'.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# === VOICEMAIL PLAYBACK ============================================
def play_voicemail():
    global _last_play

    with _lock:                          # make button-mashing thread-safe
        now = time.time()
        if now - _last_play < _cooldown:
            return                      # still in the 5-second window → ignore
        _last_play = now                # reset the timer

    def _play():
        try:
            playsound(VOICEMAIL_FILE)
        except Exception as e:
            messagebox.showerror("Playback Error", str(e))

    threading.Thread(target=_play, daemon=True).start()

# === HOTKEY BINDING ================================================
def bind_hotkey():
    keyboard.add_hotkey(HOTKEY, play_voicemail)
    keyboard.wait()

# === GUI ===========================================================
def run_gui():
    root = tk.Tk()
    root.title("MAG Service Tools")
    root.configure(bg="white")

    btn_style = dict(font=('Arial', 14), width=25,
                     bg="#ff99cc", activebackground="#ff80c0", fg="black")

    tk.Button(root, text="Generate Text",
              command=generate_text, **btn_style).pack(pady=10)
    tk.Button(root, text="Play Voicemail (Down Arrow)",
              command=play_voicemail, **btn_style).pack(pady=10)

    # --- Pokémon sprite (100×100) ----------------------------------
    raw_poke = Image.open(BytesIO(fetch_sprite())).convert("RGBA")
    poke_pil = raw_poke.crop(raw_poke.getbbox()).resize((100, 100), Image.Resampling.LANCZOS)
    poke_img = ImageTk.PhotoImage(poke_pil, master=root)
    root.poke_img = poke_img          # prevent GC

    # --- Suki image (100×100) --------------------------------------
    raw_suki = Image.open(BytesIO(fetch_suki())).convert("RGB")
    # make a copy so .thumbnail doesn’t mutate the original
    suki_pil = raw_suki.copy()
    suki_pil.thumbnail((200, 200), Image.Resampling.LANCZOS)   # keeps ratio!

    suki_img = ImageTk.PhotoImage(suki_pil, master=root)
    root.suki_img = suki_img

    # footer with heart + Suki + Pokémon
    footer = tk.Frame(root, bg="white")
    tk.Label(footer, text="❤️", font=('Arial', 24), bg="white", fg="red").pack(side="left")
    tk.Label(footer, image=suki_img, bg="white").pack(side="left", padx=10)
    #tk.Label(footer, image=poke_img, bg="white").pack(side="left", padx=10)
    footer.pack(side="bottom", pady=5)

    root.geometry('500x260')      # wider to fit both images
    threading.Thread(target=bind_hotkey, daemon=True).start()
    root.mainloop()


if __name__ == "__main__":
    run_gui()
