# 👁️ GhostView Pro 2.5

**GhostView Pro** is a sleek, powerful, and cozy screen capture + recording tool built with Python.  
Designed for creators and devs, it captures screenshots, allows annotations, records in MP4/GIF at 60 FPS, and shares instantly via Discord.

> 🧠 Clean UI · 💡 Annotate Fast · 🚀 Discord Instant Share

---

## ✨ Features

- 📐 Region Screenshot Capture  
- ✏️ Draw / Annotate Screenshots  
- 📋 Copy Image to Clipboard  
- 🚀 Share to Discord via Webhook  
- 🎬 MP4 Screen Recording (60 FPS)  
- 🎞️ GIF Screen Recording (60 FPS)  
- 🛑 One-Click Stop Recording  
- 🖼️ Custom Background & App Icon  
- 🎨 Cozy modern UI with `customtkinter`

---

## 📂 Folder Structure

```
GhostView-Pro/
├── assets/
│   ├── bg.png              # Background image
│   └── icon.png            # App icon
│
├── captures/               # Saved screenshots & annotations
├── recordings/             # Saved MP4/GIF screen records
├── main.py                 # Main app script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚙️ Requirements

Install all dependencies:

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install pillow customtkinter opencv-python pyautogui pywin32 requests
```

---

## 🚀 Run the App

```bash
python main.py
```

---

## 🔗 Discord Integration

1. Create a webhook in your Discord server.
2. Replace the `DISCORD_WEBHOOK` URL in `main.py` with yours.
3. Click "🚀 Share to Discord" in the app to send your image/recording.

---

## 🧪 Use Cases

- Capture annotated bug reports  
- Record feature demos or tutorials  
- Share visuals instantly with your team  
- Build better feedback loops using Discord

---

## 🛠️ Tech Stack

- Python
- Pillow (Image Handling)
- OpenCV (Video)
- PyAutoGUI (Screen Capture)
- CustomTkinter (GUI)
- Requests (Webhook Upload)
- pywin32 (Clipboard)

---

## 🧑‍💻 Author

**Zoro** — Discord Dev, Bot Maker & Toolsmith  
💬 [Discord](https://discord.com/users/1357257822571855986)

> “Power in simplicity. Fancy in design.”

---

## ⭐ Like it?

If this helped you or looks 🔥 in your portfolio, drop a **star** on GitHub.  
It motivates me to keep creating awesome open-source tools!

---

Let me know if you want GitHub badges, preview GIFs, or to prep the GitHub repo layout too.
