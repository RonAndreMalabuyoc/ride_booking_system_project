import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import csv
import os
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

class Passenger(User):
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
        image = Image.open(r"C:\Users\maria\OneDrive\Documents\Desktop\ride_booking_system_project\Banana_duck_logo_transparent.png")
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(300, 300))
        self.logo_photo = ImageTk.PhotoImage(image)

        logo_label = ctk.CTkLabel(self, image=ctk_image, text="", bg_color=PRIMARY_COLOR)
        logo_label.pack(pady=80)

        title = ctk.CTkLabel(self, text="Duck Dash", font=("Courier", 30, "bold"), text_color=TEXT_COLOR)
        title.pack()

        self.attributes("-alpha", 0.0)
        self.fade_in(0.0, self.show_login_screen)

    def fade_in(self, alpha, callback=None):
        alpha = round(alpha + 0.05, 2)
        if alpha <= 1.0:
            self.attributes("-alpha", alpha)
            self.after(50, lambda: self.fade_in(alpha, callback))
        else:
            self.after(800, callback)

    def show_login_screen(self):
        self.clear_window()

        tagline_text ="""Lookin for a Ride?
Book a Ride at DUCK DASH!


Fast as Duck, Quack! Quack! Quack!"""

        tagline = ctk.CTkLabel(self, text=tagline_text, font=("Courier", 18, "bold"), text_color=TEXT_COLOR)
        tagline.pack(padx=10, pady=35)

        ctk.CTkLabel(self, text="Login", font=("Arial", 20, "bold"), text_color=TEXT_COLOR).pack(pady=20)

        username_label = ctk.CTkLabel(self, text="Username", text_color=TEXT_COLOR)
        username_label.pack()
        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(self, text="Password", text_color=TEXT_COLOR)
        password_label.pack()
        self.password_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_entry.pack(pady=5)

        ctk.CTkButton(self, text="Login", command=self.verify_login).pack(pady=10)
        ctk.CTkButton(self, text="Register Now!", command=self.create_home_screen).pack(pady=5)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if os.path.exists("users.csv"):
            with open("users.csv", mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2 and row[0] == username and row[1] == password:
                        self.start_main_menu()
                        return

        messagebox.showerror("Login Failed", "Invalid username or password. Please register if you don't have an account.")

    def start_main_menu(self):
        self.attributes("-alpha", 1.0)
        self.create_home_screen()

    def create_home_screen(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Welcome to Duck Dash", font=("Courier", 28, "bold"), text_color=TEXT_COLOR).pack(pady=40)
        ctk.CTkLabel(self, text="Select your mode:", font=("Arial", 18)).pack(pady=10)

        ctk.CTkButton(self, text="   Register as Passenger   ",font=("Arial", 18), command=self.passenger_registration).pack(pady=(20,10))
        ctk.CTkButton(self, text="      Register as Driver      ", font=("Arial", 18), command=self.driver_registration).pack(pady=(20,10))

        ctk.CTkButton(self, text="Cancel Registration", command=self.show_login_screen).pack(pady=(20, 10))

    def passenger_registration(self):
        self.clear_window()
        self.passenger_data = {}

        scrollable_frame = ctk.CTkScrollableFrame(self, width=500, height=600)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scrollable_frame, text="Passenger Registration", font=("Arial", 20, "bold"), text_color=TEXT_COLOR).pack(pady=10)
        form_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        form_frame.pack(padx=10, pady=10, fill="both", expand=True)

        def create_entry(label_text, row, column):
            label = ctk.CTkLabel(form_frame, text=label_text, text_color=TEXT_COLOR)
            label.grid(row=row, column=column, sticky="w", padx=5)
            entry = ctk.CTkEntry(form_frame, width=150)
            entry.grid(row=row+1, column=column, padx=5, pady=5)
            return entry

        self.passenger_data["First Name"] = create_entry("First Name *", 0, 0)
        self.passenger_data["Last Name"] = create_entry("Last Name *", 0, 1)
        self.passenger_data["Gender"] = create_entry("Gender *", 2, 0)
        self.passenger_data["Age"] = create_entry("Age *", 2, 1)

        address_label = ctk.CTkLabel(form_frame, text="Address *", text_color=TEXT_COLOR)
        address_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
        self.passenger_data["Address"] = ctk.CTkEntry(form_frame, width=320)
        self.passenger_data["Address"].grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        contact_label = ctk.CTkLabel(form_frame, text="Contact Number *", text_color=TEXT_COLOR)
        contact_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=5)
        self.passenger_data["Contact Number"] = ctk.CTkEntry(form_frame, width=320)
        self.passenger_data["Contact Number"].grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        payment_label = ctk.CTkLabel(form_frame, text="Payment Methods *", text_color=TEXT_COLOR)
        payment_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)

        self.gcash_var = ctk.BooleanVar()
        self.paymaya_var = ctk.BooleanVar()
        self.paypal_var = ctk.BooleanVar()
        self.cod_var = ctk.BooleanVar(value=True)

        self.payment_method = ctk.StringVar(value="Cash")

        ctk.CTkRadioButton(form_frame, text="GCash", variable=self.payment_method, value="GCash").grid(row=9, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame, text="PayMaya", variable=self.payment_method, value="PayMaya").grid(row=10, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame, text="PayPal", variable=self.payment_method, value="PayPal").grid(row=11, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame, text="Cash", variable=self.payment_method, value="Cash").grid(row=12, column=0, sticky="w", padx=10, pady=(0, 10))

        button_frame = ctk.CTkFrame(scrollable_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Register as Passenger", width=280, height=40, command=self.save_passenger).pack(pady=10)
        ctk.CTkButton(button_frame, text="Back", command=self.create_home_screen).pack(pady=(0, 10))

    def save_passenger(self):
        data_passenger = {field: entry.get() for field, entry in self.passenger_data.items()}
        missing_fields = []

        for field, entry in self.passenger_data.items():
            value = entry.get().strip()
            if not value:
                missing_fields.append(field)
            data_passenger[field] = value

        if missing_fields:
            messagebox.showerror("Error", 
                                 f"Please fill in the following required Information:\n{','.join(missing_fields)}")
            return

        passenger = Passenger(data_passenger["First Name"], data_passenger["Last Name"], data_passenger["Gender"],
                      data_passenger["Address"], data_passenger["Contact Number"],
                      data_passenger.get("GCash Account"), data_passenger.get("PayMaya Account"), data_passenger.get("PayPal Account"),
                      self.cod_var.get())

        with open("passenger.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([passenger.first_name, passenger.last_name, passenger.gender, passenger.address, passenger.contact_info,
                             passenger.gcash_account, passenger.paymaya_account, passenger.paypal_account, passenger.cod_enabled])

        messagebox.showinfo("Success", "Passenger Registered Successfully!")
        self.create_home_screen()

    def driver_registration(self):
        self.clear_window()
        self.driver_data = {}
        fields = ["First Name", "Last Name", "Gender", "Age", "Contact Number",
                  "Vehicle Type", "Vehicle Model", "Vehicle Color", "Plate Number", "Qualifications"]

        scrollable_frame2 = ctk.CTkScrollableFrame(self, width=500, height=600)
        scrollable_frame2.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scrollable_frame2, text="Drivers Registration", font=("Arial", 20, "bold"), text_color=TEXT_COLOR).pack(pady=10)
        form_frame = ctk.CTkFrame(scrollable_frame2, fg_color="transparent")
        form_frame.pack(padx=10, pady=10, fill="both", expand=True)

        def create_entry(label_text, row, column):
            label = ctk.CTkLabel(form_frame, text=label_text, text_color=TEXT_COLOR)
            label.grid(row=row, column=column, sticky="w", padx=5)
            entry = ctk.CTkEntry(form_frame, width=150)
            entry.grid(row=row+1, column=column, padx=5, pady=5)
            return entry

        self.driver_data["First Name"] = create_entry("First Name *", 0, 0)
        self.driver_data["Last Name"] = create_entry("Last Name *", 0, 1)
        self.driver_data["Gender"] = create_entry("Gender *", 2, 0)
        self.driver_data["Age"] = create_entry("Age *", 2, 1)

        contact_label = ctk.CTkLabel(form_frame, text="Contact Number *", text_color=TEXT_COLOR)
        contact_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
        self.driver_data["Contact Number"] = ctk.CTkEntry(form_frame, width=320)
        self.driver_data["Contact Number"].grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.driver_data["Vehicle Type"] = create_entry("Vehicle Type *", 7, 0)
        self.driver_data["Vehicle Model"] = create_entry("Vehicle Model *", 7, 1)
        self.driver_data["Vehicle Color"] = create_entry("Vehicle Color *", 9, 0)
        self.driver_data["Plate Number"] = create_entry("Plate Number *", 9, 1 )

        button_frame = ctk.CTkFrame(scrollable_frame2)
        button_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Submit", command=self.save_driver).pack(pady=10)
        ctk.CTkButton(button_frame, text="Back", command=self.create_home_screen).pack()

    def save_driver(self):
        data_driver = {field: entry.get() for field, entry in self.driver_data.items()}
        missing_fields = []

        for field, entry in self.driver_data.items():
            value = entry.get().strip()
            if not value:
                missing_fields.append(field)
            data_driver[field] = value

        if missing_fields:
            messagebox.showerror("Error", 
                                 f"Please fill in the following required Information:\n{','.join(missing_fields)}")
            return

        vehicle = Vehicle(data_driver["Vehicle Type"], data_driver["Vehicle Model"], data_driver["Vehicle Color"], data_driver["Plate Number"])
        driver = Driver(data_driver["First Name"], data_driver["Last Name"], data_driver["Gender"], data_driver["Address"],
                        data_driver["Contact Number"], vehicle, data_driver["Qualifications"])

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