import tkinter as tk
from PIL import Image, ImageTk  # Import Pillow

history = 0
operasi = ""

def on_button_click(event):
    char_pressed = event.char
    key_symbol = event.keysym
    
    global operasi
    
    if char_pressed:
        number = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",]
        symbol = ["+", "-", "*","%", "!", "/"]
        bracket = ["(", ")"]
        
        
        # untuk menghapus index terahir
        if key_symbol == "BackSpace" and len(operasi) > 0:
            operasi = operasi[:-1]
        
        if char_pressed in number:
            operasi += char_pressed
            
        elif char_pressed in symbol + bracket:
            if operasi[-1:] in symbol and char_pressed not in bracket:
                operasi = operasi[:-1]
            operasi += char_pressed
            print(char_pressed)

            
    print(operasi)

window = tk.Tk()
window.config(background="grey")
window.title("Calculator")
window.geometry("600x400") 

original_image = Image.open("icon.png")
tk_image = ImageTk.PhotoImage(original_image)
window.iconphoto(True, tk_image)

# text display hasil
my_label = tk.Label(window, 
                    text=f"{operasi}", 
                    font=("Arial", 48),
                    bg="#2a79b5"
                    )
my_label.grid(row=0, column=0) 
 
 
# Button (0-9, C, =)
my_button = tk.Button(window, text="0", command=on_button_click)
my_button.grid(row=2, column=0)

window.bind("<Key>", on_button_click)
window.mainloop()