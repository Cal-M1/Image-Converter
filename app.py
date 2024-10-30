import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass

class App(ctk.CTk):
    def __init__(self):
        # Setup
        super().__init__(fg_color = BLACK)
        ctk.set_appearance_mode("dark")
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        self.title('')
        self.iconbitmap('empty.ico')
        self.title_bar_color()

        # Image
        raw_image = Image.open('placeholder.png').resize((200, 200))
        tk_image = ImageTk.PhotoImage(raw_image)
        self.image_canvas = CreateImage(self)
        self.image_canvas.update_image(tk_image)

        # Entry field
        self.entry_field = EntryField(self, self.image_canvas)

        # Run the app
        self.mainloop()

    def title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLOR['dark']  # Only dark mode color needed
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass

class EntryField(ctk.CTkFrame):
    def __init__(self, parent, image_canvas):
        super().__init__(master = parent, corner_radius = 20, fg_color = MAIN_COLOR)
        self.place(relx = 0.5, rely = 1, relwidth = 1, relheight = 0.4, anchor = 'center')
        self.image_canvas = image_canvas

        # Image formats
        formats = ['PNG', 'JPEG', 'WEBP', 'TIFF']

        # Grid layout 
        self.rowconfigure((0,1), weight = 1, uniform = 'a')
        self.columnconfigure(0, weight = 1, uniform = 'a')

        # Widgets 
        self.frame = ctk.CTkFrame(self, fg_color = 'transparent')
        self.frame.columnconfigure(0, weight = 1, uniform = 'b')
        self.frame.columnconfigure(1, weight = 4, uniform = 'b')
        self.frame.columnconfigure(2, weight = 2, uniform = 'b')
        self.frame.columnconfigure(3, weight = 2, uniform = 'b')
        self.frame.columnconfigure(4, weight = 1, uniform = 'b')
        self.frame.grid(row = 0, column = 0)

        self.combo = ctk.CTkComboBox(self.frame, values = formats, fg_color = BUTTON_COLOR, border_width = 0, text_color = 'white', button_color = BUTTON_COLOR, button_hover_color = HOVER_COLOR, dropdown_fg_color = MAIN_COLOR,)
        self.combo.grid(row = 0, column = 1, sticky = 'nsew', padx = 5)

        upload_button = ctk.CTkButton(self.frame, text = 'Upload', command = self.import_image, fg_color = BUTTON_COLOR, hover_color = HOVER_COLOR)
        upload_button.grid(row = 0, column = 2, sticky = 'nsew', padx = 3)

        save_button = ctk.CTkButton(self.frame, command = self.save_image, text = 'Save', fg_color = BUTTON_COLOR, hover_color = HOVER_COLOR)
        save_button.grid(row = 0, column = 3, sticky = 'nsew', padx = 3)
                
    def import_image(self):
        try:
            file = filedialog.askopenfile()
            
            if file:
                path = file.name
                self.imported_image = Image.open(path)
                
                # Create a Copy of imported image and add background
                display_image = self.imported_image.copy()
                display_image.thumbnail((300, 300), Image.Resampling.LANCZOS)
                background = Image.new('RGB', (300, 300), BLACK)
                paste_x = (300 - display_image.width) // 2
                paste_y = (300 - display_image.height) // 2
                background.paste(display_image, (paste_x, paste_y))

                image_tk = ImageTk.PhotoImage(background)
                self.image_canvas.update_image(image_tk)

        except Exception as error:
            CTkMessagebox(title="Error", message= f"Error importing image: {error}", icon="cancel", button_color = BUTTON_COLOR, button_hover_color = HOVER_COLOR)

    def save_image(self):
        try:
            selected_format = self.combo.get()

            file_extension = selected_format.lower()
            file_path = filedialog.asksaveasfilename(defaultextension=f".{file_extension}", filetypes=[(selected_format, f"*.{file_extension}")])

            if file_path and self.imported_image:
                self.imported_image.save(file_path, format=selected_format)
                CTkMessagebox(title="Info", message= f"Image saved as {file_path}", button_color = BUTTON_COLOR, button_hover_color = HOVER_COLOR)
            else:
                CTkMessagebox(title="Error", message= "No image or file path specified.", icon="cancel",  button_color = BUTTON_COLOR, button_hover_color = HOVER_COLOR)

        except Exception as error:
            CTkMessagebox(title="Error", message= f"Error saving image: {error}", icon="cancel",  button_color = BUTTON_COLOR, button_hover_color = HOVER_COLOR)

class CreateImage(tk.Canvas):
    def __init__(self, parent):
        super().__init__(master = parent, background= BLACK, bd=0, highlightthickness= 0, relief='ridge')
        self.place(relx=0.5, rely=0.4, width=300, height=300, anchor='center')
        self.image = None

    def update_image(self, image_tk):
        self.delete('all')
        self.create_image(150, 150, image= image_tk, anchor='center')
        self.image = image_tk

if __name__ == '__main__':
    App()