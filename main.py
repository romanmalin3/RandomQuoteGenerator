import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

history_file = "quote_history.json"
history = []

def load_history():
    global history
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)

def save_history():
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(quote):
    quote_copy = quote.copy()
    quote_copy["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(quote_copy)
    save_history()
    update_history_display()

def update_history_display():
    history_list.delete(0, tk.END)
    filtered = filter_quotes()
    for q in filtered:
        display = f"{q['author']} - {q['text'][:50]}... ({q['topic']})"
        history_list.insert(tk.END, display)

def filter_quotes():
    author_filter = author_var.get().strip().lower()
    topic_filter = topic_var.get().strip().lower()
    
    filtered = []
    for q in history:
        if author_filter and author_filter not in q['author'].lower():
            continue
        if topic_filter and topic_filter not in q['topic'].lower():
            continue
        filtered.append(q)
    return filtered

def generate_quote():
    if quotes:
        quote = random.choice(quotes)
        quote_display.set(f'"{quote["text"]}"\n\n— {quote["author"]}\nТема: {quote["topic"]}')
        add_to_history(quote)
    else:
        messagebox.showwarning("Нет цитат", "Сначала добавьте цитаты!")

def add_quote():
    text = new_text.get().strip()
    author = new_author.get().strip()
    topic = new_topic.get().strip()
    
    if not text or not author or not topic:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return
    
    quotes.append({"text": text, "author": author, "topic": topic})
    new_text.delete(0, tk.END)
    new_author.delete(0, tk.END)
    new_topic.delete(0, tk.END)
    messagebox.showinfo("Успех", "Цитата добавлена!")

def apply_filter():
    update_history_display()

def clear_filters():
    author_var.set("")
    topic_var.set("")
    update_history_display()


root = tk.Tk()
root.title("Random Quote Generator - Роман Малин")
root.geometry("700x600")


main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


quote_display = tk.StringVar()
quote_label = tk.Label(main_frame, textvariable=quote_display, wraplength=600, 
                       font=("Arial", 12), justify="center", relief="solid", padx=20, pady=20)
quote_label.grid(row=0, column=0, columnspan=4, pady=10)


generate_btn = ttk.Button(main_frame, text="Сгенерировать цитату", command=generate_quote)
generate_btn.grid(row=1, column=0, columnspan=4, pady=10)

ttk.Label(main_frame, text="Фильтр по автору:").grid(row=2, column=0, sticky=tk.W)
author_var = tk.StringVar()
author_entry = ttk.Entry(main_frame, textvariable=author_var, width=20)
author_entry.grid(row=2, column=1, padx=5)

ttk.Label(main_frame, text="Фильтр по теме:").grid(row=2, column=2, sticky=tk.W)
topic_var = tk.StringVar()
topic_entry = ttk.Entry(main_frame, textvariable=topic_var, width=20)
topic_entry.grid(row=2, column=3, padx=5)

filter_btn = ttk.Button(main_frame, text="Применить фильтр", command=apply_filter)
filter_btn.grid(row=3, column=0, columnspan=2, pady=5)

clear_btn = ttk.Button(main_frame, text="Очистить фильтры", command=clear_filters)
clear_btn.grid(row=3, column=2, columnspan=2, pady=5)


ttk.Label(main_frame, text="История цитат:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky=tk.W, pady=(10,0))
history_list = tk.Listbox(main_frame, height=12, width=80)
history_list.grid(row=5, column=0, columnspan=4, pady=5, sticky=(tk.W, tk.E))

ttk.Label(main_frame, text="Добавить новую цитату:", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=4, sticky=tk.W, pady=(10,0))

ttk.Label(main_frame, text="Текст:").grid(row=7, column=0, sticky=tk.W)
new_text = ttk.Entry(main_frame, width=50)
new_text.grid(row=7, column=1, columnspan=3, sticky=(tk.W, tk.E), padx=5)

ttk.Label(main_frame, text="Автор:").grid(row=8, column=0, sticky=tk.W)
new_author = ttk.Entry(main_frame, width=30)
new_author.grid(row=8, column=1, padx=5)

ttk.Label(main_frame, text="Тема:").grid(row=8, column=2, sticky=tk.W)
new_topic = ttk.Entry(main_frame, width=20)
new_topic.grid(row=8, column=3, padx=5)

add_btn = ttk.Button(main_frame, text="Добавить цитату", command=add_quote)
add_btn.grid(row=9, column=0, columnspan=4, pady=10)

load_history()
update_history_display()

root.mainloop()
