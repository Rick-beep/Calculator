import tkinter as tk
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
            elif text[i] == "^":
                new_text += "**"
                continue
            elif text[i] == "%":
                new_text += "/100*"
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
            if char_pressed == "-":
                if new_text[cursor_pos - 1] != "-":
                    new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed)
                
            elif new_text[cursor_pos - 1] == "-":
                new_text, cursor_pos = adding_char(new_text, cursor_pos, "", True, True)
                
            elif new_text[cursor_pos - 1] in symbol:
                new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed, True)
                
            elif new_text[cursor_pos - 1] not in bracket:
                new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed)        
    
    widget.delete(0, tk.END)  
    widget.insert(0, new_text)
    widget.icursor(cursor_pos)
    return "break"

def entry_main(window):
    entry_string = tk.StringVar()
    entry_main = tk.Entry(window,
                        textvariable=entry_string,
                        justify="right",
                        relief="flat",
                        font=("Arial", 36),
                        bg="#222222",
                        fg="#e7e5e5"
                        )
    entry_main.focus_set()
    entry_main.bind("<Key>", lambda e: validate_input(e, entry_main))
    entry_main.grid(row=0, column=0, sticky="new", padx=10, pady=10)
    
    return entry_main

def buttons(window):
    frame = tk.Frame(window,
                    bg="#222222",
                     )
    used_font = ("Arial", 36)
    
    def simulate_key(window, key):
        window.event_generate(key)
        
    # row 1
    # tombol open bracket ("(")
    bt_open_braket = tk.Button(frame,
                    text="(",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "(")        
    )        
    bt_open_braket.grid(
              row=1, 
              column=0, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # tombol close bracket (")")
    bt_close_bracket = tk.Button(frame,
                    text=")",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, ")")        
    )        
    bt_close_bracket.grid(row=1, 
              column=1, 
              sticky="w",
              padx=10, 
              pady=3)

    # tombol modulo (%)
    bt_modulo = tk.Button(frame,
                    text="%",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "%")        
    )        
    bt_modulo.grid(row=1, 
              column=2, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # tombol bagi (/)
    bt_bagi = tk.Button(frame,
                    text="/",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "/")        
    )        
    bt_bagi.grid(row=1, 
              column=3, 
              sticky="w",
              padx=10, 
              pady=3)
        
    # row 2
    # tombol 7
    bt_7 = tk.Button(frame,
                    text="7",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "7")        
    )        
    bt_7.grid(row=2, 
              column=0, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # tombol 8
    bt_8 = tk.Button(frame,
                    text="8",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "8")        
    )        
    bt_8.grid(row=2, 
              column=1, 
              sticky="w",
              padx=10, 
              pady=3)

    # tombol 9
    bt_9 = tk.Button(frame,
                    text="9",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "9")        
    )        
    bt_9.grid(row=2, 
              column=2, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # tombol kali (x)
    bt_kali = tk.Button(frame,
                    text="*",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "*")        
    )        
    bt_kali.grid(row=2, 
              column=3, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # row 3
    # tombol 4
    bt_4 = tk.Button(frame,
                    text="4",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "4")        
    )        
    bt_4.grid(row=3, 
              column=0, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # tombol 5
    bt_5 = tk.Button(frame,
                    text="5",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "5")        
    )        
    bt_5.grid(row=3, 
              column=1, 
              sticky="w",
              padx=10, 
              pady=3)

    # tombol 6
    bt_6 = tk.Button(frame,
                    text="6",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "6")        
    )        
    bt_6.grid(row=3, 
              column=2, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # tombol plus (-)
    bt_minus = tk.Button(frame,
                    text="-",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "-")        
    )        
    bt_minus.grid(row=3, 
              column=3, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # row 4
    # tombol 1
    bt_1 = tk.Button(frame,
                    text="1",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "1")        
    )        
    bt_1.grid(row=4, 
              column=0, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # tombol 2
    bt_2 = tk.Button(frame,
                    text="2",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "2")        
    )        
    bt_2.grid(row=4, 
              column=1, 
              sticky="w",
              padx=10, 
              pady=3)

    # tombol 3
    bt_3 = tk.Button(frame,
                    text="3",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "3")        
    )        
    bt_3.grid(row=4, 
              column=2, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # tombol plus (+)
    bt_plus = tk.Button(frame,
                    text="+",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "+")        
    )        
    bt_plus.grid(row=4, 
              column=3, 
              sticky="w",
              padx=10, 
              pady=3)
    
    # row 5
    # tombol 0
    bt_0 = tk.Button(frame,
                    text="0",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "0")
                    )
    bt_0.grid(row=5, 
              column=0, 
              sticky="w", 
              padx=10, 
              pady=3)
    
    # tombol dot (.)
    bt_dot = tk.Button(frame,
                    text=".",
                    font=used_font,
                    relief="flat",
                    fg="#e7e5e5",
                    bg="#4e4f4f",
                    command=lambda: simulate_key(window, "."))
    bt_dot.grid(row=5, 
              column=1, 
              sticky="s", 
              padx=10, 
              pady=3)
    
    # tombol backspace
    bt_backspace = tk.Button(frame,
                text="<",
                font=used_font,
                relief="flat",
                fg="#e7e5e5",
                bg="#4e4f4f",
                command=lambda: simulate_key(window, "<BackSpace>"))
    bt_backspace.grid(row=5, 
              column=2, 
              sticky="e", 
              padx=10, 
              pady=3)
    
    # tombol equal (evaluasi hasil)
    bt_equal = tk.Button(frame,
                text="=",
                font=used_font,
                relief="flat",
                fg="#e7e5e5",
                bg="#4e4f4f",
                command=lambda: simulate_key(window, "="))
    bt_equal.grid(row=5, 
              column=3, 
              sticky="e", 
              padx=10, 
              pady=3)
    
    # set frame
    frame.grid(row=1,
               column=0,
               sticky="s",
               padx=10,
               pady=10)
    
def main():
    # inisialisasi 
    window = tk.Tk()
    window.config(background="#222222")
    window.title("Calculator")
    window.geometry("600x600")
    
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    

    original_image = Image.open("icon.png")
    tk_image = ImageTk.PhotoImage(original_image)
    window.iconphoto(True, tk_image)
     
    entry_main(window)
    buttons(window)
    
    window.mainloop()
    
if __name__ == "__main__":
    main()