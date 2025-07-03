from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from tkintermapview import TkinterMapView
import tkinter as tk
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
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "Banana_duck_logo_transparent.png")
DUCK_INTRO_PATH = os.path.join(os.path.dirname(__file__), "Duck_app_Intro.wav")
PASSENGERS_PATH = os.path.join(os.path.dirname(__file__), "passenger.csv")
DRIVERS_PATH = os.path.join(os.path.dirname(__file__), "drivers.csv")
BOOK_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "book_button.png")
BOOKINGS_FILE = os.path.join(os.path.dirname(__file__), "bookings.csv")

# Files (.png, .wav, .csv) should now need to be in the same folder as DuckApp.py
# Running the program again will create new .csv files since old ones are in C:\Users\<Name of Computer>

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

    def clear_window(self):                         # Reusable Code
        for widget in self.winfo_children():
            widget.destroy()
            
# ====== STARTING FLUFF SCREEN ======

    def show_logo_screen(self):
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(DUCK_INTRO_PATH)
        pygame.mixer.music.play()  # loop to keep playing during fade

        self.clear_window()
        image = Image.open(IMAGE_PATH)
        ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(300, 300))
        self.logo_photo = ImageTk.PhotoImage(image)

        logo_label = ctk.CTkLabel(self, image=ctk_image, text="", bg_color=PRIMARY_COLOR)
        logo_label.pack(pady=80)

        title = ctk.CTkLabel(self, text="Duck Dash", font=("Courier", 30, "bold"), text_color=TEXT_COLOR)
        title.pack()

        self.attributes("-alpha", 0.0)
        self.fade_in(0.0, lambda: (pygame.mixer.music, self.show_start_screen()))

    def fade_in(self, alpha, callback=None):
        import pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(DUCK_INTRO_PATH)
            pygame.mixer.music.play()
        alpha = round(alpha + 0.05, 2)
        if alpha <= 1.0:
            self.attributes("-alpha", alpha)
            self.after(50, lambda: self.fade_in(alpha, callback))
        else:
            self.after(800, callback)

