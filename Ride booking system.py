import csv
from datetime import datetime

class User:
    def __init__(self, first_name, last_name, gender, address, contact_info, age=None):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.address = address
        self.contact_info = contact_info
        self.age = age


class Rider(User):
    def __init__(self, first_name, last_name, gender, address, contact_info, gcash_account=None, paymaya_account=None, paypal_account=None, cod_enabled=True):
        super().__init__(first_name, last_name, gender, address, contact_info)
        self.gcash_account = gcash_account
        self.paymaya_account = paymaya_account
        self.paypal_account = paypal_account  
        self.cod_enabled = cod_enabled  # Cash on Delivery enabled by default
        self.recent_places = []
        self.favorites = []
class Vehicle:
    def __init__(self, vehicle_type, model, color, plate_number):
        self.vehicle_type = vehicle_type
        self.model = model
        self.color = color
        self.plate_number = plate_number

class Driver(User):
    def __init__(self, first_name, last_name, gender, address, contact_info, vehicle, qualifications=None, join_date=None, password=None):
        super().__init__(first_name, last_name, gender, address, contact_info)
        self.vehicle = vehicle
        self.qualifications = qualifications
        self.ratings = []
        self.total_rides = 0
        self.earnings = 0.0
        self.mileage = 0.0
        self.successful_drives = 0
        self.join_date = join_date or datetime.now().isoformat()
        self.password = password

def show_terms_of_service_and_mode_select():
    print("Welcome to ____")
    print("Terms of Service (TOS):")
    print("""
    1. By using this application, you agree to provide accurate and up-to-date information during registration.
    2. Location access is required for booking and ride tracking purposes.
    3. All users must treat each other with respect and follow community guidelines.
    4. Payments must be made through the supported payment methods.
    5. The app is not liable for any loss, damage, or injury during rides.
    6. Drivers and passengers are responsible for their own safety and belongings.
    7. Any misuse of the platform may result in account suspension or termination.
    8. Your data will be handled in accordance with our privacy policy.
    """)
    response = input("Do you accept (yes/no): ")
    if response != "yes":
        print("You must agree to terms of service: ")
    elif response == "yes":
        mode_select = input("Are you using this app as a Rider or a Driver? Press 1 for Driver, Press 2 for Rider: " )
        if mode_select == "1":
            return "Driver"
        elif mode_select == "2":
            return "Rider"
        else:
            print("Invalid option, exiting application")
            return None

def save_rider_profile(rider, filename="riders.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            rider.first_name, rider.last_name, rider.gender, rider.address, rider.contact_info,
            rider.gcash_account, rider.paymaya_account, rider.paypal_account, rider.cod_enabled
        ])

def save_driver_profile(driver, filename="drivers.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            driver.first_name, driver.last_name, driver.gender, driver.address, driver.contact_info,
            driver.vehicle.vehicle_type, driver.vehicle.model, driver.vehicle.color, driver.vehicle.plate_number,
            driver.qualifications, driver.total_rides, driver.earnings, len(driver.ratings), driver.join_date, driver.password
        ]) 

def log_ride(rider, driver, distance, fare, filename="rides.csv"):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            rider.first_name, driver.first_name, driver.vehicle.plate_number,
            distance, fare, datetime.now().isoformat()
        ])

def register_rider():
    print("=== Rider Registration ===")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    gender = input("Gender: ")
    age = input("Age: ")
    address = input("Address: ")
    contact_info = input("Contact Number: ")

    print("Select payment methods you want to use (type numbers separated by commas):")
    print("1. GCash")
    print("2. PayMaya")
    print("3. PayPal")
    print("4. Cash on Delivery (CoD)")
    selected = input("Your choices: ").replace(" ", "").split(",")

    gcash_account = None
    paymaya_account = None
    paypal_account = None
    cod_enabled = False

    if "1" in selected:
        gcash_account = input("Enter GCash Account: ")
    if "2" in selected:
        paymaya_account = input("Enter PayMaya Account: ")
    if "3" in selected:
        paypal_account = input("Enter PayPal Account: ")
    if "4" in selected:
        cod_enabled = True

    rider = Rider(
        first_name, last_name, gender, address, contact_info,
        gcash_account, paymaya_account, paypal_account, cod_enabled
    )
    save_rider_profile(rider)
    print("Rider registered successfully!")
    return rider

def register_driver():
    print("=== Driver Registration ===")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    gender = input("Gender: ")
    age = input("Age: ")
    address = input("Address: ")
    contact_info = input("Contact Number: ")
    vehicle_type = input("Vehicle Type: ")
    model = input("Vehicle Model: ")
    color = input("Vehicle Color: ")
    plate_number = input("Plate Number: ")
    qualifications = input("Qualifications (optional): ")
    password = input("Set a password: ")
    vehicle = Vehicle(vehicle_type, model, color, plate_number)
    driver = Driver(first_name, last_name, gender, address, contact_info, vehicle, qualifications, password=password)
    save_driver_profile(driver)
    print("Driver registered successfully!")
    return driver\
    
