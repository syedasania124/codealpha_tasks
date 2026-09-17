import tkinter as tk
from tkinter import ttk, messagebox
import requests


# =========================================================
# COLORS
# =========================================================

BLACK = "#0D0D0D"
DARK_BLACK = "#151515"
CARD = "#1C1C1C"
INPUT_BG = "#242424"

MAROON = "#800000"
DARK_MAROON = "#5A0000"
LIGHT_MAROON = "#A52A2A"

WHITE = "#FFFFFF"
LIGHT_TEXT = "#E6E6E6"
GRAY = "#A0A0A0"
BORDER = "#333333"


# =========================================================
# LANGUAGES
# =========================================================

languages = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Turkish": "tr",
    "Dutch": "nl"
}


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("AI Language Translation Tool")
root.geometry("950x700")
root.minsize(850, 620)
root.configure(bg=BLACK)


# =========================================================
# COMBOBOX STYLE
# =========================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Dark.TCombobox",
    fieldbackground=INPUT_BG,
    background=INPUT_BG,
    foreground=WHITE,
    arrowcolor=WHITE,
    bordercolor=BORDER,
    lightcolor=INPUT_BG,
    darkcolor=INPUT_BG,
    padding=9
)

style.map(
    "Dark.TCombobox",
    fieldbackground=[("readonly", INPUT_BG)],
    foreground=[("readonly", WHITE)],
    selectbackground=[("readonly", MAROON)],
    selectforeground=[("readonly", WHITE)]
)


# =========================================================
# DARK DROPDOWN
# =========================================================

def make_dropdown_dark(combo):
    try:
        popdown = root.tk.call(
            "ttk::combobox::PopdownWindow",
            combo
        )

        listbox = f"{popdown}.f.l"

        root.tk.call(
            listbox,
            "configure",
            "-background", INPUT_BG,
            "-foreground", WHITE,
            "-selectbackground", MAROON,
            "-selectforeground", WHITE
        )

    except tk.TclError:
        pass


# =========================================================
# TRANSLATE FUNCTION
# =========================================================

def translate_text():

    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Empty Text",
            "Please enter some text to translate."
        )
        return

    source = source_combo.get()
    target = target_combo.get()

    source_code = languages[source]
    target_code = languages[target]

    if source_code == target_code:

        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", text)

        status_label.config(
            text="● Translation completed",
            fg="#5CB85C"
        )

        return

    status_label.config(
        text="● Translating...",
        fg="#E0A800"
    )

    root.update_idletasks()

    try:

        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": f"{source_code}|{target_code}"
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            raise Exception("Translation API is unavailable.")

        data = response.json()

        translated = data["responseData"]["translatedText"]

        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", translated)

        status_label.config(
            text="● Translation completed",
            fg="#5CB85C"
        )

    except requests.exceptions.RequestException:

        status_label.config(
            text="● Connection error",
            fg="#D9534F"
        )

        messagebox.showerror(
            "Connection Error",
            "Please check your internet connection."
        )

    except Exception as error:

        status_label.config(
            text="● Translation error",
            fg="#D9534F"
        )

        messagebox.showerror(
            "Error",
            str(error)
        )


# =========================================================
# CLEAR FUNCTION
# =========================================================

def clear_text():

    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

    char_label.config(
        text="0 characters"
    )

    status_label.config(
        text="● Ready",
        fg=GRAY
    )


# =========================================================
# COPY FUNCTION
# =========================================================

def copy_translation():

    translated = output_text.get(
        "1.0",
        tk.END
    ).strip()

    if not translated:

        messagebox.showwarning(
            "Nothing to Copy",
            "There is no translation to copy."
        )

        return

    root.clipboard_clear()
    root.clipboard_append(translated)
    root.update()

    status_label.config(
        text="● Translation copied",
        fg="#5CB85C"
    )


# =========================================================
# SWAP FUNCTION
# =========================================================

def swap_languages():

    source = source_combo.get()
    target = target_combo.get()

    source_combo.set(target)
    target_combo.set(source)

    old_input = input_text.get(
        "1.0",
        tk.END
    ).strip()

    old_output = output_text.get(
        "1.0",
        tk.END
    ).strip()

    if old_output:

        input_text.delete("1.0", tk.END)
        input_text.insert("1.0", old_output)

        output_text.delete("1.0", tk.END)
        output_text.insert("1.0", old_input)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=BLACK
)

header.pack(
    fill="x",
    pady=(25, 10)
)


title = tk.Label(
    header,
    text="AI LANGUAGE TRANSLATOR",
    font=("Segoe UI", 25, "bold"),
    bg=BLACK,
    fg=LIGHT_MAROON
)

title.pack()


subtitle = tk.Label(
    header,
    text="Translate text between multiple languages using an online API",
    font=("Segoe UI", 11),
    bg=BLACK,
    fg=GRAY
)

subtitle.pack(pady=(5, 0))


# =========================================================
# LANGUAGE SELECTION CARD
# =========================================================

language_card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

language_card.pack(
    fill="x",
    padx=40,
    pady=10
)


# Source

source_frame = tk.Frame(
    language_card,
    bg=CARD
)

source_frame.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(20, 8),
    pady=18
)


tk.Label(
    source_frame,
    text="SOURCE LANGUAGE",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=LIGHT_TEXT
).pack(
    anchor="w",
    pady=(0, 7)
)


source_combo = ttk.Combobox(
    source_frame,
    values=list(languages.keys()),
    state="readonly",
    style="Dark.TCombobox",
    font=("Segoe UI", 11)
)

