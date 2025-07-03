from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import tkinter as tk
from tkintermapview import TkinterMapView


def available_vehicles():
    vehicles = ["Car", "Van", "Motorcycle"]
    print("Available Vehicles:")
    for idx, vehicle in enumerate(vehicles, start=1):
        print(f"{idx}. {vehicle}")
    return vehicles

def available_seats():
    seats = {"Car": [4, 5, 6], "Van": [6, 8, 10, 15, 20], "Motorcycle": [1]}
    return seats

def select_vehicle():
    vehicles = available_vehicles()
    while True:
        try:
            choice = int(input("Select the number of the vehicle you want: "))
            if 1 <= choice <= len(vehicles):
                return vehicles[choice - 1]
            else:
                print("Invalid choice, please select again.")
        except ValueError:
            print("Please enter a valid number.")

def select_seat_count(vehicle, seats):
    print(f"Available seats for {vehicle}: {seats[vehicle]}")
    while True:
        try:
            seat_count = int(input(f"Choose the number of seats for {vehicle}: "))
            if seat_count in seats[vehicle]:
                return seat_count
            else:
                print("Invalid seat count, please select again.")
        except ValueError:
            print("Please enter a valid number.")

def show_map_and_get_distance(pickup, dropoff):
    geolocator = Nominatim(user_agent="ride_booking_app")

    pickup_location = geolocator.geocode(pickup)
    dropoff_location = geolocator.geocode(dropoff)
    if not pickup_location or not dropoff_location:
        print("Could not find one or both locations.")
        return None
    pickup_coords = (pickup_location.latitude, pickup_location.longitude)
    dropoff_coords = (dropoff_location.latitude, dropoff_location.longitude)
    distance_km = geodesic(pickup_coords, dropoff_coords).kilometers
    print(f"Distance from {pickup} to {dropoff}: {distance_km:.2f} km")

    root = tk.Tk()
    root.title("Route Map")
    map_widget = TkinterMapView(root, width=800, height=600, corner_radius=0)
    map_widget.pack(fill="both", expand=True)
    map_widget.set_position(pickup_location.latitude, pickup_location.longitude)
    map_widget.set_zoom(12)
    map_widget.set_marker(*pickup_coords, text="Pickup")
    map_widget.set_marker(*dropoff_coords, text="Dropoff")
    map_widget.set_path([pickup_coords, dropoff_coords])
    root.mainloop()
    
    return distance_km

def total_fare(vehicle, distance_km):
    fare_per_km = {
        "Car": 45.00,
        "Van": 60.00,
        "Motorcycle": 30.00
    }
    return fare_per_km[vehicle] * distance_km

def main():
    print("Your vehicle is ready to roll! 🚗💨")
    vehicle = select_vehicle()
    seats = available_seats()
    seat_count = select_seat_count(vehicle, seats)

    print("Enter the full address or landmark for precise navigation.")
    pickup_name = input("Pickup location: ").strip()
    dropoff_name = input("Dropoff location: ").strip()


    distance_km = show_map_and_get_distance(pickup_name, dropoff_name)
    if distance_km is None:
        print("Unable to calculate distance. Please check your locations.")
        return

    fare = total_fare(vehicle, distance_km)
    print(f"\n✨ Summary of your booking!✨")
    print(f"Your vehicle for today is {vehicle} with {seat_count} seats")
    print(f"From: {pickup_name}")
    print(f"To: {dropoff_name}")
    print(f"Distance: {distance_km:.2f} km")
    print(f"Total Fare: ₱{fare:.2f}")

if __name__ == "__main__":
    main()
