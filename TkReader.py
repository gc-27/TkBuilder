from tkinter import Tk, mainloop, Button, Label, Frame
from json import load

"""
Written by gamerchungus27
"""

version:float = 1.0



class FileExtensionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("FileExtensionError: Provided file is not a .tkbuilt.json file")

class FileNotLoadedError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("FileNotLoadedError: You cannot read a file that has not been loaded.")


class TkReader:
    """
    The base class for reading, loading and building TkBuilt files.
    \n
    Functions: 
    \n
    load_file() -> Loads a file from the given path.
    \n
    read_file() -> Reads the file once loaded. Can only be called if load_file() returns a valid response.
    \n
    BUILD() -> Builds the window for use, and will return all mutable variables in a dictionary.
    """

    def __init__(self):
        self.__elements = []
        self.file_loaded = False

    @property
    def version(self):
        print(f"You are currently running TkReader Version {version}.")
      
    def _build_button(self, name: str, properties: dict):
        setattr(self, name, 
            Button(master=getattr(self, properties['master']), 
                bg=properties['bg'], 
                bd=properties['bd'],
                text=properties['text'], 
                width=properties['width'], 
                height=properties['height'])
            )
        self._add_element(name, getattr(self, name), properties['x'], properties['y'])

    def _build_label(self, name: str, properties: dict):
        setattr(self, name, 
            Label(master=getattr(self, properties['master']), 
                bg=properties['bg'], 
                bd=properties['bd'],
                text=properties['text'], 
                width=properties['width'], 
                height=properties['height'])
            )
        self._add_element(name, getattr(self, name), properties['x'], properties['y'])
    
    def _build_frame(self, name: str, properties: dict):
        setattr(self, name, 
            Frame(master=getattr(self, properties['master']), 
                bg=properties['bg'],
                bd=properties['bd'],
                width=properties['width'], 
                height=properties['height'],))
        self._add_element(name, getattr(self, name), properties['x'], properties['y'])

    def _add_element(self, name: str, item: object, x: int, y: int):
        self.__elements.append((name, item, x, y))

    def _init_window(self):
        self.WINDOW = Tk()
        self.WINDOW.title('Built Window')
        self.WINDOW.update()
        
    def load_file(self, file: str):
        """
        Attempts to load a JSON file with the path given. 
        If the file is not found, it will exit.
        """
        if file.split('.')[-2:] != ['tkbuilt', 'json']:
            raise FileExtensionError


        try:
            self.file_loaded = True
            self.dict = load(open(file, "r"))
            return 0
        except FileNotFoundError:
            print(f"File not found: {file}. Please make sure your path is correct.")
            return 1

    def read_file(self):
        """
        Reads the provided file, if it is a valid format.
        """
        if self.file_loaded:
            self._init_window()
            
            try:
                highest_loading_order = -1
                filtered_items = []
                for name, properties in self.dict.items():  #Loops through the individual elements and sorts them by their loading order.
                    if properties["load_order"] > highest_loading_order:
                        highest_loading_order = properties["load_order"]
                        filtered_items.append([])
                    filtered_items[properties['load_order']].append({"name": name, "properties": properties}) 



                for value in filtered_items: #Loops through sorted list of elements and procedurally builds them based on their loading order.
                    for item in value:
                        match item['properties']['item_type']:
                            case 'button':
                                self._build_button(item['name'], item['properties'])
                            case 'label':
                                self._build_label(item['name'], item['properties'])
                            case 'frame':
                                self._build_frame(item['name'], item['properties'])
                            case _:
                                print(f"{item['properties']['item_type']} is not a proper Tk object.")


                

                return 0
            except AttributeError as e:
                print(e)
                print("Your tkbuilt file is improperly formatted. If you believe this a bug, please report on the Github page. See: ####INSERT LINK HERE####")
                return 1
        else:
            raise FileNotLoadedError

    
    def BUILD(self) -> dict:
        """
        Compiles the Tkinter window and returns all mutable variables in a dict.
        """
        for name,item,x,y in self.__elements:
            setattr(self, name, item)
            item.place(x=x, y=y)


def main():
    WINDOW = TkReader()
    WINDOW.load_file("output.tkbuilt.json")
    WINDOW.read_file()
    WINDOW.BUILD()
    WINDOW.version




if __name__ == '__main__':
    main()
    mainloop()
    
