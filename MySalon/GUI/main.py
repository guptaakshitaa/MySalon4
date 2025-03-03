from tkinter import *
#import Welcome
from lib.Welcome import *
from lib.Main_window import *
from lib.user_authentication import *


class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Page")
        self.root.geometry("300x200")
        
        Label(self.root, text="Welcome", font=("Arial", 16)).pack(pady=20)
        
        Button(self.root, text="I am a Customer!", command=self.open_user_side).pack(pady=5)
        Button(self.root, text="I am a Service Provider!", command=self.open_service_provider_side).pack(pady=5)
    
    def open_user_side(self): 
        self.root.destroy()
        root = Tk()
        app = UserAuthentication(root)
        root.mainloop()
    
    def open_service_provider_side(self):
        self.root.destroy()
        root = Tk()
        app = MysalonApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = HomePage(root)
    root.mainloop()
