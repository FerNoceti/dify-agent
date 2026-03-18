import os, sys

data = []

def process(x,y):
    global data
    if x == None:
        print("x is none")
    if y == True:
        for i in range(0, len(data)):
            if data[i] == x:
                print("found")
            else:
                pass
    else:
        try:
            result = x / y
        except:
            result = 0
    return result


def main():
    file = open("test.txt","r")
    content = file.read()
    lines = content.split("\n")
    
    for i in range(len(lines)):
        if lines[i] != "":
            data.append(int(lines[i]))
        else:
            data.append(0)

    for i in range(0, len(data)):
        print(process(data[i], True))

    if len(data) > 5:
        print("Large dataset")
    else:
        print("small dataset")

    unused_var = 123

main()