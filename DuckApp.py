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
        image = Image.open(r"C:\Users\JD Angelo G. Soon\Downloads\33a76bf9-7215-4778-a1e4-ad40d74a0db0.png")
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(300, 300))
        self.logo_photo = ImageTk.PhotoImage(image)

        logo_label = ctk.CTkLabel(self, image=ctk_image, text="", bg_color=PRIMARY_COLOR)
        logo_label.pack(pady=80)

        title = ctk.CTkLabel(self, text="Duck Dash", font=("Courier", 30, "bold"), text_color=TEXT_COLOR)
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
        ctk.CTkLabel(self, text="Welcome to Duck Dash", font=("Courier", 25, "bold"), text_color=TEXT_COLOR).pack(pady=20)
        ctk.CTkLabel(self, text="Select your mode:", font=("Arial", 18)).pack(pady=10)

        ctk.CTkButton(self, text="Register as Rider", command=self.rider_registration).pack(pady=10)
        ctk.CTkButton(self, text="Register as Driver", command=self.driver_registration).pack(pady=10)

        tagline_text ="""Lookin for a Ride?
Book a Ride at DUCK DASH!


Fast as Duck, Quack! Quack! Quack!"""

        tagline = ctk.CTkLabel(self, text=tagline_text, font=("Courier", 18, "bold"), text_color=TEXT_COLOR)
        tagline.pack(padx=10, pady=95)

    def rider_registration(self):
        self.clear_window()
        self.rider_data = {}

        scrollable_frame = ctk.CTkScrollableFrame(self, width=500, height=600)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scrollable_frame, text="Rider Registration", font=("Arial", 20, "bold"), text_color=TEXT_COLOR).pack(pady=10)
        form_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        form_frame.pack(padx=10, pady=10, fill="both", expand=True)

        def create_entry(label_text, row, column):
            label = ctk.CTkLabel(form_frame, text=label_text, text_color=TEXT_COLOR)
            label.grid(row=row, column=column, sticky="w", padx=5)
            entry = ctk.CTkEntry(form_frame, width=150)
            entry.grid(row=row+1, column=column, padx=5, pady=5)
            return entry

        self.rider_data["First Name"] = create_entry("First Name *", 0, 0)
        self.rider_data["Last Name"] = create_entry("Last Name *", 0, 1)
        self.rider_data["Gender"] = create_entry("Gender", 2, 0)
        self.rider_data["Age"] = create_entry("Age", 2, 1)

        address_label = ctk.CTkLabel(form_frame, text="Address", text_color=TEXT_COLOR)
        address_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
        self.rider_data["Address"] = ctk.CTkEntry(form_frame, width=320)
        self.rider_data["Address"].grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        contact_label = ctk.CTkLabel(form_frame, text="Contact Number *", text_color=TEXT_COLOR)
        contact_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=5)
        self.rider_data["Contact Number"] = ctk.CTkEntry(form_frame, width=320)
        self.rider_data["Contact Number"].grid(row=7, column=0, columnspan=2, padx=5, pady=5)

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

        ctk.CTkButton(button_frame, text="Register as Rider", width=280, height=40, command=self.save_rider).pack(pady=10)
        ctk.CTkButton(button_frame, text="Back", command=self.create_home_screen).pack(pady=(0, 10))

    def save_rider(self):
        data_rider = {field: entry.get() for field, entry in self.rider_data.items()}
        missing_fields = []

        for field, entry in self.rider_data.items():
            value = entry.get().strip()
            if not value:
                missing_fields.append(field)
            data_rider[field] = value

        if missing_fields:
            messagebox.showerror("Error", 
                                 f"Please fill in the following required Information:\n{','.join(missing_fields)}")
            return

        rider = Rider(data_rider["First Name"], data_rider["Last Name"], data_rider["Gender"],
                      data_rider["Address"], data_rider["Contact Number"],
                      data_rider.get("GCash Account"), data_rider.get("PayMaya Account"), data_rider.get("PayPal Account"),
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

        scrollable_frame2 = ctk.CTkScrollableFrame(self, width=400, height=500)
        scrollable_frame2.pack(fill="both", expand=True, padx=10, pady=10)

        for field in fields:
            ctk.CTkLabel(scrollable_frame2, text=field + ":", text_color=TEXT_COLOR).pack()
            entry = ctk.CTkEntry(scrollable_frame2, width=250)
            entry.pack()
            self.driver_data[field] = entry

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
