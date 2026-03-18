import os, sys
from datetime import datetime

SECRET = "hardcoded_secret_key"
DEBUG = True

class UserManager:
    users = []
    
    def __init__(self):
        self.db = open("users.db", "r")
    
    def add_user(self, name, email, password):
        for i in range(0, len(self.users)):
            if self.users[i]["email"] == email:
                return False
        user = {
            "name": name,
            "email": email,
            "password": password,
            "created": str(datetime.now()),
            "active": True
        }
        self.users.append(user)
        return True
    
    def get_user(self, email):
        for i in range(0, len(self.users)):
            if self.users[i] == None:
                continue
            if self.users[i]["email"] == email:
                return self.users[i]
        return None
    
    def delete_user(self, email):
        for i in range(0, len(self.users)):
            if self.users[i]["email"] == email:
                self.users.pop(i)
                return True

    def update_password(self, email, new_password):
        user = self.get_user(email)
        if user != None:
            user["password"] = new_password
            return True
        return False

    def list_active(self):
        active = []
        for i in range(0, len(self.users)):
            if self.users[i]["active"] == True:
                active.append(self.users[i])
        return active


def log(msg, level="INFO"):
    f = open("app.log", "a")
    f.write("[" + level + "] " + str(datetime.now()) + " - " + msg + "\n")


def send_email(to, subject, body):
    import smtplib
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.login("app@gmail.com", "password123")
    msg = "To: " + to + "\nSubject: " + subject + "\n\n" + body
    server.sendmail("app@gmail.com", to, msg)


def validate_email(email):
    if "@" in email == True:
        return True
    return False


def parse_age(value):
    age = int(value)
    if age < 0:
        return 0
    return age


def calculate_discount(price, discount):
    if discount > 1:
        discount = discount / 100
    final = price - (price * discount)
    return round(final, 2)


def load_users_from_file(path):
    f = open(path, "r")
    import json
    data = json.load(f)
    return data


def save_report(users, path):
    f = open(path, "w")
    import json
    json.dump(users, f)


def main():
    manager = UserManager()

    manager.add_user("Alice", "alice@example.com", "alice123")
    manager.add_user("Bob", "bob@example.com", "bob456")
    manager.add_user(None, None, None)

    if validate_email("alice@example.com") == True:
        log("Valid email")

    user = manager.get_user("alice@example.com")
    if user != None:
        manager.update_password("alice@example.com", "newpass")
        send_email(user["email"], "Welcome", "Hello " + user["name"])

    try:
        age = parse_age("not_a_number")
    except:
        age = 0

    prices = [100, 200, 300]
    for i in range(0, len(prices)):
        d = calculate_discount(prices[i], 20)
        print("Discounted: " + str(d))

    loaded = load_users_from_file("backup.json")
    save_report(loaded, "report.json")

    unused = "nothing"
    x = 1 + 1

    print("done")

main()
