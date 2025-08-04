# full_agent_gui.py

import tkinter as tk
from tkinter import scrolledtext
import re
import os
import json
import google.generativeai as genai
import calculator_tool
import translator_tool
from datetime import datetime

# ========== Gemini Setup ==========
genai.configure(api_key=os.getenv("GEMINI_API_KEY") or "your-api-key")
model = genai.GenerativeModel("models/gemini-2.5-pro")
chat = model.start_chat(history=[])

# ========== Task Detection ==========
def detect_tasks(text):
    tasks = []
    text = text.lower()
    parts = re.split(r'\b(?:then|,)\b', text)

    for part in parts:
        part = part.strip()

        # Translation
        match = re.search(r"translate\s+'(.+?)'\s+into\s+german", part)
        if match:
            tasks.append(('translate', match.group(1)))
            continue

        # Capital of country
        match = re.search(r"capital of (\w+)", part)
        if match:
            tasks.append(('general', f"What is the capital of {match.group(1)}?"))
            continue

        # Math: "add 10 and 20", "multiply 5 and 6", etc.
        math_pattern = r"(add|plus|sum|subtract|minus|multiply|times|divide|divided|\+|\-|\*|\/)\s+(\d+(?:\.\d+)?)(?:\s+(?:and|with)?\s*(\d+(?:\.\d+)?))?"
        matches = re.findall(math_pattern, part)
        for match in matches:
            op, num1, num2 = match
            if num1 and num2:
                tasks.append(('math', f"{op} {num1} and {num2}"))

    return tasks

# ========== Handle Tasks ==========
def handle_task(task):
    task_type, content = task
    if task_type == 'math':
        return calculator_tool.calculate(content).strip()
    elif task_type == 'translate':
        return translator_tool.translate_to_german(content).strip()
    elif task_type == 'general':
        try:
            response = chat.send_message(content)
            return response.text.strip()
        except Exception as e:
            return f"LLM Error: {e}"
    return "Unrecognized task."

# ========== Save Logs ==========
def log_interaction(user_msg, bot_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to TXT
    with open("interaction_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\nYou: {user_msg}\nBot:\n{bot_response}\n\n")

    # Save to JSON
    log_entry = {
        "timestamp": timestamp,
        "user": user_msg,
        "bot": bot_response.splitlines()
    }

    if not os.path.exists("interaction_logs.json"):
        with open("interaction_logs.json", "w", encoding="utf-8") as f:
            json.dump([log_entry], f, indent=2)
    else:
        with open("interaction_logs.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=2)

# ========== GUI Setup ==========
root = tk.Tk()
root.title("🧠 LLM Agent (Level 3)")
root.geometry("700x600")
root.configure(bg="#1e1e1e")

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#121212", fg="#f0f0f0", font=("Consolas", 12))
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_display.config(state=tk.DISABLED)

input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(input_frame, font=("Arial", 14), bg="#2e2e2e", fg="#ffffff")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entry.bind("<Return>", lambda e: send_message())

send_btn = tk.Button(input_frame, text="Send", font=("Arial", 12), bg="#1E88E5", fg="white", command=lambda: send_message())
send_btn.pack(side=tk.LEFT)

# ========== Display Chat ==========
def display_message(text, sender="Bot"):
    chat_display.config(state=tk.NORMAL)
    if sender == "You":
        chat_display.insert(tk.END, f"\n🧑 You:\n", "user")
    else:
        chat_display.insert(tk.END, f"\n🤖 Bot:\n", "bot")
    chat_display.insert(tk.END, f"{text}\n", "msg")
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)

chat_display.tag_config("user", foreground="#90CAF9", font=("Consolas", 11, "bold"))
chat_display.tag_config("bot", foreground="#A5D6A7", font=("Consolas", 11, "bold"))
chat_display.tag_config("msg", foreground="#E0E0E0")

# ========== Send Message ==========
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    display_message(user_input, "You")
    entry.delete(0, tk.END)

    tasks = detect_tasks(user_input)
    if not tasks:
        try:
            response = chat.send_message(user_input)
            result = response.text.strip()
        except Exception as e:
            result = f"LLM Error: {e}"
        display_message(result, "Bot")
        log_interaction(user_input, result)
        return

    full_response = ""
    for task in tasks:
        result = handle_task(task)
        full_response += result + "\n"
    full_response = full_response.strip()
    display_message(full_response, "Bot")
    log_interaction(user_input, full_response)

# ========== Run App ==========
root.mainloop()

