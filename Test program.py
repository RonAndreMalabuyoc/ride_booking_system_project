class User:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info

class Rider(User):
    def __init__ (self, name, contact_info, location, vehicle_select):
        super().__init__(name, contact_info)
        self.location = location
        self.vehicle_select = vehicle_select

class Vehicle:
    def __init__(self, vehicle_type, vehicle_model, vehicle_color, vehicle_plate_number):
        self.vehicle_type = vehicle_type
        self.vehicle_model = vehicle_model
        self.vehicle_color = vehicle_color
        self.vehicle_plate_number = vehicle_plate_number

class Driver(User):
    def __init__(self, name, contact_info, qualifications, ratings, total_rides, earnings, vehicle):
        super().__init__(name, contact_info)
        self.qualifications = qualifications
        self.ratings = ratings
        self.total_rides = total_rides
        self.earnings = earnings
        self.vehicle = vehicle

def show_terms_of_service_and_mode_select():
    print("Welcome to ____")
    print("TOS insert here: ")
    response = input("Do you accept (yes/no): ")
    if response != "yes":
        print("You must agree to terms of service")
    elif response == "yes":
        mode_select = input("Are you using this app as a Rider or a Driver? Press 1 for Driver, Press 2 for Rider")
        if mode_select == "1":
            return "Driver"
        elif mode_select == "2":
            return "Rider"
        else:
            print("Invalid option, exiting application")
            return None
        
if __name__ == "__main__":
    show_terms_of_service_and_mode_select()
        

