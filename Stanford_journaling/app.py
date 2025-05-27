import pygame
import tkinter as tk
import random
import sqlite3
from datetime import datetime

pygame.mixer.init()
is_music_playing = False

prompts = [
    "What are you grateful for today?",
    "Describe your perfect day from start to finish.",
    "Write about a lesson you learned the hard way.",
    "What is something you wish more people knew about you?",
    "Reflect on a recent challenge. What did it teach you?",
    "If you could talk to your past self, what would you say?",
    "What are your goals for the next 6 months?",
    "Write about a place that makes you feel at peace.",
    "What habits are helping or hurting your growth?",
    "List 10 things that make you smile.",
    "Describe a moment when you felt truly proud of yourself.",
    "How do you define success?",
    "What fears are holding you back?",
    "Write about someone who inspires you and why.",
    "What does your ideal morning routine look like?",
    "How do you handle failure?",
    "What are three things you love about yourself?",
    "What would you do if you knew you couldn't fail?",
    "Describe your dream life in 10 years.",
    "Write a letter to your future self."
]

# 🧠 Show random prompt
def show_prompt():
    selected = random.choice(prompts)
    prompt_label.config(text=selected)
    text_box.delete("1.0", tk.END)

# 💾 Save entry to SQLite
def save_entry():
    prompt = prompt_label.cget("text")
    entry = text_box.get("1.0", tk.END).strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if prompt and entry:
        conn = sqlite3.connect("journal.db")
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                entry TEXT,
                timestamp TEXT
            )
        """)

        # Insert data
        cursor.execute("INSERT INTO journal_entries (prompt, entry, timestamp) VALUES (?, ?, ?)",
                       (prompt, entry, timestamp))

        conn.commit()
        conn.close()

        # Feedback
        status_label.config(text="✅ Entry saved successfully!", fg="green")
        text_box.delete("1.0", tk.END)
    else:
        status_label.config(text="⚠ Please write something before saving.", fg="red")

# Playing music
def toggle_music():
    global is_music_playing

    if not is_music_playing:
        try:
            pygame.mixer.music.load("lofi-relax-lofi-345374.mp3")
            pygame.mixer.music.play(-1)
            play_button.config(text="⏹ Stop Music")
            is_music_playing = True
        except Exception as e:
            status_label.config(text=f"❌ Error: {str(e)}", fg="red")
    else:
        pygame.mixer.music.stop()
        play_button.config(text="▶ Play Music")
        is_music_playing = False

# 🌿 GUI Setup
root = tk.Tk()
root.title("📝 Mindful Journal")
root.geometry("800x700")
root.configure(bg="#f0f4f8")

# Top bar frame (for positioning)
top_frame = tk.Frame(root, bg="#f0f4f8")
top_frame.pack(fill="x", pady=(10, 0), padx=20)

# 🎵 Play Music Button (top-left)
play_button = tk.Button(top_frame, text="▶ Play Music", command=toggle_music,
                        font=("Arial", 10), bg="#fce8ff", padx=8, pady=4)
play_button.pack(side="left")

# 🌸 Prompt Label
prompt_label = tk.Label(root, text="Click the button for a journaling prompt ✨",
                        font=("Arial", 14), bg="#f0f4f8", wraplength=600, justify="center")
prompt_label.pack(pady=30)

# 🎲 Prompt Button
prompt_button = tk.Button(root, text="🎲 Show Prompt", command=show_prompt,
                          font=("Arial", 12), bg="#dceefc", padx=10, pady=5)
prompt_button.pack()

# ✍ Journal Textbox
text_box = tk.Text(root, height=20, width=80, font=("Arial", 12), wrap=tk.WORD, bd=2, padx=10, pady=10)
text_box.pack(pady=25)

# 💾 Save Button
save_button = tk.Button(root, text="💾 Save Entry", command=save_entry,
                        font=("Arial", 12), bg="#c8f7c5", padx=10, pady=5)
save_button.pack()

# ✅ Status Label
status_label = tk.Label(root, text="", font=("Arial", 10), bg="#f0f4f8")
status_label.pack(pady=10)

# 🚀 Run the app
root.mainloop()