
import tkinter as tk
from tkinter import ttk

# -------------------------
# Focus Buddy - Version 1.0
# -------------------------

FOCUS_TIME = 25 * 60
BREAK_TIME = 5 * 60

root = tk.Tk()
root.title("Focus Buddy")
root.geometry("420x520")
root.resizable(False, False)
root.configure(bg="#FFF4F0")

# Application state
mode = "Focus"
remaining_seconds = FOCUS_TIME
sessions_completed = 0
is_running = False
timer_id = None


def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def update_pet():
    if sessions_completed == 0:
        pet_label.config(text="🐱")
        pet_message.config(text="I'm ready! Let's get productive!")
    elif sessions_completed < 3:
        pet_label.config(text="😺")
        pet_message.config(text="You're doing great! Keep going!")
    elif sessions_completed < 5:
        pet_label.config(text="😻")
        pet_message.config(text="WOW! You're on fire!")
    else:
        pet_label.config(text="😽")
        pet_message.config(text="You're a productivity legend!")


def update_display():
    timer_label.config(text=format_time(remaining_seconds))
    mode_label.config(text=f"{mode} Time")

    duration = FOCUS_TIME if mode == "Focus" else BREAK_TIME
    progress = (duration - remaining_seconds) / duration * 100

    progress_bar["value"] = progress
    session_label.config(
        text=f"Sessions completed: {sessions_completed}"
    )

    update_pet()


def tick():
    global remaining_seconds, timer_id, is_running

    if not is_running:
        return

    if remaining_seconds > 0:
        remaining_seconds -= 1
        update_display()
        timer_id = root.after(1000, tick)
    else:
        finish_session()


def start_timer():
    global is_running

    if not is_running:
        is_running = True
        start_button.config(text="Pause")
        tick()


def pause_timer():
    global is_running, timer_id

    is_running = False

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    start_button.config(text="Start")


def toggle_timer():
    if is_running:
        pause_timer()
    else:
        start_timer()


def reset_timer():
    global remaining_seconds

    pause_timer()

    remaining_seconds = (
        FOCUS_TIME if mode == "Focus" else BREAK_TIME
    )

    update_display()


def finish_session():
    global mode, remaining_seconds, sessions_completed
    global is_running, timer_id

    is_running = False
    timer_id = None
    start_button.config(text="Start")

    if mode == "Focus":
        sessions_completed += 1
        mode = "Break"
        remaining_seconds = BREAK_TIME
        status_label.config(
            text="Focus session complete! Time for a break! 🎉"
        )
    else:
        mode = "Focus"
        remaining_seconds = FOCUS_TIME
        status_label.config(
            text="Break's over! Ready for another round?"
        )

    update_display()


def skip_session():
    global remaining_seconds, mode

    pause_timer()

    if mode == "Focus":
        mode = "Break"
        remaining_seconds = BREAK_TIME
    else:
        mode = "Focus"
        remaining_seconds = FOCUS_TIME

    status_label.config(text="Switched sessions. Your choice!")
    update_display()


# -------------------------
# User Interface
# -------------------------

title_label = tk.Label(
    root,
    text="FOCUS BUDDY",
    font=("Arial", 22, "bold"),
    bg="#FFF4F0",
    fg="#754C45"
)
title_label.pack(pady=(25, 5))

subtitle_label = tk.Label(
    root,
    text="Your little productivity companion",
    font=("Arial", 10),
    bg="#FFF4F0",
    fg="#A17D75"
)
subtitle_label.pack()

pet_label = tk.Label(
    root,
    text="🐱",
    font=("Segoe UI Emoji", 65),
    bg="#FFF4F0"
)
pet_label.pack(pady=(15, 0))

pet_message = tk.Label(
    root,
    text="I'm ready! Let's get productive!",
    font=("Arial", 10),
    bg="#FFF4F0",
    fg="#754C45"
)
pet_message.pack(pady=5)

mode_label = tk.Label(
    root,
    text="Focus Time",
    font=("Arial", 14, "bold"),
    bg="#FFF4F0",
    fg="#C47D72"
)
mode_label.pack(pady=(15, 0))

timer_label = tk.Label(
    root,
    text="25:00",
    font=("Arial", 48, "bold"),
    bg="#FFF4F0",
    fg="#754C45"
)
timer_label.pack(pady=5)

progress_bar = ttk.Progressbar(
    root,
    length=280,
    mode="determinate",
    maximum=100
)
progress_bar.pack(pady=15)

button_frame = tk.Frame(root, bg="#FFF4F0")
button_frame.pack(pady=10)

start_button = tk.Button(
    button_frame,
    text="Start",
    font=("Arial", 11, "bold"),
    bg="#D99A91",
    fg="white",
    width=10,
    relief="flat",
    command=toggle_timer
)
start_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(
    button_frame,
    text="Reset",
    font=("Arial", 11),
    bg="#E8D4CD",
    fg="#754C45",
    width=10,
    relief="flat",
    command=reset_timer
)
reset_button.grid(row=0, column=1, padx=5)

skip_button = tk.Button(
    button_frame,
    text="Skip",
    font=("Arial", 11),
    bg="#E8D4CD",
    fg="#754C45",
    width=10,
    relief="flat",
    command=skip_session
)
skip_button.grid(row=0, column=2, padx=5)

session_label = tk.Label(
    root,
    text="Sessions completed: 0",
    font=("Arial", 11, "bold"),
    bg="#FFF4F0",
    fg="#754C45"
)
session_label.pack(pady=(20, 5))

status_label = tk.Label(
    root,
    text="Every little step counts. 💗",
    font=("Arial", 9),
    bg="#FFF4F0",
    fg="#A17D75",
    wraplength=350
)
status_label.pack(pady=5)

update_display()
root.mainloop()