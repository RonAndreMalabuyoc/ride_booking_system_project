import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import csv
from PIL import Image, ImageTk

# Theme & Colors
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

PRIMARY_COLOR = '#fce7a2'
TEXT_COLOR = '#5c3d00'

# Base Classes
class User:
    def __init__(self, first_name, last_name, gender, address, contact_info, age=None):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.address = address
        self.contact_info = contact_info
        self.age = age

class Rider(User):
    def __init__(self, first_name, last_name, gender, address, contact_info,
                 gcash_account=None, paymaya_account=None, paypal_account=None, cod_enabled=True):
        super().__init__(first_name, last_name, gender, address, contact_info)
        self.gcash_account = gcash_account
        self.paymaya_account = paymaya_account
        self.paypal_account = paypal_account
        self.cod_enabled = cod_enabled

class Vehicle:
    def __init__(self, vehicle_type, model, color, plate_number):
        self.vehicle_type = vehicle_type
        self.model = model
        self.color = color
        self.plate_number = plate_number

class Driver(User):
    def __init__(self, first_name, last_name, gender, address, contact_info,
                 vehicle, qualifications=None, join_date=None):
        super().__init__(first_name, last_name, gender, address, contact_info)
        self.vehicle = vehicle
        self.qualifications = qualifications
        self.join_date = join_date or datetime.now().isoformat()

# GUI App
class DuckDashApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Duck Dash")
        self.geometry("400x550")
        self.configure(fg_color=PRIMARY_COLOR)
        self.after(100, self.show_logo_screen)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_logo_screen(self):
        self.clear_window()
        image = Image.open(r"Ride booking system project\ride_booking_system_project\Banana_duck_logo_transparent.png")
        image = image.resize((200, 200), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(image)

        logo_label = ctk.CTkLabel(self, image=self.logo_photo, text="", bg_color=PRIMARY_COLOR)
        logo_label.pack(pady=40)

        title = ctk.CTkLabel(self, text="Duck Dash", font=("Arial", 22, "bold"), text_color=TEXT_COLOR)
        title.pack()

        self.attributes("-alpha", 0.0)
        self.fade_in(0.0, self.start_main_menu)

    def fade_in(self, alpha, callback=None):
        alpha = round(alpha + 0.05, 2)
        if alpha <= 1.0:
            self.attributes("-alpha", alpha)
            self.after(50, lambda: self.fade_in(alpha, callback))
        else:
            self.after(800, callback)

    def start_main_menu(self):
        self.attributes("-alpha", 1.0)
        self.create_home_screen()

    def create_home_screen(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Welcome to Duck Dash", font=("Arial", 18, "bold"), text_color=TEXT_COLOR).pack(pady=20)
        ctk.CTkLabel(self, text="Select your mode:", font=("Arial", 14)).pack(pady=10)

        ctk.CTkButton(self, text="Register as Rider", command=self.rider_registration).pack(pady=10)
        ctk.CTkButton(self, text="Register as Driver", command=self.driver_registration).pack(pady=10)

    def rider_registration(self):
        self.clear_window()
        self.rider_data = {}
        fields = ["First Name", "Last Name", "Gender", "Age", "Address", "Contact Number",
                  "GCash Account", "PayMaya Account", "PayPal Account"]

        for field in fields:
            ctk.CTkLabel(self, text=field + ":", text_color=TEXT_COLOR).pack()
            entry = ctk.CTkEntry(self, width=250)
            entry.pack()
            self.rider_data[field] = entry

        self.cod_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self, text="Enable Cash on Delivery", variable=self.cod_var).pack(pady=10)

        ctk.CTkButton(self, text="Submit", command=self.save_rider).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=self.create_home_screen).pack()

    def save_rider(self):
        data = {field: entry.get() for field, entry in self.rider_data.items()}
        rider = Rider(data["First Name"], data["Last Name"], data["Gender"],
                      data["Address"], data["Contact Number"],
                      data.get("GCash Account"), data.get("PayMaya Account"), data.get("PayPal Account"),
                      self.cod_var.get())

        with open("riders.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([rider.first_name, rider.last_name, rider.gender, rider.address, rider.contact_info,
                             rider.gcash_account, rider.paymaya_account, rider.paypal_account, rider.cod_enabled])

        messagebox.showinfo("Success", "Rider registered successfully!")
        self.create_home_screen()

    def driver_registration(self):
        self.clear_window()
        self.driver_data = {}
        fields = ["First Name", "Last Name", "Gender", "Age", "Address", "Contact Number",
                  "Vehicle Type", "Vehicle Model", "Vehicle Color", "Plate Number", "Qualifications"]

        for field in fields:
            ctk.CTkLabel(self, text=field + ":", text_color=TEXT_COLOR).pack()
            entry = ctk.CTkEntry(self, width=250)
            entry.pack()
            self.driver_data[field] = entry

        ctk.CTkButton(self, text="Submit", command=self.save_driver).pack(pady=10)
        ctk.CTkButton(self, text="Back", command=self.create_home_screen).pack()

    def save_driver(self):
        d = {field: entry.get() for field, entry in self.driver_data.items()}
        vehicle = Vehicle(d["Vehicle Type"], d["Vehicle Model"], d["Vehicle Color"], d["Plate Number"])
        driver = Driver(d["First Name"], d["Last Name"], d["Gender"], d["Address"],
                        d["Contact Number"], vehicle, d["Qualifications"])

        with open("drivers.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([driver.first_name, driver.last_name, driver.gender, driver.address, driver.contact_info,
                             driver.vehicle.vehicle_type, driver.vehicle.model, driver.vehicle.color, driver.vehicle.plate_number,
                             driver.qualifications, driver.join_date])

        messagebox.showinfo("Success", "Driver registered successfully!")
        self.create_home_screen()

if __name__ == '__main__':
    app = DuckDashApp()
    app.mainloop()
