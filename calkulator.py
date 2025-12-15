import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow
from AST_parse import safe_eval

def kakulasi(text: str): # kalkulasi dan FORMAT input
    # menambahkan "*" jika char == "(", "*" di tambahkan pada index sebelum index "("
    new_text = ""
    for i in range(len(text)):
        if text[i] == "(":
            if i > 0:
                if text[i-1].isdigit():
                    new_text += "*"
        new_text += text[i]
    try:
        result = safe_eval(new_text)
        result = str(result)
        result = result[:20]
    except ZeroDivisionError:
        result = 0
    except OverflowError:
        result = "Out of range"
    return str(result)
    
def button_press(event, widget): # FILTER input
    char_pressed = event.char
    current_text = widget.get()
    new_text = current_text[:]
    cursor_pos = widget.index(tk.INSERT)
    
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",]
    symbol = ["+", "-", "*","%", "!", "/", "."]
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
    
    if event.keysym == "Left" and cursor_pos > 0:
        cursor_pos -= 1
        widget.icursor(cursor_pos)
        
    if event.keysym == "Right" and cursor_pos < len(new_text):
        cursor_pos += 1
        widget.icursor(cursor_pos)
        
    # hapus char sesuai posisi cursor
    if event.keysym == "BackSpace":
        if cursor_pos > 0:
            new_text = new_text[:cursor_pos-1] + new_text[cursor_pos:]
            cursor_pos -= 1

            widget.delete(0, tk.END)
            widget.insert(0, new_text)
            widget.icursor(cursor_pos)       
        return "break"
    if event.keysym == "Delete":
        widget.delete(0, tk.END)
        widget.icursor(cursor_pos)       
        return "break"        
    
    # memberi batas panjang operasi
    if len(new_text) >= 21:
        return "break"
    
    # raturn "break" jika nilai ord event.keysym < 32 
    if not char_pressed or ord(char_pressed) < 32 and event.keysym != "Return":
        return "break"
    
    # Aturan custom buat inputan operasi
    if char_pressed in number + bracket:
        new_text, cursor_pos = adding_char(new_text, cursor_pos, char_pressed)
    
    elif char_pressed in symbol:
        if len(new_text) > 0:
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

def main_entry(window):
    # text display hasil
    my_label = tk.Entry(window,
                        justify="right",
                        relief="flat",
                        font=("Arial", 36),
                        bg="#424242",
                        fg="#e7e5e5"
                        )
    my_label.focus_set()
    my_label.bind("<Key>", lambda e: button_press(e, my_label))
    my_label.grid(row=0, column=0, sticky="new", padx=10, pady=10)

def buttons(window):
    used_font = ("Arial", 36)
    bt_0 = tk.Button(window,
                      font=used_font,
                      fg="black")
    bt_0.grid(row=1, column=0, sticky="new", padx=10, pady=10)
def main():
    # inisialisasi 
    window = tk.Tk()
    window.config(background="#424242")
    window.title("Calculator")
    window.geometry("600x400")
    
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    

    original_image = Image.open("icon.png")
    tk_image = ImageTk.PhotoImage(original_image)
    window.iconphoto(True, tk_image)
    
    main_entry(window)
    buttons(window)
    
    window.mainloop()
    
if __name__ == "__main__":
    main()