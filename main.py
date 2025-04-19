import os, io, threading, time
from datetime import datetime
from PIL import ImageGrab, Image, ImageTk, ImageDraw, ImageSequence
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import requests
import pyautogui
import cv2
import numpy as np
import win32clipboard

# === CONFIG ===
CAPTURE_DIR = "captures"
RECORD_DIR = "recordings"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1363087293711126608/l1KjvMw8egBHyDW539Fi6JSkETRFomj4jGo87WTRs-t6RFQk6_bt63Vr5RZmF7W-6Cbw"
ICON_PATH = "assets/icon.png"
BG_IMAGE_PATH = "assets/bg.png"

os.makedirs(CAPTURE_DIR, exist_ok=True)
os.makedirs(RECORD_DIR, exist_ok=True)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class GhostView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("👁 GhostView Pro 2.5")
        self.geometry("560x640")
        self.resizable(False, False)

        # Background image
        try:
            bg_img = Image.open(BG_IMAGE_PATH).resize((560, 640))
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"[WARN] Couldn't load background: {e}")

        # App icon
        try:
            icon_img = Image.open(ICON_PATH)
            icon_tk = ImageTk.PhotoImage(icon_img)
            self.iconphoto(False, icon_tk)
        except Exception as e:
            print(f"[WARN] Couldn't set icon: {e}")

        self.last_img = None
        self.last_path = None
        self.recording = False
        self.gif_frames = []

        self.build_ui()

    def build_ui(self):
        frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#1e1e1e")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="👁 GhostView Pro", font=("Segoe UI", 28, "bold"), text_color="cyan").pack(pady=20)

        pad_btn = {"width": 360, "height": 45, "font": ("Segoe UI", 14)}

        ctk.CTkButton(frame, text="📐 Capture Screenshot", command=self.capture_region, **pad_btn).pack(pady=5)
        ctk.CTkButton(frame, text="✏️ Annotate Last", command=self.annotate_last, **pad_btn).pack(pady=5)
        ctk.CTkButton(frame, text="📋 Copy to Clipboard", command=self.copy_clipboard, **pad_btn).pack(pady=5)
        ctk.CTkButton(frame, text="🚀 Share to Discord", command=self.share_discord, **pad_btn).pack(pady=5)

        ctk.CTkLabel(frame, text="Screen Recording", font=("Segoe UI", 18), text_color="orange").pack(pady=(15, 5))
        ctk.CTkButton(frame, text="🎬 Record MP4 (60FPS)", command=self.start_record_mp4, **pad_btn).pack(pady=3)
        ctk.CTkButton(frame, text="🎞️ Record GIF (60FPS)", command=self.start_record_gif, **pad_btn).pack(pady=3)
        ctk.CTkButton(frame, text="🛑 Stop Recording", command=self.stop_recording, fg_color="red", **pad_btn).pack(pady=10)

        self.status = ctk.CTkLabel(frame, text="", font=("Segoe UI", 13), text_color="lightgreen")
        self.status.pack(pady=10)

    def set_status(self, text):
        self.status.configure(text=text)

    def capture_region(self):
        self.withdraw()
        self.after(400, self._grab_region)

    def _grab_region(self):
        overlay = tk.Tk()
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.3)
        overlay.configure(bg="black")
        canvas = tk.Canvas(overlay, cursor="cross", bg="black")
        canvas.pack(fill=tk.BOTH, expand=True)
        coords = {}

        def on_click(e):
            coords["x1"], coords["y1"] = e.x, e.y

        def on_drag(e):
            canvas.delete("box")
            coords["x2"], coords["y2"] = e.x, e.y
            canvas.create_rectangle(coords["x1"], coords["y1"], coords["x2"], coords["y2"], outline='red', width=2, tag="box")

        def on_release(e):
            overlay.destroy()
            x1, y1, x2, y2 = coords["x1"], coords["y1"], coords["x2"], coords["y2"]
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            filename = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
            path = os.path.join(CAPTURE_DIR, filename)
            img.save(path)
            self.last_img = img
            self.last_path = path
            self.deiconify()
            self.set_status(f"✅ Captured: {filename}")

        canvas.bind("<Button-1>", on_click)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        overlay.mainloop()

    def annotate_last(self):
        if not self.last_img:
            return messagebox.showerror("Error", "No image to annotate yet.")

        win = tk.Toplevel(self)
        canvas = tk.Canvas(win, width=self.last_img.width, height=self.last_img.height)
        canvas.pack()

        draw_img = self.last_img.copy()
        draw = ImageDraw.Draw(draw_img)
        tk_img = ImageTk.PhotoImage(draw_img)
        canvas_img = canvas.create_image(0, 0, anchor="nw", image=tk_img)
        coords = {}

        def start_draw(e):
            coords["x"], coords["y"] = e.x, e.y

        def draw_line(e):
            x1, y1, x2, y2 = coords["x"], coords["y"], e.x, e.y
            canvas.create_line(x1, y1, x2, y2, fill="red", width=3)
            draw.line([x1, y1, x2, y2], fill="red", width=3)
            coords["x"], coords["y"] = x2, y2

        def save_annot():
            filename = datetime.now().strftime("annotated_%Y%m%d_%H%M%S.png")
            path = os.path.join(CAPTURE_DIR, filename)
            draw_img.save(path)
            self.last_img = draw_img
            self.last_path = path
            self.set_status(f"📝 Saved: {filename}")
            win.destroy()

        canvas.bind("<Button-1>", start_draw)
        canvas.bind("<B1-Motion>", draw_line)
        ctk.CTkButton(win, text="💾 Save", command=save_annot).pack(pady=5)

    def copy_clipboard(self):
        if not self.last_img:
            return
        output = io.BytesIO()
        self.last_img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        self.set_status("📋 Copied to clipboard")

    def share_discord(self):
        if not self.last_path:
            return
        def post():
            with open(self.last_path, "rb") as f:
                files = {"file": (os.path.basename(self.last_path), f)}
                r = requests.post(DISCORD_WEBHOOK, files=files)
            if r.status_code in [200, 204]:
                self.set_status("🚀 Shared to Discord")
            else:
                self.set_status("❌ Discord error")
        threading.Thread(target=post, daemon=True).start()

    def start_record_mp4(self):
        self.recording = True
        threading.Thread(target=self._record_mp4, daemon=True).start()
        self.set_status("🎬 Recording MP4...")

    def _record_mp4(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        filename = datetime.now().strftime("recording_%Y%m%d_%H%M%S.mp4")
        path = os.path.join(RECORD_DIR, filename)
        out = cv2.VideoWriter(path, fourcc, 60.0, screen_size)
        while self.recording:
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame)
        out.release()
        self.last_path = path
        self.last_img = None
        self.set_status(f"🎥 MP4 saved: {filename}")

    def start_record_gif(self):
        self.recording = True
        self.gif_frames = []
        threading.Thread(target=self._record_gif, daemon=True).start()
        self.set_status("🎞️ Recording GIF...")

    def _record_gif(self):
        while self.recording:
            frame = pyautogui.screenshot()
            self.gif_frames.append(frame)
            time.sleep(1/60.0)
        filename = datetime.now().strftime("recording_%Y%m%d_%H%M%S.gif")
        path = os.path.join(RECORD_DIR, filename)
        self.gif_frames[0].save(path, save_all=True, append_images=self.gif_frames[1:], optimize=False, duration=16, loop=0)
        self.last_path = path
        self.last_img = self.gif_frames[0]
        self.set_status(f"🎞️ GIF saved: {filename}")

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False
        self.set_status("🛑 Recording stopped.")

if __name__ == "__main__":
    app = GhostView()
    app.mainloop()
