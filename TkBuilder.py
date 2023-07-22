from tkinter import Tk, mainloop, Label, Button, Frame, StringVar
from tkinter.ttk import Combobox, Style
from ttkthemes import ThemedTk
from json import dump

"""
Written by gamerchungus27
"""



def create_button(owner_window:object, name:str, master:object, text:str, width:int, height:int, bg:str, bd:int, x:int, y:int):
    button = Button(master, width=width, height=height, text=text, name=name, bg=bg, bd=bd)
    owner_window.place_element(button, x, y)
    return button

def create_label(owner_window:object, name:str, master:object, text:str, width:int, height:int, bg:str, bd:int, x:int, y:int):
    label = Label(master, width=width, height=height, text=text, name=name, bg=bg, bd=bd)
    owner_window.place_element(label, x, y)
    return label

def create_frame(owner_window:object, name:str, master:object, width:int, height:int, bg:str, bd:int, x:int, y:int):
    frame = Frame(master, width=width, height=height, name=name, bg=bg, bd=bd)
    owner_window.place_element(frame, x, y)
    return frame

def create_combobox(owner_window:object, name:str, master:object, value:list, width:int, height:int, x:int, y:int):
    combobox = Combobox(master, width=width, height=height, name=name, values=value, state='readonly')
    owner_window.place_element(combobox, x, y)
    return combobox


class Application(ThemedTk):
    def __init__(self):
        super().__init__()
        Style(self).theme_use('arc')
        self.title("TkBuilder")
        self.real_children = []
        self.resizable(True,True)
        self.geometry('800x700')
        self.minsize(800,700)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind("<Map>", self.unminimised)
        self.bind("<Unmap>", self.minimised)

        self.primary_frame = Frame(self, bg='gray75', bd=1); self.primary_frame.pack(anchor="e")
        self.primary_panel = Label(self.primary_frame, bd=0, width=20, height=40, bg="gray95"); self.primary_panel.pack(padx=0,pady=0)

        self.create_gui()


    def create_gui(self):
        create_button(self, "test_button", self.primary_panel, "test", 5, 2, "gray90", 0, 10, 10)
        create_combobox(self, "test_optionmenu", self.primary_panel, ["Hi", "Bye", "Hello"], 5, 0, 75, 20)
    

    

    def close(self):
        BUILD_WINDOW.destroy()
        self.destroy()

    def unminimised(self,event):
        BUILD_WINDOW.deiconify()
    
    def minimised(self,event):
        BUILD_WINDOW.iconify()

    def place_element(self, item, x, y):
        item.place(x=x, y=y)
        item.name = item.winfo_name()
        self.real_children.append(item)

    


class APP_WINDOW(ThemedTk):
    def __init__(self):
        super().__init__()
        self.style = Style(self)
        self.style.theme_use('alt')
        self.real_children = []
        self.name = "WINDOW"
        self.load_order = 0
        self.resizable(False,False)
        self.title("Build Window")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.attributes('-topmost', True)
        self.bind("<Map>", self.unminimised)
        self.bind("<Unmap>", self.minimised)

        create_button(self, "test_button", self, "TEST_BUTTON", 5, 2, "gray90", 0, 10, 10)

    
    def place_element(self, item, x, y):
        if item.master == self:
            item.load_order = 0
        else:
            item.load_order = item.master.load_order + 1
        item.place(x=x, y=y)
        item.name = item.winfo_name()
        self.real_children.append(item)
        
    
    def close(self):
        self.save_json()
        for child in self.winfo_children():
            child.destroy()
        self.real_children = []

    def save_json(self):
        if self.winfo_children():
            data = {"window_data": {},
                    "objects": {}}
            with open("output.tkbuilt.json", "w") as file:
                for child in self.real_children:
                    data["objects"][str(child.winfo_name())] = {
                            "item_type": child.widgetName,
                            "load_order": child.load_order,
                            "master": child.master.name,
                            "bg": child['bg'],
                            "bd": child['bd'],
                            "width": child['width'],
                            "height": child['height'],
                            "x": child.winfo_x(),
                            "y": child.winfo_y(),
                        }
                    try: #Checks to see if object has "text" option. If not, passes.
                        data['objects'][str(child.winfo_name())]['text'] = child['text']
                    except Exception as e:
                        print(e)
                data["window_data"] = {"test": "test"}
                dump(data, file)

       
    def destroy(self) -> None:
        self.save_json()
        return super().destroy()
    
    def unminimised(self,event):
        WINDOW.deiconify()
    
    def minimised(self,event):
        WINDOW.iconify()
    





if __name__ == "__main__":
    WINDOW = Application()
    BUILD_WINDOW = APP_WINDOW()
    
    def update_build_WINDOW():
        BUILD_WINDOW.geometry("{0}x{1}+{2}+{3}".format(WINDOW.winfo_width() - 250, WINDOW.winfo_height() - 125, WINDOW.winfo_x() + 50, WINDOW.winfo_y() + 50))
        BUILD_WINDOW.after(1, update_build_WINDOW)
    
    BUILD_WINDOW.after(1, update_build_WINDOW)

    mainloop()