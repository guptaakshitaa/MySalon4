from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector #type:ignore
from lib.Main_window import MysalonApp
from lib.Welcome import WelcomeScreen 

class UserAuthentication:
    def __init__(self, root):
        self.root = root
        self.root.geometry('400x400')
        self.root.configure(background='#fed0d1')  # Light red background for root
        self.root.title("User Authentication")

        # Connect to MySQL database
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='new12345',
                database='salonMumbai'
                )
            print("Connected to MySQL database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Database Connection Error", f"Error connecting to the database: {err}")
            return

        # Create a frame to hold the elements
        self.frame = Frame(self.root, bg='#fed0d1')  # Light red background for frame
        self.frame.pack(pady=20, fill=BOTH, expand=True)
        Label(self.frame, text='Welcome to Mysalon', bg='#fed0d1', fg='#793633',font=('arial', 24, 'bold')).pack(pady=(0, 10))
        # Label for the title
        Label(self.frame, text='Beauty at Your Fingertips', bg='#fed0d1', fg='#793633', font=('Brush Script MT', 16, 'bold', 'italic')).pack(pady=(0, 9))

        # Login Section
        Label(self.frame, text='Login', bg='#fed0d1', fg='#793633',font=('arial', 18, 'bold')).pack()
        self.username_label = Label(self.frame, text='Username', fg='#793633',bg='#fed0d1', font=('arial', 12))
        self.username_label.pack(pady=(10, 5))
        self.username_entry = Entry(self.frame, font=('arial', 12))
        self.username_entry.pack(pady=5)

        self.password_label = Label(self.frame, text='Password', fg='#793633',bg='#fed0d1', font=('arial', 12))
        self.password_label.pack(pady=(10, 5))
        self.password_entry = Entry(self.frame, show='*', font=('arial', 12))
        self.password_entry.pack(pady=5)

        self.login_button = Button(self.frame, text='Login', bg='#F0F8FF', font=('arial', 12), command=self.login)
        self.login_button.pack(pady=10)

        # Signup Button
        self.signup_button = Button(self.frame, text='Signup', bg='#F0F8FF', font=('arial', 12), command=self.open_signup_window)
        self.signup_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == '' or password == '':
            messagebox.showerror("Error", "All fields are required!")
        else:
            try:
                c = self.conn.cursor()
                query = "SELECT user_id,username,password FROM users WHERE username = %s AND password = %s"
                c.execute(query, (username, password))
                user = c.fetchone()

                if user:
                    self.user_id=user[0]
                    messagebox.showinfo("Success", "Login Successful!")
                    self.root.destroy()  # Close the login window

                    start_zomato_app(self.user_id)

                
                else:
                    messagebox.showerror("Error", "Invalid username or password")
            except Exception as e:
                print(f"Error during login: {e}")
                messagebox.showerror("Error", "An error occurred during login")

    def open_signup_window(self):
        signup_window = Toplevel(self.root)
        signup_window.geometry('400x400')
        signup_window.configure(background='#fed0d1')  # Light red background for signup window
        signup_window.title("Signup")

        Label(signup_window, text='Signup', bg='#fed0d1', font=('arial', 20, 'bold')).pack(pady=(10, 10))

        # New Username
        Label(signup_window, text='New Username', bg='#fed0d1', font=('arial', 12)).pack(pady=(10, 5))
        new_username_entry = Entry(signup_window, font=('arial', 12))
        new_username_entry.pack(pady=5)

        # New Password
        Label(signup_window, text='New Password', bg='#fed0d1', font=('arial', 12)).pack(pady=(10, 5))
        new_password_entry = Entry(signup_window, show='*', font=('arial', 12))
        new_password_entry.pack(pady=5)

        # Email
        Label(signup_window, text='Email', bg='#fed0d1', font=('arial', 12)).pack(pady=(10, 5))
        email_entry = Entry(signup_window, font=('arial', 12))
        email_entry.pack(pady=5)

        # Profile Info
        Label(signup_window, text='Other Profile Info', bg='#fed0d1', font=('arial', 12)).pack(pady=(10, 5))
        other_profile_info_entry = Entry(signup_window, font=('arial', 12))
        other_profile_info_entry.pack(pady=5)

        def signup():
            new_username = new_username_entry.get()
            new_password = new_password_entry.get()
            email = email_entry.get()
            other_profile_info = other_profile_info_entry.get()

            print(f"Signup attempt with Username: {new_username}, Password: {new_password}, Email: {email}, Other Profile Info: {other_profile_info}")

            if new_username == '' or new_password == '' or email == '' or other_profile_info == '':
                messagebox.showerror("Error", "All fields are required!")
            else:
                try:
                    c = self.conn.cursor()
                    # Check if the username already exists
                    query = "SELECT * FROM users WHERE username = %s"
                    c.execute(query, (new_username,))
                    existing_user = c.fetchone()

                    if existing_user:
                        print(f"Username {new_username} already exists.")
                        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
                    else:
                        # Insert new user into database
                        insert_query = "INSERT INTO users (username, password, email, other_profile_info) VALUES (%s, %s, %s, %s)"
                        c.execute(insert_query, (new_username, new_password, email, other_profile_info))
                        self.conn.commit()
                        print(f"Inserted user: {new_username}")
                        messagebox.showinfo("Success", "Signup Successful! You can now enjoy Mysalon.")
                        signup_window.destroy()
                        self.root.destroy()
                        start_zomato_app()
                except mysql.connector.Error as err:
                    print(f"MySQL Error during signup: {err}")
                    messagebox.showerror("Error", f"MySQL Error during signup: {err}")
                except Exception as e:
                    print("General Error during signup:")
                    #messagebox.showerror("Error", f"An error occurred during signup: {}")

        signup_button = Button(signup_window, text='Signup', bg='#F0F8FF', font=('arial', 12), command=signup)
        signup_button.pack(pady=20)
        
       

def start_zomato_app(user_id):
    root = Tk()
    app = WelcomeScreen(root,user_id)
    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = UserAuthentication(root)
    root.mainloop()

