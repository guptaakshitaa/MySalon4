from tkinter import *
from tkinter import messagebox, ttk
from config.database import get_database_connection
from controllers.salon_controller import SalonController


class MysalonApp:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.geometry('879x488')
        self.root.configure(background='#fed0d1')  # Light red background
        self.root.title("MySalon - Home")
        self.root.state('zoomed')

        # Database connection
        self.conn = get_database_connection()
        self.salon_controller = SalonController()

        # UI Setup
        self.setup_ui()

        # Display Top Salons on Startup
        self.display_top_salons()

    def setup_ui(self):
        """Sets up the UI layout."""
        self.frame = Frame(self.root, bg='#fed0d1')
        self.frame.pack(pady=20, fill=BOTH, expand=True)

        Label(self.frame, text='MySalon', bg='#fed0d1', fg = '#793633', font=('Times New Roman', 40, 'bold')).pack(pady=(0, 10))

        # Search Section
        self.setup_search_section()

        # Buttons
        self.setup_buttons()

        # Results Section with Scrollable Canvas
        self.setup_results_section()

    def setup_search_section(self):
        """Creates search bar with dropdown."""
        self.search_frame = Frame(self.frame, bg='#fed0d1')
        self.search_frame.pack(pady=(0, 10))

        Label(self.search_frame, text='SEARCH:', bg='#fed0d1', fg = '#793633', font=('Times New Roman', 20, 'bold')).pack(side=LEFT)

        self.selected_option = StringVar(value="Name")  # Default search type
        self.dropdown = ttk.Combobox(self.search_frame, textvariable=self.selected_option,
                                     values=["Name of Salon", "Services", "Location"], state="readonly")
        self.dropdown.pack(side=LEFT, padx=5)

        self.search_bar = Entry(self.search_frame, font=('Arial', 20), width=30)
        self.search_bar.pack(side=LEFT, padx=5)

        self.search_button = Button(self.search_frame, text='Search 🔎', bg='#800000', font=('Arial', 15),
                                    command=self.search)
        self.search_button.pack(side=LEFT)

    def setup_buttons(self):
        """Creates main action buttons."""
        self.button_frame = Frame(self.frame, bg='#fed0d1')
        self.button_frame.pack(pady=10)

        Button(self.button_frame, text='Book Appointment', bg='#800000', font=('Arial', 15),
               command=self.display_top_salons).pack(side=LEFT, padx=10)

        Button(self.button_frame, text='View History 🔁', bg='#800000', font=('Arial', 15),
               command=self.view_history).pack(side=LEFT, padx=10)

        Button(self.root, text='❤️ YOU ❤️', bg='#800000', font=('Arial', 15), command=self.view_profile).place(
            relx=1.0, x=-10, y=10, anchor='ne')

    def setup_results_section(self):
        """Creates the scrollable results section."""
        self.canvas = Canvas(self.frame, bg='#fed0d1')
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.results_frame = Frame(self.canvas, bg='#fed0d1')
        self.results_frame_id = self.canvas.create_window((0, 0), window=self.results_frame, anchor='nw')

        self.frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.results_frame_id, width=event.width)

    def search(self):
        """Handles the salon search functionality."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        search_query = self.search_bar.get().strip()
        search_filter = self.selected_option.get().lower()

        if not search_query:
            messagebox.showinfo("Error", "Please enter a search term.")
            return

        results = self.salon_controller.search_salons(search_query, search_filter)

        if results:
            for salon in results:
                self.display_salon_result(salon)
        else:
            Label(self.results_frame, text="No results found", fg="red").pack()

    def display_top_salons(self):
        """Displays top-rated salons."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        top_salons = self.salon_controller.get_top_salons()
        for salon in top_salons:
            self.display_salon_result(salon)

    def display_salon_result(self, salon):
        """Displays an individual salon result."""
        result_frame = Frame(self.results_frame, bg='#800000', padx=10, pady=10, relief=RAISED, bd=2)
        result_frame.pack(fill=X, pady=5, padx=20)

        name_label = Label(result_frame, text=salon.name, bg='#800000', font=('Arial', 15))
        name_label.pack(side=LEFT, padx=10)

        info_label = Label(result_frame, text=f"({salon.rating} ⭐) {salon.category} - {salon.address}",
                           bg='#800000', font=('Arial', 12))
        info_label.pack(side=LEFT)

        Button(result_frame, text='View Services', bg='#FF6666', font=('Arial', 12),
               command=lambda: self.view_salon_services(salon)).pack(side=RIGHT, padx=10)

    def view_salon_services(self, salon):
        """Opens a window displaying the services of a selected salon."""
        messagebox.showinfo("Salon Services", f"Displaying services for {salon.name}")

    def view_history(self):
        """Opens the order history window."""
        messagebox.showinfo("Order History", "Displaying past appointments.")

    def view_profile(self):
        """Opens the user profile window."""
        messagebox.showinfo("User Profile", "Displaying user information.")


if __name__ == "__main__":
    root = Tk()
    app = MysalonApp(root, user_id=1)
    root.mainloop()
