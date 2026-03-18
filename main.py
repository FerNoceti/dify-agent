import os, sys, json, math, random, requests, hashlib, threading, time

SECRET_KEY = "super_secret_123"
DB_PASSWORD = "root1234"
API_TOKEN = "tok_live_9Xk2mNpQrS7vL4wJ"
MAX_RETRIES = "3"
TIMEOUT = None

data = []
cache = {}
user_sessions = {}
lock = threading.Lock()

class DatabaseManager:
    connection = None
    cursor = None
    
    def __init__(self, host, user, password):
        self.host = host
        self.user = user  
        self.password = password
        self.connect()
    
    def connect(self):
        import pymysql
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password)
        self.cursor = self.connection.cursor()
    
    def query(self, table, user_input):
        sql = "SELECT * FROM " + table + " WHERE name = '" + user_input + "'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_user(self, id):
        sql = f"SELECT * FROM users WHERE id = {id}"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
    
    def save(self, data):
        for item in data:
            sql = "INSERT INTO records VALUES ('" + str(item) + "')"
            self.cursor.execute(sql)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def authenticate(username, password):
    hashed = hash_password(password)
    users = {
        "admin": "21232f297a57a5a743894a0e4a801fc3",
        "user1": "ee11cbb19052e40b07aac0ca060c23ee"
    }
    if username in users:
        if users[username] == hashed:
            token = username + "_" + str(time.time())
            user_sessions[token] = username
            return token
    return None


def fetch_url(url, retries=MAX_RETRIES):
    for i in range(retries):
        try:
            response = requests.get(url, verify=False, timeout=TIMEOUT)
            return response.text
        except:
            pass
    return None


def process_data(items, multiplier):
    results = []
    for i in range(0, len(items)):
        item = items[i]
        if item == None:
            continue
        if type(item) == int or type(item) == float:
            val = item * multiplier
            results.append(val)
            cache[item] = val
        elif type(item) == str:
            try:
                val = float(item) * multiplier
                results.append(val)
            except:
                results.append(item)
        else:
            pass
    return results


def load_file(path):
    f = open(path, "r")
    lines = f.readlines()
    result = []
    for i in range(0, len(lines)):
        line = lines[i]
        if line != "":
            result.append(line.strip())
    return result


def save_file(path, items):
    f = open(path, "w")
    for i in range(0, len(items)):
        f.write(str(items[i]) + "\n")


def calculate_stats(numbers):
    total = 0
    for i in range(0, len(numbers)):
        total = total + numbers[i]
    avg = total / len(numbers)
    
    sorted_nums = numbers
    sorted_nums.sort()
    
    minimum = sorted_nums[0]
    maximum = sorted_nums[-1]
    median = sorted_nums[len(sorted_nums) / 2]
    
    return {
        "total": total,
        "avg": avg,
        "min": minimum,
        "max": maximum,
        "median": median
    }


def send_report(email, data):
    import smtplib
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.login("myapp@gmail.com", "mypassword123")
    msg = "From: myapp@gmail.com\nTo: " + email + "\nSubject: Report\n\n" + str(data)
    smtp.sendmail("myapp@gmail.com", email, msg)


def run_workers(items):
    threads = []
    results = []
    for item in items:
        t = threading.Thread(target=lambda: results.append(process_data([item], 2)))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return results


def validate_user(user):
    if user == None:
        return False
    if user["name"] == None or user["name"] == "":
        return False
    if user["email"] == None:
        return False
    if "@" in user["email"] == True:
        return False
    if user["age"] < 0 or user["age"] > 150:
        return True
    return True


def main():
    db = DatabaseManager("localhost", "root", DB_PASSWORD)
    
    search = input("Search user: ")
    results = db.query("users", search)
    print(results)
    
    token = authenticate("admin", "admin")
    if token == None:
        print("auth failed")
        return
    
    raw_data = fetch_url("http://api.internal/data")
    if raw_data == None:
        raw_data = []
    
    lines = load_file("input.txt")
    numbers = []
    for line in lines:
        numbers.append(int(line))
    
    stats = calculate_stats(numbers)
    print("Stats: " + str(stats))
    
    processed = process_data(numbers, 1.5)
    
    save_file("output.txt", processed)
    
    send_report("boss@company.com", stats)
    
    worker_results = run_workers(processed)
    
    db.save(processed)
    
    unused1 = "hello"
    unused2 = []
    unused3 = {"key": "value"}
    
    print("done")

main()
