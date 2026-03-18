import os
import sys
import json

data = []

def process(x, y):
    if x is None:
        print("x is None")

    if y:
        for value in data:
            if value == x:
                print("found")
    else:
        try:
            result = x / y
        except ZeroDivisionError:
            result = 0
    return result


def read_file(filepath):
    with open(filepath, "r") as file:
        return file.read()


def main():
    content = read_file("test.json")
    lines = content.split("\n")

    for line in lines:
        if line.strip() != "":
            try:
                data.append(int(line))
            except ValueError:
                data.append(0)
        else:
            data.append(0)

    for value in data:
        print(process(value, True))

    if len(data) > 5:
        print("Large dataset")
    else:
        print("Small dataset")


main()