def driver_login(filename="drivers.csv"):
    print("=== Driver Log In ===")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    password = input("Password: ")
    found = False
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                # row indices: ... 14=password
                if row[0] == first_name and row[1] == last_name and row[14] == password:
                    vehicle = Vehicle(row[5], row[6], row[7], row[8])
                    driver = Driver(
                        row[0], row[1], row[2], row[3], row[4],
                        vehicle, row[9], row[13], password=row[14]
                    )
                    driver.total_rides = int(row[10])
                    driver.earnings = float(row[11])
                    driver.ratings = [None] * int(row[12])
                    found = True
                    print("Login successful!")
                    return driver
        if not found:
            print("Driver not found or incorrect password. Please try again or register.")
            return None
    except FileNotFoundError:
        print("No driver profiles found. Please register first.")
        return None
    
def driver_dashboard(driver):
    while True:
        print("\n=== Driver Dashboard ===")
        print("1. View Profile")
        print("2. View Nearby Bookings")
        print("3. View Earnings")
        print("4. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            print(f"\nName: {driver.first_name} {driver.last_name}")
            print(f"Gender: {driver.gender}")
            print(f"Address: {driver.address}")
            print(f"Contact: {driver.contact_info}")
            print(f"Vehicle: {driver.vehicle.vehicle_type} {driver.vehicle.model} ({driver.vehicle.color}), Plate: {driver.vehicle.plate_number}")
            print(f"Qualifications: {driver.qualifications}")
            print(f"Total Rides: {driver.total_rides}")
            print(f"Earnings: {driver.earnings}")
            print(f"Ratings: {driver.ratings}")
            print(f"Successful Drives: {driver.successful_drives}")
            print(f"Join Date: {driver.join_date}")

        elif choice == "2":
            # Simulate viewing bookings (replace with real booking logic)
            print("\nNearby Bookings:")
            print("1. Pickup: Main St. | Dropoff: Park Ave. | Fare: 150")
            print("2. Pickup: 2nd Ave. | Dropoff: Mall | Fare: 120")
            booking_choice = input("Accept a booking? (1/2 or 'b' to go back): ")
            if booking_choice in ["1", "2"]:
                print("Booking accepted! Navigating to pickup location...")
                # Simulate ride completion
                complete = input("Mark ride as complete? (yes/no): ")
                if complete.lower() == "yes":
                    fare = 150 if booking_choice == "1" else 120
                    driver.total_rides += 1
                    driver.earnings += fare
                    driver.successful_drives += 1
                    print("Ride completed and earnings updated!")
            else:
                continue

        elif choice == "3":
            print(f"\nTotal Earnings: {driver.earnings}")
            print(f"Total Rides: {driver.total_rides}")

        elif choice == "4":
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")

def rider_experience(rider):
    location_access = input("Allow location access (Y/n): ")
    if location_access != "Y":
        print("Location access is required to proceed.")
        return
    else:
        print("Location access granted. Enter your current location:")

    # Vehicle Selection
    print("Please select which Vehicle you would like to book:")
    print("Press 1 for Motorcycle, Press 2 for Car, Press 3 for Van")
    vehicle_choice = input("Enter your option here: ")
    vehicle_types = {"1": "Motorcycle", "2": "Car", "3": "Van"}
    vehicle_selected = vehicle_types.get(vehicle_choice, None)

    if vehicle_selected:
        print(f"Searching for a {vehicle_selected} nearby...")
        print(f"Finding a {vehicle_selected} near your location... Please wait.")
        input(f"A {vehicle_selected} has arrived. Press Enter to confirm ride arrival.")

        print("Please rate your ride experience:")
        rating = input("Rate from 1 to 5 stars: ")
        while rating not in ["1", "2", "3", "4", "5"]:
            print("Invalid input. Please enter a rating between 1 and 5.")
            rating = input("Rate from 1 to 5 stars: ")

        print(f"Thank you for your feedback! You rated your ride {rating} stars.")

if __name__ == "__main__":
    mode = show_terms_of_service_and_mode_select()
    if mode == "Driver":
        print("1. Register as Driver")
        print("2. Log In as Driver")
        action = input("Select an option: ")
        if action == "1":
            driver = register_driver()
        elif action == "2":
            driver = driver_login()
        else:
            print("Invalid option.")
            driver = None
        if driver:
            driver_dashboard(driver)
    elif mode == "Rider":
        rider = register_rider()
        rider_experience(rider)