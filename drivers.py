import customtkinter as ctk
import csv
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BOOKINGS_FILE = "bookings.csv"

class DriverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DuckDash Driver Panel")
        self.geometry("600x400")
        self.selected_ride_index = None

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

        self.load_bookings()

    def load_bookings(self):
        self.ride_listbox.delete("0.0", "end")
        self.bookings = []

        if not os.path.exists(BOOKINGS_FILE):
            self.ride_listbox.insert("0.0", "No bookings available.")
            return

        with open(BOOKINGS_FILE, newline="") as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if row["Status"].lower() == "pending":
                    self.bookings.append(row)
                    ride_info = f"[{i}] {row['Name']} | From: {row['Pickup']} → {row['Dropoff']} at {row['Time']}"
                    self.ride_listbox.insert("end", ride_info + "\n")

    def select_ride(self):
        index_prompt = ctk.CTkInputDialog(text="Enter ride number to select:", title="Select Ride")
        index_str = index_prompt.get_input()
        if index_str and index_str.isdigit():
            index = int(index_str)
            if 0 <= index < len(self.bookings):
                self.selected_ride_index = index
                self.accept_button.configure(state="normal")
                ctk.CTkMessagebox(title="Ride Selected", message=f"Ride #{index} selected.", icon="check")
            else:
                ctk.CTkMessagebox(title="Invalid", message="Invalid ride index!", icon="cancel")

    def accept_ride(self):
        if self.selected_ride_index is not None:
            with open(BOOKINGS_FILE, newline="") as file:
                rows = list(csv.DictReader(file))

            pending_rides = [r for r in rows if r["Status"].lower() == "pending"]
            ride_to_accept = self.bookings[self.selected_ride_index]
            for row in rows:
                if (row["Name"] == ride_to_accept["Name"] and 
                    row["Pickup"] == ride_to_accept["Pickup"] and 
                    row["Dropoff"] == ride_to_accept["Dropoff"]):
                    row["Status"] = "Accepted"
                    break

            with open(BOOKINGS_FILE, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Name", "Pickup", "Dropoff", "Time", "Status"])
                writer.writeheader()
                writer.writerows(rows)

            ctk.CTkMessagebox(title="Success", message="Ride accepted!", icon="check")
            self.accept_button.configure(state="disabled")
            self.load_bookings()

if __name__ == "__main__":
    app = DriverApp()
    app.mainloop()
