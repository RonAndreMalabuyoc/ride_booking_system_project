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
    def __init__(self, first_name, last_name, gender, address, contact_info, vehicle, qualifications=None, join_date=None):
        super().__init__(first_name, last_name, gender, address, contact_info)
        self.vehicle = vehicle
        self.qualifications = qualifications
        self.ratings = []
        self.total_rides = 0
        self.earnings = 0.0
        self.mileage = 0.0
        self.successful_drives = 0
        self.join_date = join_date or datetime.now().isoformat()

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
            driver.qualifications, driver.total_rides, driver.earnings, len(driver.ratings), datetime.now().isoformat()
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
    gcash_account = input("GCash Account (optional): ")
    paymaya_account = input("PayMaya Account (optional): ")
    paypal_account = input("PayPal Account (optional): ")
    cod_enabled = input("Enable Cash on Delivery? (yes/no): ").strip().lower() == "yes"
    rider = Rider(first_name, last_name, gender, address, contact_info, gcash_account, paymaya_account, paypal_account, cod_enabled)
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
    vehicle = Vehicle(vehicle_type, model, color, plate_number)
    driver = Driver(first_name, last_name, gender, address, contact_info, vehicle, qualifications)
    save_driver_profile(driver)
    print("Driver registered successfully!")
    return driver

if __name__ == "__main__":
    mode = show_terms_of_service_and_mode_select()
    if mode == "Driver":
        driver = register_driver()
        # Continue with driver dashboard or booking logic
    elif mode == "Rider":
        rider = register_rider()
        # Continue with rider booking logic