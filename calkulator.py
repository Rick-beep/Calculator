import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow


def kakulasi(text: str):
    # menambahkan "*" jika char == "(", "*" di tambahkan pada index sebelum index "("
    new_text = ""
    for i in range(len(text)):
        if text[i] == "(":
            new_text += "*"
        new_text += text[i]

    try:
        result = eval(new_text)
    except ZeroDivisionError:
        result = 0
    
    except OverflowError:
        result = "Out of range"
    
    return str(result)
    

def on_button_click(event, widget):
    char_pressed = event.char
    
    current_text = widget.get()
    new_text = current_text[:]
    
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",]
    symbol = ["+", "-", "*","%", "!", "/", "."]
    bracket = ["(", ")"]
    
    cursor_pos = widget.index(tk.INSERT)
    
    # hapus char sesuai posisi cursor
    if event.keysym == "BackSpace":
        if len(current_text) > 0:
            new_text = current_text[:-1]
            widget.delete(0, tk.END)
            widget.insert(0, new_text)
        return "break"

    if event.keysym == "Return" or char_pressed == "=" and len(new_text) > 0:
        new_text = kakulasi(new_text)
        
    if not char_pressed or ord(char_pressed) < 32 and event.keysym != "Return":
        return "break"
    
    if char_pressed in number:
        new_text = new_text[:cursor_pos] + char_pressed + new_text[cursor_pos:]
        cursor_pos += 1
        
    elif char_pressed in symbol + bracket:
        if len(new_text) > 0 and new_text[cursor_pos-1] in symbol and char_pressed not in bracket:
            new_text = new_text[:cursor_pos-1] + new_text[cursor_pos:]
        new_text = new_text[:cursor_pos] + char_pressed + new_text[cursor_pos:]
        cursor_pos += 1
     
    widget.delete(0, tk.END)
    widget.insert(0, new_text)
    widget.icursor(cursor_pos)
    return "break"
        
window = tk.Tk()
window.config(background="grey")
window.title("Calculator")
window.geometry("600x400") 

original_image = Image.open("icon.png")
tk_image = ImageTk.PhotoImage(original_image)
window.iconphoto(True, tk_image)

# text display hasil
my_label = tk.Entry(window, 
                    font=("Arial", 48),
                    bg="#2a79b5"
                    )
my_label.focus_set()
my_label.grid(row=0, column=0) 
 
my_label.bind("<Key>", lambda e: on_button_click(e, my_label))
window.mainloop()