# ====== Start Screen ======

    def show_start_screen(self):
        self.clear_window()
        # Ensure window is visible after logout
        self.attributes("-alpha", 1.0)
        print("[DEBUG] show_start_screen called")

        tagline_text = """Lookin for a Ride?
Book a Ride at DUCK DASH!

Fast as Duck, Quack! Quack! Quack!"""
        tagline = ctk.CTkLabel(self, text=tagline_text, font=("Courier", 14, "bold"), text_color=TEXT_COLOR, justify="center")
        tagline.pack(pady=20)

        ctk.CTkButton(self, text="Login Type", command=self.create_login_screen).pack(pady=5)
        ctk.CTkButton(self, text="Register Now!", command=self.create_register_screen).pack(pady=5)

    def verify_login_passenger(self):                     # Login Button Functionality
        username = self.username_entry.get()
        password = self.password_entry.get()

        if os.path.exists(PASSENGERS_PATH):
            with open(PASSENGERS_PATH, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 6 and row[5] == username and row[6] == password:
                        self.start_main_menu_passenger()
                        return

        messagebox.showerror("Login Failed", "Invalid username or password. Please register if you don't have an account.")
        
    def verify_login_driver(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if os.path.exists(DRIVERS_PATH):
            with open(DRIVERS_PATH, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 9 and row[4] == username and row[9] == password:
                        self.start_main_menu_passenger()
                        return

    def start_main_menu_passenger(self):
        """Called right after successful authentication."""
        self.attributes("-alpha", 1.0)
        self.show_dashboard_passenger()
        
    def start_main_menu_driver(self):
        """Called right after successful authentication."""
        self.attributes("-alpha", 1.0)
        self.show_dashboard_driver()

# ====== PASSENGER DASHBOARD ======

    #MAP BOOKING
    def show_dashboard_passenger(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Welcome to Duck Dash!", font=("Courier", 24, "bold"), text_color=TEXT_COLOR).pack(pady=20)

        # Load the image for the booking button
        book_img = Image.open(IMAGE_PATH)
        book_ctk_img = ctk.CTkImage(light_image=book_img, dark_image=book_img, size=(30, 30))

        ctk.CTkButton(self, text=" Book a Ride", image=book_ctk_img, compound="left", font=("Arial", 18), command=self.show_booking_screen).pack(pady=15)
        ctk.CTkButton(self, text="Log Out", font=("Arial", 15), command=self.show_start_screen).pack(pady=30)

    def show_booking_screen(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Book a Ride", font=("Arial", 22, "bold"), text_color=TEXT_COLOR).pack(pady=20)

        ctk.CTkLabel(self, text="Pickup Location", text_color=TEXT_COLOR).pack()
        self.pickup_entry = ctk.CTkEntry(self, width=300)
        self.pickup_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Dropoff Location", text_color=TEXT_COLOR).pack()
        self.dropoff_entry = ctk.CTkEntry(self, width=300)
        self.dropoff_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Vehicle", text_color=TEXT_COLOR).pack(pady=5)
        self.selected_vehicle = ctk.StringVar(value=self.available_vehicles()[0])
        self.vehicle_menu = ctk.CTkOptionMenu(self, variable=self.selected_vehicle, values=self.available_vehicles(), command=self.update_seat_options)
        self.vehicle_menu.pack(pady=5)

        ctk.CTkLabel(self, text="Seat Count", text_color=TEXT_COLOR).pack()
        self.selected_seat = ctk.StringVar()
        initial_seats = [str(seat) for seat in self.available_seats()[self.selected_vehicle.get()]]
        self.selected_seat.set(initial_seats[0])
        self.seat_menu = ctk.CTkOptionMenu(self, variable=self.selected_seat, values=initial_seats)
        self.seat_menu.pack(pady=5)

        ctk.CTkButton(self, text="Calculate Fare & Show Map", command=self.process_booking).pack(pady=15)
        ctk.CTkButton(self, text="Confirm Ride", command=self.confirm_ride).pack(pady=10)
        ctk.CTkButton(self, text="Back to Dashboard", command=self.show_dashboard_passenger).pack(pady=10)

    def update_seat_options(self, selected_vehicle):
        seats = [str(seat) for seat in self.available_seats()[selected_vehicle]]
        self.seat_menu.configure(values=seats)
        self.selected_seat.set(seats[0])

    def available_vehicles(self):
        return ["Car", "Van", "Motorcycle"]

    def available_seats(self):
        return {"Car": [4, 5, 6],
                "Van": [6, 8, 10, 15, 20], 
                "Motorcycle": [1]}

    def total_fare(self, vehicle, distance_km):
        rates = {"Car": 45, "Van": 60, "Motorcycle": 30}
        return rates.get(vehicle, 0) * distance_km

    def process_booking(self):
        pickup = self.pickup_entry.get().strip()
        dropoff = self.dropoff_entry.get().strip()
        vehicle = self.selected_vehicle.get()
        try:
            seat_count = int(self.selected_seat.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Seat count must be a number.")
            return

        if not pickup or not dropoff:
            messagebox.showerror("Missing Info", "Pickup and dropoff cannot be empty.")
            return

        if seat_count not in self.available_seats()[vehicle]:
            messagebox.showerror("Seat Error", f"{vehicle}s cannot have {seat_count} seats.")
            return

        geolocator = Nominatim(user_agent="duckdash_app")
        pickup_loc = geolocator.geocode(pickup)
        dropoff_loc = geolocator.geocode(dropoff)

        if not pickup_loc or not dropoff_loc:
            messagebox.showerror("Location Error", "Invalid pickup or dropoff address.")
            return

        pickup_coords = (pickup_loc.latitude, pickup_loc.longitude)
        dropoff_coords = (dropoff_loc.latitude, dropoff_loc.longitude)
        distance_km = geodesic(pickup_coords, dropoff_coords).kilometers
        fare = self.total_fare(vehicle, distance_km)

        summary = f"""
            ✨ Booking Summary ✨
            Vehicle: {vehicle}
            Seats: {seat_count}
            From: {pickup}
            To: {dropoff}
            Distance: {distance_km:.2f} km
            Fare: ₱{fare:.2f}
            """
        messagebox.showinfo("Ride Summary", summary.strip())

        # Show route map
        map_window = tk.Toplevel(self)
        map_window.title("Route Map")
        map_widget = TkinterMapView(map_window, width=800, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_position(*pickup_coords)
        map_widget.set_zoom(12)
        map_widget.set_marker(*pickup_coords, text="Pickup")
        map_widget.set_marker(*dropoff_coords, text="Dropoff")
        map_widget.set_path([pickup_coords, dropoff_coords])

    def confirm_ride(self):
        pickup = self.pickup_entry.get().strip()
        dropoff = self.dropoff_entry.get().strip()
        vehicle = self.selected_vehicle.get()
        seat = self.selected_seat.get()
        geolocator = Nominatim(user_agent="duckdash_app_confirm")
        pickup_loc = geolocator.geocode(pickup)
        dropoff_loc = geolocator.geocode(dropoff)
        if not pickup_loc or not dropoff_loc:
            messagebox.showerror("Location Error", "Invalid pickup or dropoff address.")
            return
        pickup_coords = (pickup_loc.latitude, pickup_loc.longitude)
        dropoff_coords = (dropoff_loc.latitude, dropoff_loc.longitude)
        distance_km = geodesic(pickup_coords, dropoff_coords).kilometers
        fare = self.total_fare(vehicle, distance_km)
        details = f"""
        ✅ Ride Confirmed!

        --- Ride Details ---
        Pickup Location: {pickup}
        Dropoff Location: {dropoff}
        Vehicle: {vehicle}
        Seat Count: {seat}
        Distance: {distance_km:.2f} km
        Fare: ₱{fare:.2f}

        Thank you for booking with Duck Dash!
        """
        messagebox.showinfo("Ride Confirmed", details.strip())
        # Save booking as a row with all required fields for driver dashboard
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        booking_row = {
            "Name": "Passenger",  # You can replace with actual passenger name if available
            "Pickup": pickup,
            "Dropoff": dropoff,
            "Time": now,
            "Status": "Pending",
            "Vehicle": vehicle,
            "Seat": seat,
            "Distance": f"{distance_km:.2f}",
            "Fare": f"{fare:.2f}"
        }
        file_exists = os.path.exists(BOOKINGS_FILE)
        with open(BOOKINGS_FILE, "a", newline='', encoding="utf-8") as file:
            fieldnames = ["Name", "Pickup", "Dropoff", "Time", "Status", "Vehicle", "Seat", "Distance", "Fare"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists or os.stat(BOOKINGS_FILE).st_size == 0:
                writer.writeheader()
            writer.writerow(booking_row)

# ====== DRIVER DASHBOARD ======

    def show_dashboard_driver(self):
        self.clear_window()
        ctk.CTkLabel(self, text="Welcome to Duck Dash!", font=("Courier", 24, "bold"), text_color=TEXT_COLOR).pack(pady=20)

        book_img = Image.open(IMAGE_PATH)
        book_ctk_img = ctk.CTkImage(light_image=book_img, dark_image=book_img, size=(30, 30))

        ctk.CTkButton(self, text=" Start Ride", image=book_ctk_img, compound="left", font=("Arial", 18), command=self.load_bookings).pack(pady=15)
        ctk.CTkButton(self, text="Log Out", font=("Arial", 15), command=self.show_start_screen).pack(pady=30)

        self.title_label = ctk.CTkLabel(self, text="Available Booked Rides", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.ride_listbox = ctk.CTkTextbox(self, width=550, height=200)
        self.ride_listbox.pack(pady=10)

        self.select_button = ctk.CTkButton(self, text="Select Ride", command=self.select_ride)
        self.select_button.pack(pady=5)

        self.accept_button = ctk.CTkButton(self, text="Accept Ride", command=self.accept_ride, state="disabled")
        self.accept_button.pack(pady=5)

        self.refresh_button = ctk.CTkButton(self, text="Refresh List", command=self.load_bookings)
        self.refresh_button.pack(pady=5)

        self.selected_ride_index = None
        self.load_bookings()
    
    def load_bookings(self):
        self.ride_listbox.delete("0.0", "end")
        self.bookings = []

        if not os.path.exists(BOOKINGS_FILE):
            self.ride_listbox.insert("0.0", "No bookings available.")
            return

        with open(BOOKINGS_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if row.get("Status", "").lower() == "pending":
                    self.bookings.append(row)
                    ride_info = f"[{i}] {row.get('Name', 'Passenger')} | From: {row.get('Pickup', '')} → {row.get('Dropoff', '')} at {row.get('Time', '')} | Vehicle: {row.get('Vehicle', '')} | Seat: {row.get('Seat', '')} | Fare: ₱{row.get('Fare', '')}"
                    self.ride_listbox.insert("end", ride_info + "\n")

    def select_ride(self):
        index_prompt = ctk.CTkInputDialog(text="Enter ride number to select:", title="Select Ride")
        index_str = index_prompt.get_input()
        if index_str and index_str.isdigit():
            index = int(index_str)
            if 0 <= index < len(self.bookings):
                self.selected_ride_index = index
                self.accept_button.configure(state="normal")
                messagebox.showinfo("Ride Selected", f"Ride #{index} selected.")
            else:
                messagebox.showerror("Invalid", "Invalid ride index!")

    def accept_ride(self):
        if self.selected_ride_index is not None:
            with open(BOOKINGS_FILE, newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))

            ride_to_accept = self.bookings[self.selected_ride_index]
            for row in rows:
                if (row.get("Name", "") == ride_to_accept.get("Name", "") and 
                    row.get("Pickup", "") == ride_to_accept.get("Pickup", "") and 
                    row.get("Dropoff", "") == ride_to_accept.get("Dropoff", "") and
                    row.get("Time", "") == ride_to_accept.get("Time", "")):
                    row["Status"] = "Accepted"
                    break

            fieldnames = rows[0].keys() if rows else ["Name", "Pickup", "Dropoff", "Time", "Status", "Vehicle", "Seat", "Distance", "Fare"]
            with open(BOOKINGS_FILE, "w", newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            messagebox.showinfo("Success", "Ride accepted!")
            self.accept_button.configure(state="disabled")
            self.load_bookings()


# ====== SCREEN AFTER START UP ====== REUSABLE Codes

    def create_login_screen(self):              # Reusable Code
            self.clear_window()
            ctk.CTkLabel(self, text="Welcome to Duck Dash", font=("Courier", 28, "bold"), text_color=TEXT_COLOR).pack(pady=40)
            ctk.CTkLabel(self, text="Select your mode:", font=("Arial", 18)).pack(pady=10)

            ctk.CTkButton(self, text="   Login as Passenger   ",font=("Arial", 18), command=self.passenger_login).pack(pady=(20,10))
            ctk.CTkButton(self, text="      Login as Driver      ", font=("Arial", 18), command=self.driver_login).pack(pady=(20,10))

            ctk.CTkButton(self, text="Back", command=self.show_start_screen).pack(pady=(150, 30))

    def create_register_screen(self):             # Reusable Code
            self.clear_window()
            ctk.CTkLabel(self, text="Welcome to Duck Dash", font=("Courier", 28, "bold"), text_color=TEXT_COLOR).pack(pady=40)
            ctk.CTkLabel(self, text="Select your mode:", font=("Arial", 18)).pack(pady=10)

            ctk.CTkButton(self, text="   Register as Passenger   ",font=("Arial", 18), command=self.passenger_registration).pack(pady=(20,10))
            ctk.CTkButton(self, text="      Register as Driver      ", font=("Arial", 18), command=self.driver_registration).pack(pady=(20,10))

            ctk.CTkButton(self, text="Back", command=self.show_start_screen).pack(pady=(150, 30))
            
# ====== Login as Passenger ======

    def passenger_login(self):
        self.clear_window()
        tagline_text = """Lookin for a Ride?
Book a Ride at DUCK DASH!

Fast as Duck, Quack! Quack! Quack!"""
        tagline = ctk.CTkLabel(self, text=tagline_text, font=("Courier", 14, "bold"), text_color=TEXT_COLOR, justify="center")
        tagline.pack(pady=20)

        ctk.CTkLabel(self, text="Login", font=("Arial", 20, "bold"), text_color=TEXT_COLOR).pack(pady=20)

        username_label = ctk.CTkLabel(self, text="Username", text_color=TEXT_COLOR)
        username_label.pack()
        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(self, text="Password", text_color=TEXT_COLOR)
        password_label.pack()
        self.password_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_entry.pack(pady=5)
        
        ctk.CTkButton(self, text="Login", command=self.verify_login_passenger).pack(pady=10)
    
# ====== Login as Driver ======

    def driver_login(self):
        self.clear_window()
        tagline_text = """Lookin for a Ride?
Book a Ride at DUCK DASH!

Fast as Duck, Quack! Quack! Quack!"""
        tagline = ctk.CTkLabel(self, text=tagline_text, font=("Courier", 14, "bold"), text_color=TEXT_COLOR, justify="center")
        tagline.pack(pady=20)

        ctk.CTkLabel(self, text="Login", font=("Arial", 20, "bold"), text_color=TEXT_COLOR).pack(pady=20)

        username_label = ctk.CTkLabel(self, text="Username", text_color=TEXT_COLOR)
        username_label.pack()
        self.username_entry = ctk.CTkEntry(self, width=200)
        self.username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(self, text="Password", text_color=TEXT_COLOR)
        password_label.pack()
        self.password_entry = ctk.CTkEntry(self, show="*", width=200)
        self.password_entry.pack(pady=5)
        
        ctk.CTkButton(self, text="Login", command=self.verify_login_driver).pack(pady=10)

# ====== Register as Passenger ======

    def passenger_registration(self):
        self.clear_window()
        self.passenger_data = {}

        scrollable_frame = ctk.CTkScrollableFrame(self, width=500, height=600)
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scrollable_frame, text="Passenger Registration", font=("Arial", 20, "bold"), text_color=TEXT_COLOR).pack(pady=10)
        form_frame1 = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        form_frame1.pack(padx=10, pady=10, fill="both", expand=True)

        def create_entry(label_text, row, column):
            label = ctk.CTkLabel(form_frame1, text=label_text, text_color=TEXT_COLOR)
            label.grid(row=row, column=column, sticky="w", padx=5)
            entry = ctk.CTkEntry(form_frame1, width=150)
            entry.grid(row=row+1, column=column, padx=5, pady=5)
            return entry

        self.passenger_data["First Name"] = create_entry("First Name *", 0, 0)
        self.passenger_data["Last Name"] = create_entry("Last Name *", 0, 1)
        
        gender_label = ctk.CTkLabel(form_frame1, text="Gender *", text_color=TEXT_COLOR)
        gender_label.grid(row=2, column=0, sticky="w", padx=5)
        self.passenger_data["Gender"] = ctk.StringVar(value="Male")
        gender_menu = ctk.CTkOptionMenu(form_frame1, variable=self.passenger_data["Gender"], values=["Male", "Female", "LGBTQ+", "Prefer Not to Say"])
        gender_menu.grid(row=3, column=0, padx=5, pady=5)

        self.passenger_data["Age"] = create_entry("Age *", 2, 1)

        address_label = ctk.CTkLabel(form_frame1, text="Address *", text_color=TEXT_COLOR)
        address_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
        self.passenger_data["Address"] = ctk.CTkEntry(form_frame1, width=320)
        self.passenger_data["Address"].grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        username_label = ctk.CTkLabel(form_frame1, text="Username *", text_color=TEXT_COLOR)
        username_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=5)
        self.passenger_data["Username"] = ctk.CTkEntry(form_frame1, width=320)
        self.passenger_data["Username"].grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        password_label = ctk.CTkLabel(form_frame1, text="Enter a Password *", text_color=TEXT_COLOR)
        password_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=5)
        self.passenger_data["Password"] = ctk.CTkEntry(form_frame1, width=320)
        self.passenger_data["Password"].grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        contact_label = ctk.CTkLabel(form_frame1, text="Contact Number *", text_color=TEXT_COLOR)
        contact_label.grid(row=10, column=0, columnspan=2, sticky="w", padx=5)
        self.passenger_data["Contact Number"] = ctk.CTkEntry(form_frame1, width=320)
        self.passenger_data["Contact Number"].grid(row=11, column=0, columnspan=2, padx=5, pady=5)

        self.gcash_var = ctk.BooleanVar()
        self.paymaya_var = ctk.BooleanVar()
        self.paypal_var = ctk.BooleanVar()
        self.cod_var = ctk.BooleanVar(value=True)

        self.payment_method = ctk.StringVar(value="Cash")

        ctk.CTkRadioButton(form_frame1, text="GCash", variable=self.payment_method, value="GCash").grid(row=14, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame1, text="PayMaya", variable=self.payment_method, value="PayMaya").grid(row=16, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame1, text="PayPal", variable=self.payment_method, value="PayPal").grid(row=18, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame1, text="Cash", variable=self.payment_method, value="Cash").grid(row=20, column=0, sticky="w", padx=10, pady=(0, 10))

        button_frame = ctk.CTkFrame(scrollable_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Register as Passenger", width=280, height=40, command=self.save_passenger).pack(pady=10)
        ctk.CTkButton(button_frame, text="Back", command=self.create_register_screen).pack(pady=(0, 10))

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

        try: 
            age= int(data_passenger["Age"])
            if age <=17:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a Valid Age. Passenger should be 18 and above.")
            return 
        
        passenger = Passenger(data_passenger["First Name"], data_passenger["Last Name"], data_passenger["Gender"],
                      data_passenger["Address"], data_passenger["Contact Number"],
                      data_passenger.get("GCash Account"), data_passenger.get("PayMaya Account"), data_passenger.get("PayPal Account"),
                      self.cod_var.get())
        
        if os.path.exists(PASSENGERS_PATH):
            with open(PASSENGERS_PATH, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([passenger.first_name, passenger.last_name, passenger.gender, passenger.address, passenger.contact_info,
                                data_passenger["Username"], data_passenger["Password"],
                                passenger.gcash_account, passenger.paymaya_account, passenger.paypal_account, passenger.cod_enabled])

        messagebox.showinfo("Success", "Passenger Registered Successfully!")
        self.create_register_screen()

# ====== Driver Registration ======

    def driver_registration(self):
        self.clear_window()
        self.driver_data = {}
        fields = ["First Name", "Last Name", "Gender", "Age", "Address", "Contact Number",
                  "Vehicle Type", "Vehicle Model", "Vehicle Color", "Plate Number", "Qualifications", "Password"]

        scrollable_frame2 = ctk.CTkScrollableFrame(self, width=500, height=1000)
        scrollable_frame2.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scrollable_frame2, text="Drivers Registration", font=("Arial", 20, "bold"), text_color=TEXT_COLOR).pack(pady=10)
        form_frame2 = ctk.CTkFrame(scrollable_frame2, fg_color="transparent")
        form_frame2.pack(padx=10, pady=10, fill="both", expand=True)

        def create_entry(label_text, row, column):
            label = ctk.CTkLabel(form_frame2, text=label_text, text_color=TEXT_COLOR)
            label.grid(row=row, column=column, sticky="w", padx=5)
            entry = ctk.CTkEntry(form_frame2, width=150)
            entry.grid(row=row+1, column=column, padx=5, pady=5)
            return entry

        self.driver_data["First Name"] = create_entry("First Name *", 0, 0)
        self.driver_data["Last Name"] = create_entry("Last Name *", 0, 1)
        
        gender_label = ctk.CTkLabel(form_frame2, text="Gender *", text_color=TEXT_COLOR)
        gender_label.grid(row=2, column=0, sticky="w", padx=5)
        self.driver_data["Gender"] = ctk.StringVar(value="Male")
        gender_menu = ctk.CTkOptionMenu(form_frame2, variable=self.driver_data["Gender"], values=["Male", "Female", "LGBTQ+", "Prefer Not to Say"])
        gender_menu.grid(row=3, column=0, padx=5, pady=5)

        self.driver_data["Age"] = create_entry("Age *", 2, 1)

        username_label = ctk.CTkLabel(form_frame2, text="Username *", text_color=TEXT_COLOR)
        username_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5)
        self.driver_data["Username"] = ctk.CTkEntry(form_frame2, width=320)
        self.driver_data["Username"].grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.driver_data["Vehicle Type"] = create_entry("Vehicle Type *", 7, 0)
        self.driver_data["Vehicle Model"] = create_entry("Vehicle Model *", 7, 1)
        self.driver_data["Vehicle Color"] = create_entry("Vehicle Color *", 9, 0)
        self.driver_data["Plate Number"] = create_entry("Plate Number *", 9, 1 )

        password_label = ctk.CTkLabel(form_frame2, text="Password *", text_color=TEXT_COLOR)
        password_label.grid(row=12, column=0, columnspan=2, sticky="w", padx=5)
        self.driver_data["Password"] = ctk.CTkEntry(form_frame2, width=320)
        self.driver_data["Password"].grid(row=14, column=0, columnspan=2, padx=1, pady=5)

        contact_label = ctk.CTkLabel(form_frame2, text="Contact Number *", text_color=TEXT_COLOR)
        contact_label.grid(row=15, column=0, columnspan=2, sticky="w", padx=5)
        self.driver_data["Contact Number"] = ctk.CTkEntry(form_frame2, width=320)
        self.driver_data["Contact Number"].grid(row=17, column=0, columnspan=2, padx=1, pady=5)

        self.payment_method = ctk.StringVar(value="Cash")
        ctk.CTkRadioButton(form_frame2, text="GCash", variable=self.payment_method, value="GCash").grid(row=19, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame2, text="PayMaya", variable=self.payment_method, value="PayMaya").grid(row=21, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame2, text="PayPal", variable=self.payment_method, value="PayPal").grid(row=23, column=0, sticky="w", padx=10)
        ctk.CTkRadioButton(form_frame2, text="Cash", variable=self.payment_method, value="Cash").grid(row=25, column=0, sticky="w", padx=10, pady=(0, 10))

        button_frame = ctk.CTkFrame(scrollable_frame2)
        button_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Submit", command=self.save_driver).pack(pady=15)
        ctk.CTkButton(button_frame, text="Back", command=self.create_register_screen).pack()

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

        try:
            age = int(data_driver["Age"])
            if age <=17:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a Valid Age. Driver should be of legal Age")
            return 
        
        contact_num = data_driver["Contact Number"].strip()
        if not (contact_num.isdigit() and len(contact_num) == 11):
            messagebox.showerror("Invalid Input", "Contact Number must be exactly 11 digits.")
            return

        vehicle = Vehicle(data_driver["Vehicle Type"], data_driver["Vehicle Model"], data_driver["Vehicle Color"], data_driver["Plate Number"])
        driver = Driver(
            data_driver["First Name"],
            data_driver["Last Name"],
            data_driver["Gender"],
            data_driver.get("Address", ""),
            data_driver["Username"],
            vehicle,
        )

        if os.path.exists(DRIVERS_PATH):
            with open(DRIVERS_PATH, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    data_driver["First Name"],
                    data_driver["Last Name"],
                    data_driver["Gender"],
                    data_driver["Age"],
                    data_driver["Username"],
                    data_driver["Vehicle Type"],
                    data_driver["Vehicle Model"],
                    data_driver["Vehicle Color"],
                    data_driver["Plate Number"],
                    data_driver["Password"],
                    data_driver["Contact Number"]
                ])


        messagebox.showinfo("Success", "Driver registered successfully!")
        self.create_register_screen()

if __name__ == '__main__':
    app = DuckDashApp()
    app.mainloop()