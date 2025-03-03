from tkinter import *
from tkinter import messagebox
from lib.Main_window import MysalonApp

class WelcomeScreen:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id  # Store user_id
        self.root.geometry("600x400")
        self.root.configure(background="#793633")  # Light red background
        self.root.title("Welcome to Mysalon")

        Label(self.root, text="Welcome to Mysalon", font=("Arial", 24, "bold"), bg="#793633").pack(pady=20)

        # Creating buttons
        btn1 = Button(self.root, text="Find a Salon", font=("Arial", 14), bg="#fed0d1", command=self.open_main_app)
        btn1.pack(pady=10, ipadx=20, ipady=5)

        btn2 = Button(self.root, text="Look in preferred area", font=("Arial", 14), command=self.open_main_app)
        btn2.pack(pady=10, ipadx=20, ipady=5)

        btn3 = Button(self.root, text="Look based on availability date", font=("Arial", 14), command=self.open_main_app)
        btn3.pack(pady=10, ipadx=20, ipady=5)

        btn4 = Button(self.root, text="Take me to Home Page", font=("Arial", 14), command=self.open_main_app)
        btn4.pack(pady=10, ipadx=20, ipady=5)

    def open_main_app(self):
        self.root.destroy()  # Close the welcome screen
        new_root = Tk()  # Create a new Tkinter window
        app = MysalonApp(new_root, self.user_id)  # Pass user_id correctly
        new_root.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = WelcomeScreen(root, user_id=1)  # Pass user_id when initializing
    root.mainloop()
