from tkinter import *
import sqlite3

import add_menu
import remove_menu
import rent_menu
import return_menu
import schedule_menu
import settings_menu


class BookRentalSystem:
    rent_fee = 200
    late_fee = 25

    def __init__(self, window):
        self.main_window = window
        self.main_window.title("Book Rental Mangement System")
        self.main_window.configure(bg="#f2eecb")
        # ==========   Places the window at the center   ==========
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # ========== Places the window at the center END ==========

        # Sets up the widgets
        self.set_interface()
        # Initializes the database
        self.init_db()

    def set_interface(self):
        # Header
        main_header = Label(text="BOOK RENTAL MANAGEMENT SYSTEM", font=("Segoe UI", 20, "bold"))
        main_header.configure(bg="#f2eecb")
        main_header.place(x=140, y=100)

        # Buttons
        rent_button = Button(text="RENT A BOOK", font=("Segoe UI", 12, "bold"), width=49)
        rent_button.configure(command=self.rent_book)
        rent_button.place(x=140, y=250)

        return_button = Button(text="RETURN A BOOK", font=("Segoe UI", 12, "bold"), width=49)
        return_button.configure(command=self.return_book)
        return_button.place(x=140, y=310)

        add_button = Button(text="ADD BOOK", font=("Segoe UI", 12, "bold"), width=49)
        add_button.configure(command=self.add_book)
        add_button.place(x=140, y=370)

        remove_book = Button(text="REMOVE BOOK", font=("Segoe UI", 12, "bold"), width=49)
        remove_book.configure(command=self.remove_book)
        remove_book.place(x=140, y=430)

        sched_button = Button(text="SHOW RENT SCHEDULE", font=("Segoe UI", 12, "bold"), width=49)
        sched_button.configure(command=self.see_sched)
        sched_button.place(x=140, y=490)

        settings_button = Button(text="Settings", font=("Segoe UI", 9, "bold"), width=7, height=2)
        settings_button.configure(command=self.settings)
        settings_button.place(x=10, y=550)

    def rent_book(self):
        rent_menu_window = rent_menu.RentBookInterface(self.main_window)
        rent_menu_window.rent_window.wait_window()

    def return_book(self):
        return_menu_window = return_menu.ReturnBookInterface(self.main_window, None)
        return_menu_window.return_window.wait_window()

    def add_book(self):
        add_menu_window = add_menu.AddBookInterface(self.main_window)
        add_menu_window.add_window.wait_window()

    def remove_book(self):
        remove_menu_window = remove_menu.RemoveBookInterface(self.main_window)
        remove_menu_window.remove_window.wait_window()

    def see_sched(self):
        schedule_menu_window = schedule_menu.ScheduleInterface(self.main_window)
        schedule_menu_window.schedule_window.wait_window()

    def settings(self):
        settings_menu_window = settings_menu.SettingsInterface(self.main_window)
        settings_menu_window.settings_window.wait_window()

    @staticmethod
    def init_db():
        db = sqlite3.connect("BOOK RENTAL.db")
        script = db.cursor()

        script.execute('''CREATE TABLE IF NOT EXISTS Renter (
                           Renter_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Last_Name TEXT NOT NULL, First_Name TEXT
                         , Middle_Initial TEXT
                         , Phone_Number TEXT, Email TEXT
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Author(
                           Author_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Author_Name TEXT NOT NULL
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Payment (
                           Payment_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Payment_Amount INTEGER, Payment_Date TEXT
                         , Payment_Mode TEXT
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS LateFee (
                           LateFee_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Fee INTEGER, Days_Late INTEGER
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Book (
                           Book_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Book_Name TEXT NOT NULL, Author_ID TEXT
                         , FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID)
                        )''')
        script.execute('''CREATE TABLE IF NOT EXISTS Schedule (
                           Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT
                         , Payment_ID TEXT, Renter_ID TEXT
                         , Book_ID TEXT, Rent_Date TEXT
                         , Return_Date TEXT, isCompleted BOOL
                         , FOREIGN KEY (Payment_ID) REFERENCES Payment(Payment_ID)
                         , FOREIGN KEY (Renter_ID) REFERENCES Renter(Renter_ID)
                         , FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID)
                        )''')
        db.commit()
        script.close()
        db.close()


def main():
    main_window = Tk()
    BookRentalSystem(main_window)

    main_window.mainloop()


if __name__ == "__main__":
    main()