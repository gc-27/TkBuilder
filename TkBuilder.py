from tkinter import Tk, mainloop, Label, Button, Frame
from json import dump

"""
Written by gamerchungus27
"""



def create_button(caller:object, name:str, master:object, text:str, width:int, height:int, bg:str, bd:int, x:int, y:int):
    label = Button(master, width=width, height=height, text=text, name=name, bg=bg, bd=bd)
    caller.place_element(label, x, y)
    return label

def create_label(caller:object, name:str, master:object, text:str, width:int, height:int, bg:str, bd:int, x:int, y:int):
    label = Label(master, width=width, height=height, text=text, name=name, bg=bg, bd=bd)
    caller.place_element(label, x, y)
    return label

def create_frame(caller:object, name:str, master:object, text, width:int, height:int, bg:str, bd:int, x:int, y:int):
    label = Frame(master, width=width, height=height, text=text, name=name, bg=bg, bd=bd)
    caller.place_element(label, x, y)
    return label


class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("TkBuilder")
        self.resizable(True,True)
        self.geometry('800x700')
        self.minsize(800,700)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind("<Map>", self.unminimised)
        self.bind("<Unmap>", self.minimised)

    def close(self):
        BUILD_WINDOW.destroy()
        self.destroy()

    def unminimised(self,event):
        BUILD_WINDOW.deiconify()
    
    def minimised(self,event):
        BUILD_WINDOW.iconify()

    def compile_WINDOW(self):
        for child,x,y in self.children:
            child.place(x=x, y=y)


class APP_WINDOW(Tk):
    def __init__(self):
        super().__init__()
        self.real_children = []
        self.name = "WINDOW"
        self.load_order = 0
        self.resizable(False,False)
        self.title("Build Window")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.attributes('-topmost', True)
        self.bind("<Map>", self.unminimised)
        self.bind("<Unmap>", self.minimised)

        self.label = create_label(self, "master_label", self, "", 400, 75, 'white', 0, 25, 5)
        self.button = create_button(self, "button", self.label, 1, 10, 2, 'white', 1, 0, 0)
        self.button1 = create_button(self, "button1", self.label, 1, 10, 2, 'white', 1, 100, 100)
        self.button2 = create_button(self, "button2", self.label, 1, 10, 2, 'white', 1, 200, 200)
        self.button3 = create_button(self, "button3", self.label, 1, 10, 2, 'white', 1, 300, 300)

    
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

    def save_json(self):
        if self.winfo_children():
            data = {}
            with open("output.tkbuilt.json", "w") as file:
                for child in self.real_children:
                    data[str(child.winfo_name())] = {
                            "item_type": child.widgetName,
                            "load_order": child.load_order,
                            "master": child.master.name,
                            "bg": child['bg'],
                            "bd": child['bd'],
                            "text": child['text'],
                            "width": child['width'],
                            "height": child['height'],
                            "x": child.winfo_x(),
                            "y": child.winfo_y()
                        }
                dump(data, file)

       
    def destroy(self) -> None:
        self.save_json()
        return super().destroy()
    
    def unminimised(self,event):
        WINDOW.deiconify()
    
    def minimised(self,event):
        WINDOW.iconify()
    
WINDOW = Application()
BUILD_WINDOW = APP_WINDOW()


frame = Frame(WINDOW, bg='gray75', bd=1); frame.pack(anchor="e")
panel = Label(frame, bd=0, width=20, height=40, bg="gray95"); panel.pack(padx=0,pady=0)

def update_build_WINDOW():
    BUILD_WINDOW.geometry("{0}x{1}+{2}+{3}".format(WINDOW.winfo_width() - 250, WINDOW.winfo_height() - 125, WINDOW.winfo_x() + 50, WINDOW.winfo_y() + 50))
    BUILD_WINDOW.after(1, update_build_WINDOW)


BUILD_WINDOW.after(1, update_build_WINDOW)



mainloop()