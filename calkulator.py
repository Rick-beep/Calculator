import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import Pillow
from AST_parse import safe_eval

def kakulasi(text: str): # kalkulasi dan FORMAT input
    # menambahkan "*" jika char == "(", "*" di tambahkan pada index sebelum index "("
    new_text = ""
    
    # check charr pada index terrakhir, jika char digit atau "(", ")". block kode akan berjalan
    if text[-1].isdigit() or text[-1] in "()":
        for i in range(len(text)):
            if text[i] == "(" and i > 0:
                if text[i-1].isdigit():
                    new_text += "*"
            
            elif text[i-1] == ")" and text[i] not in "+-*%^/.":
                new_text += "*"
                new_text += text[i]
            
            elif text[i] == "^":
                new_text += "**"
                continue
            elif text[i] == "%": # PErbaiki bagian ini
                new_text = "(" + new_text + "/100)*"
                continue
            new_text += text[i]
    else:
        return text
    
    try:
        result = safe_eval(new_text)
        result = str(result)
        result = result[:20]
    except ZeroDivisionError:
        result = 0
    except OverflowError:
        result = "Out of range"
    
    return str(result)
    
def validate_input(event, widget): # FILTER input
    char_pressed = event.char
    current_text = widget.get()
    new_text = current_text[:]
    cursor_pos = widget.index(tk.INSERT)
    
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",]
    symbol = ["+", "-", "*", "%", "^", "/", "."]
    bracket = ["(", ")"]
    
    
    def adding_char(new_text, cursor_pos, char_pressed, replace_flag=False, remove_flag=False):
        offset = 0
        rmv_offset = 0
        if replace_flag:
            offset = 1
        
        if remove_flag:
            rmv_offset = 1
    
        new_text = new_text[:cursor_pos - offset] + char_pressed + new_text[cursor_pos:]
        cursor_pos += 1 - offset - rmv_offset
        
        return new_text, cursor_pos        
    
    # evaluasi hasil dari operasi
    if event.keysym == "Return" or char_pressed == "=" and len(new_text) > 0:
        new_text = kakulasi(new_text)
        cursor_pos = len(str(new_text))
        
    elif event.keysym == "Left" and cursor_pos > 0:
        cursor_pos -= 1
        widget.icursor(cursor_pos)
        
    elif event.keysym == "Right" and cursor_pos < len(new_text):
        cursor_pos += 1
        widget.icursor(cursor_pos)
        
    # hapus char sesuai posisi cursor
    elif event.keysym == "BackSpace":
        if cursor_pos > 0:
            new_text = new_text[:cursor_pos-1] + new_text[cursor_pos:]
            cursor_pos -= 1

            widget.delete(0, tk.END)
            widget.insert(0, new_text)
            widget.icursor(cursor_pos)       
        return "break"
    elif event.keysym == "Delete":
        widget.delete(0, tk.END)
        widget.icursor(cursor_pos)       
        return "break"        
    
    # memberi batas panjang operasi
    if len(new_text) >= 20:
        return "break"
    
    # raturn "break" jika nilai ord event.keysym < 32 
    if not char_pressed or ord(char_pressed) < 32 and event.keysym != "Return":
        return "break"
    
    # Aturan custom buat inputan operasi
    if char_pressed in number + bracket:
        new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed)
    
    elif char_pressed in symbol:
        if char_pressed == "." and "." in new_text:
            pass
        elif len(new_text) > 0:
            if new_text[-1] == "%":
                new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed)        
                
            if char_pressed == "-":
                if new_text[cursor_pos - 1] != "-":
                    new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed)
                
            elif new_text[cursor_pos - 1] == "-":
                new_text, cursor_pos = adding_char(new_text, cursor_pos, "", True, True)
                
            elif new_text[cursor_pos - 1] in symbol:
                new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed, True)
                
            else:
                new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed)        
    
    widget.delete(0, tk.END)  
    widget.insert(0, new_text)
    widget.icursor(cursor_pos)
    return "break"

def entry_main(window, style):
    style.theme_use("clam")
    
    style.configure("Custom.TEntry",
                justify="right",
                insertcolor="#e7e5e5",
                insertwidth=2,
                foreground="#e7e5e5",
                fieldbackground="#222222",
                background="#222222",
                lightcolor="#222222",
                bordercolor="#222222",     
                relief="flat"
                ) 
    
    style.map("Custom.TEntry",
                lightcolor=[("focus", "#222222"),
                    ("pressed", "#222222"),
                    ("active", "#222222")],
                bordercolor=[("focus", "#222222"),
                    ("pressed", "#222222"),
                    ("active", "#222222")]
              )

    
    entry_string = tk.StringVar()
    current_entry_main = ttk.Entry(window,
                                   style="Custom.TEntry",
                                    font=("Calibri", 36),
                                   textvariable=entry_string)
    
    current_entry_main.focus_set()
    current_entry_main.bind("<Key>", lambda e: validate_input(e, current_entry_main))
    current_entry_main.grid(row=0, column=0, sticky="new", padx=10, pady=10)
    
    return current_entry_main

