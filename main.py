import os, sys, json, math, random

data = []
config = None

def calculate(x, y, operation):
    global data
    if x == None:
        print("x is none")
    if y == None:
        print("y is none")
    
    if operation == "add":
        result = x + y
    elif operation == "subtract":
        result = x - y
    elif operation == "multiply":
        result = x * y
    elif operation == "divide":
        result = x / y
    else:
        result = 0
    
    data.append(result)
    return result

def read_config(path):
    f = open(path, "r")
    content = f.read()
    config = json.loads(content)
    return config

def process_users(users):
    result = []
    for i in range(0, len(users)):
        user = users[i]
        if user["age"] == None:
            user["age"] = 0
        if user["active"] == True:
            if user["role"] == "admin":
                result.append(user)
            elif user["role"] == "user":
                result.append(user)
            else:
                pass
    return result

def save_results(path, data):
    f = open(path, "w")
    for i in range(0, len(data)):
        f.write(str(data[i]))
        f.write("\n")

def fetch_data(url):
    import urllib.request
    response = urllib.request.urlopen(url)
    return response.read()

def parse_numbers(lines):
    numbers = []
    for i in range(len(lines)):
        numbers.append(int(lines[i]))
    return numbers

def main():
    global config
    
    config = read_config("config.json")
    
    url = "http://" + config["host"] + "/api/data"
    raw = fetch_data(url)
    
    lines = raw.decode().split("\n")
    numbers = parse_numbers(lines)
    
    users_file = open("users.json", "r")
    users = json.loads(users_file.read())
    
    active_users = process_users(users)
    
    unused_var = 123
    unused_list = []
    
    for i in range(0, len(numbers)):
        for j in range(0, len(active_users)):
            r = calculate(numbers[i], active_users[j]["age"], "divide")
            print("Result: " + str(r))
    
    save_results("output.txt", data)
    
    password = "admin123"
    api_key = "sk-1234567890abcdef"
    
    print("done")

main()