source_combo.set("English")

source_combo.pack(
    fill="x"
)


# Swap

swap_button = tk.Button(
    language_card,
    text="⇄",
    command=swap_languages,
    font=("Segoe UI", 18, "bold"),
    bg=DARK_MAROON,
    fg=WHITE,
    activebackground=LIGHT_MAROON,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    width=3,
    cursor="hand2"
)

swap_button.pack(
    side="left",
    padx=8,
    pady=(32, 0)
)


# Target

target_frame = tk.Frame(
    language_card,
    bg=CARD
)

target_frame.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(8, 20),
    pady=18
)


tk.Label(
    target_frame,
    text="TARGET LANGUAGE",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=LIGHT_TEXT
).pack(
    anchor="w",
    pady=(0, 7)
)


target_combo = ttk.Combobox(
    target_frame,
    values=list(languages.keys()),
    state="readonly",
    style="Dark.TCombobox",
    font=("Segoe UI", 11)
)

target_combo.set("Urdu")

target_combo.pack(
    fill="x"
)


# =========================================================
# TEXT CARD
# =========================================================

text_card = tk.Frame(
    root,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

text_card.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=10
)


# =========================================================
# INPUT TITLE
# =========================================================

input_header = tk.Frame(
    text_card,
    bg=CARD
)

input_header.pack(
    fill="x",
    padx=18,
    pady=(15, 5)
)


tk.Label(
    input_header,
    text="ENTER TEXT",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=LIGHT_TEXT
).pack(
    side="left"
)


char_label = tk.Label(
    input_header,
    text="0 characters",
    font=("Segoe UI", 9),
    bg=CARD,
    fg=GRAY
)

char_label.pack(
    side="right"
)


# =========================================================
# INPUT BOX
# =========================================================

input_text = tk.Text(
    text_card,
    height=6,
    font=("Segoe UI", 12),
    bg=INPUT_BG,
    fg=WHITE,
    insertbackground=WHITE,
    selectbackground=MAROON,
    selectforeground=WHITE,
    relief="flat",
    wrap="word",
    padx=15,
    pady=12
)

input_text.pack(
    fill="x",
    padx=18
)


# =========================================================
# THREE MAIN BUTTONS
# =========================================================

button_frame = tk.Frame(
    text_card,
    bg=CARD
)

button_frame.pack(
    pady=15
)


translate_button = tk.Button(
    button_frame,
    text="TRANSLATE",
    command=translate_text,
    font=("Segoe UI", 11, "bold"),
    bg=MAROON,
    fg=WHITE,
    activebackground=LIGHT_MAROON,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=35,
    pady=11,
    cursor="hand2"
)

translate_button.grid(
    row=0,
    column=0,
    padx=7
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_text,
    font=("Segoe UI", 11, "bold"),
    bg="#333333",
    fg=WHITE,
    activebackground="#505050",
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=35,
    pady=11,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=1,
    padx=7
)


copy_button = tk.Button(
    button_frame,
    text="COPY TRANSLATION",
    command=copy_translation,
    font=("Segoe UI", 11, "bold"),
    bg=DARK_MAROON,
    fg=WHITE,
    activebackground=MAROON,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    padx=25,
    pady=11,
    cursor="hand2"
)

copy_button.grid(
    row=0,
    column=2,
    padx=7
)


# =========================================================
# OUTPUT TITLE
# =========================================================

output_header = tk.Frame(
    text_card,
    bg=CARD
)

output_header.pack(
    fill="x",
    padx=18,
    pady=(0, 5)
)


tk.Label(
    output_header,
    text="TRANSLATED TEXT",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=LIGHT_TEXT
).pack(
    side="left"
)


# =========================================================
# OUTPUT BOX
# =========================================================

output_text = tk.Text(
    text_card,
    height=6,
    font=("Segoe UI", 12),
    bg=INPUT_BG,
    fg=WHITE,
    insertbackground=WHITE,
    selectbackground=MAROON,
    selectforeground=WHITE,
    relief="flat",
    wrap="word",
    padx=15,
    pady=12
)

output_text.pack(
    fill="both",
    expand=True,
    padx=18,
    pady=(0, 15)
)


# =========================================================
# STATUS BAR
# =========================================================

status_frame = tk.Frame(
    root,
    bg=DARK_BLACK
)

status_frame.pack(
    fill="x"
)


status_label = tk.Label(
    status_frame,
    text="● Ready",
    font=("Segoe UI", 9),
    bg=DARK_BLACK,
    fg=GRAY
)

status_label.pack(
    side="left",
    padx=25,
    pady=8
)


tk.Label(
    status_frame,
    text="Translation API Connected",
    font=("Segoe UI", 9),
    bg=DARK_BLACK,
    fg=GRAY
).pack(
    side="right",
    padx=25,
    pady=8
)


# =========================================================
# CHARACTER COUNTER
# =========================================================

def update_counter(event=None):

    text = input_text.get(
        "1.0",
        tk.END
    ).strip()

    char_label.config(
        text=f"{len(text)} characters"
    )


input_text.bind(
    "<KeyRelease>",
    update_counter
)


# =========================================================
# KEYBOARD SHORTCUT
# =========================================================

def translate_shortcut(event=None):

    translate_text()
    return "break"


input_text.bind(
    "<Control-Return>",
    translate_shortcut
)


# =========================================================
# START
# =========================================================

root.after(
    300,
    lambda: make_dropdown_dark(source_combo)
)

root.after(
    300,
    lambda: make_dropdown_dark(target_combo)
)

root.mainloop()