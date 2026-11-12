
import json
import os

class BloodSystem:

    def __init__(self):
        self.file = "blood.json"

        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {"donors": [], "requests": []}

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    # Register Donor
    def add_donor(self):
        name = input("Donor name: ")

        try:
            age = int(input("Donor age: "))
        except ValueError:
            print("Please enter a valid age!")
            return

        if age < 18 or age > 65:
            print("Age must be between 18 and 65!")
            return

        group = input("Blood group: ").upper()
        city = input("City: ")

        if group not in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            print("Invalid blood group!")
            return

        self.data["donors"].append({
            "name": name,
            "age": age,
            "group": group,
            "city": city
        })

        self.save()
        print("Donor registered successfully!")

    # Register Hospital Request
    def add_request(self):
        hospital = input("Hospital name: ")
        group = input("Required blood group: ").upper()
        city = input("City: ")
        priority = input("Priority (Critical/Urgent/Normal): ").capitalize()

        if group not in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"] or priority not in ["Critical", "Urgent", "Normal"]:
            print("Invalid details!")
            return

        self.data["requests"].append({
            "hospital": hospital,
            "group": group,
            "city": city,
            "priority": priority
        })

        self.save()
        print("Request registered successfully!")

    # Priority Queue
    def priority_queue(self):
        order = {"Critical": 1, "Urgent": 2, "Normal": 3}

        requests = sorted(
            self.data["requests"],
            key=lambda x: order[x["priority"]]
        )

        for r in requests:
            print(r)

    # Find Matching Donors
    def find_donors(self):
        for r in self.data["requests"]:
            matches = [
                d for d in self.data["donors"]
                if d["group"] == r["group"]
                and d["city"].lower() == r["city"].lower()
            ]

            print("\nHospital:", r["hospital"])

            if matches:
                print("Matching donors:")
                for d in matches:
                    print(d["name"], "-", d["age"],
                          "years -", d["group"], "-", d["city"])
            else:
                print("ALERT: No matching donor available!")

    # Unfulfilled Requests
    def unfulfilled(self):
        for r in self.data["requests"]:
            found = any(
                d["group"] == r["group"]
                and d["city"].lower() == r["city"].lower()
                for d in self.data["donors"]
            )

            if not found:
                print("Unfulfilled:", r["hospital"], r["group"])

    # Main Menu
    def menu(self):
        while True:
            print("""
===== EMERGENCY BLOOD SYSTEM =====
1. Register Donor
2. Register Hospital Request
3. Priority Queue
4. Find Matching Donors
5. Unfulfilled Requests
6. Exit
""")

            ch = input("Enter choice: ")

            if ch == "1":
                self.add_donor()
            elif ch == "2":
                self.add_request()
            elif ch == "3":
                self.priority_queue()
            elif ch == "4":
                self.find_donors()
            elif ch == "5":
                self.unfulfilled()
            elif ch == "6":
                print("Thank you!")
                break
            else:
                print("Invalid choice!")

app = BloodSystem()
app.menu()