def buttons(window, entry, style):
    frame = tk.Frame(window,
                    bg="#222222",
                     )
    style.configure("Custom.TButton",
                    font="Calibri",
                    relief="flat",
                    borderwidth=0,
                    highlightcolor="#4e4f4f",
                    focuscolor="#4e4f4f")
    style.map("Custom.TButton",
                    foreground=[('disabled', '#e7e5e5'), ('active', '#e7e5e5')],
                    background=[('pressed', "#4e4f4f"), ('active', "#4e4f4f",)],)

    padx_value, pady_value = 5, 3
    
    def simulate_key(entry, key):
        entry.focus()
        entry.event_generate(key)
        
    # row 1
    # tombol open bracket ("(")
    bt_open_braket = ttk.Button(frame,
                                text="(",
                                style="Custom.TButton",
                                command=lambda: simulate_key(entry, "(")        
    )        
    bt_open_braket.grid(
              row=1, 
              column=0, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # tombol close bracket (")")
    bt_close_bracket = ttk.Button(frame,
                    text=")",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, ")")        
    )        
    bt_close_bracket.grid(row=1, 
              column=1, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)

    # tombol modulo (%)
    bt_modulo = ttk.Button(frame,
                    text="%",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "%")        
    )        
    bt_modulo.grid(row=1, 
              column=2, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # tombol bagi (/)
    bt_bagi = ttk.Button(frame,
                    text="/",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "/")        
    )        
    bt_bagi.grid(row=1, 
              column=3, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
        
    # row 2
    # tombol 7
    bt_7 = ttk.Button(frame,
                    text="7",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "7")        
    )        
    bt_7.grid(row=2, 
              column=0, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # tombol 8
    bt_8 = ttk.Button(frame,
                    text="8",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "8")        
    )        
    bt_8.grid(row=2, 
              column=1, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)

    # tombol 9
    bt_9 = ttk.Button(frame,
                    text="9",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "9")        
    )        
    bt_9.grid(row=2, 
              column=2, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # tombol kali (x)
    bt_kali = ttk.Button(frame,
                    text="*",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "*")        
    )        
    bt_kali.grid(row=2, 
              column=3, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # row 3
    # tombol 4
    bt_4 = ttk.Button(frame,
                    text="4",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "4")        
    )        
    bt_4.grid(row=3, 
              column=0, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # tombol 5
    bt_5 = ttk.Button(frame,
                    text="5",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "5")        
    )        
    bt_5.grid(row=3, 
              column=1, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)

    # tombol 6
    bt_6 = ttk.Button(frame,
                    text="6",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "6")        
    )        
    bt_6.grid(row=3, 
              column=2, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # tombol plus (-)
    bt_minus = ttk.Button(frame,
                    text="-",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "-")        
    )        
    bt_minus.grid(row=3, 
              column=3, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # row 4
    # tombol 1
    bt_1 = ttk.Button(frame,
                    text="1",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "1")        
    )        
    bt_1.grid(row=4, 
              column=0, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # tombol 2
    bt_2 = ttk.Button(frame,
                    text="2",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "2")        
    )        
    bt_2.grid(row=4, 
              column=1, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)

    # tombol 3
    bt_3 = ttk.Button(frame,
                    text="3",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "3")        
    )        
    bt_3.grid(row=4, 
              column=2, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # tombol plus (+)
    bt_plus = ttk.Button(frame,
                    text="+",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "+")        
    )        
    bt_plus.grid(row=4, 
              column=3, 
              sticky="w",
              padx=padx_value, 
              pady=pady_value)
    
    # row 5
    # tombol 0
    bt_0 = ttk.Button(frame,
                    text="0",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "0")
                    )
    bt_0.grid(row=5, 
              column=0, 
              sticky="w", 
              padx=padx_value, 
              pady=pady_value)
    
    # tombol dot (.)
    bt_dot = ttk.Button(frame,
                    text=".",
                    style="Custom.TButton",
                    command=lambda: simulate_key(entry, "."))
    bt_dot.grid(row=5, 
              column=1, 
              sticky="s", 
              padx=padx_value, 
              pady=pady_value)
    
    # tombol backspace
    bt_backspace = ttk.Button(frame,
                text="<",
                style="Custom.TButton",
                command=lambda: simulate_key(entry, "<BackSpace>"))
    bt_backspace.grid(row=5, 
              column=2, 
              sticky="e", 
              padx=padx_value, 
              pady=pady_value)
    
    # tombol equal (evaluasi hasil)
    bt_equal = ttk.Button(frame,
                text="=",
                style="Custom.TButton",
                command=lambda: simulate_key(entry, "="))
    bt_equal.grid(row=5, 
              column=3, 
              sticky="e", 
              padx=padx_value, 
              pady=pady_value)
    
    # set frame
    frame.grid(row=1,
               column=0,
               sticky="s",
               padx=padx_value,
               pady=10)
    
def main():
    # inisialisasi 
    window = tk.Tk()
    style = ttk.Style()
    window.config(background="#222222")
    window.title("Calculator")
    window.geometry("550x512")
    
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    
    original_image = Image.open("icon.png")
    tk_image = ImageTk.PhotoImage(original_image)
    window.iconphoto(True, tk_image)
     
    entry = entry_main(window, style)
    buttons(window, entry, style)
    
    window.mainloop()
    
if __name__ == "__main__":
    main()