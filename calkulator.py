import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow

def on_button_click(event, widget):
    char_pressed = event.char
    
    current_text = widget.get()
    new_text = current_text[:]
    
    number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",]
    symbol = ["+", "-", "*","%", "!", "/"]
    bracket = ["(", ")"]
    
    # hapus index terakhir
    if event.keysym == "BackSpace":
        if len(current_text) > 0:
            new_text = current_text[:-1]
            widget.delete(0, tk.END)
            widget.insert(0, new_text)
        return "break"
    
    
    if not char_pressed or ord(char_pressed) < 32:
        return "break"
    
    if char_pressed in number:
        new_text += char_pressed
        #TODO Perbaiki bagian ini;
        #jika input "2/(+2)" format seharusmya = "2/(2)"
    elif char_pressed in symbol + bracket:
        if new_text[-1] in bracket and char_pressed in symbol:
            pass
        if len(new_text) > 0 and new_text[-1] in symbol and char_pressed not in bracket:
            new_text = new_text[:-1]
        new_text += char_pressed

    widget.delete(0, tk.END)
    widget.insert(0, new_text)
    
    widget.icursor(tk.END)
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