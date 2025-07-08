import sys
import os
import json
import requests as rqt
import libs.math_nash as math
import libs.os_nash as osn

last_version = rqt.get("https://raw.githubusercontent.com/SamuelXadai/Nash/refs/heads/main/version.txt?token=GHSAT0AAAAAADGP7MYVVJGJSGRZTVJDZ4CG2DG2IHA").text.strip()

if (sys.argv[1]) == "--version":
    with open('version.txt', 'r') as file:
        version = file.read()
        if version != last_version:
            print("New version available!")
            print(version)
        else:
            print(version)
        sys.exit(0)

data = {}
lib = {"math": False, "os": False}
ifp = False

with open(sys.argv[1], 'r') as file:
    code = file.readlines()

def parser(code, index):
    global ifp

    if len(code) == 0 or ifp == True:
        if code[0] == "else":
            if ifp == True:
                ifp = False
            else:
                ifp = True
        return
    
    
    if code[0] == "print" and len(code) >= 1:
        value = code[1].strip()
        print(data.get(value, value))
    elif code[0][0] == "!":
        return
    elif code[0] == "if" and len(code) > 0:
        cond = str(code[1])
        codition = eval(f"{cond}", data, {"true": True, "false": False})
        if codition == True:
            return
        ifp = True
        return
    elif code[0] == "set" and len(code) > 1:
        codee = code[1].split(" ")
        var = codee[0]
        value = codee[1]

        if value == "$input":
            data[var] = input()
            return
        
        data[var] = value
    elif code[0] == "use":
        if code[1] == "math":
            lib["math"] = True
        elif code[1] == "os":
            lib["os"] = True
        else:
            if len(code) == 2 and os.path.exists(f"{code[1]}.json"):
                with open(f"{code[1]}.json", 'r') as json_file:
                    lib_json = (json.load(json_file))
                    lib_json = lib_json.copy()
                    data.update(lib_json)
                    return
            print("ERROR: The library:", "".join(code[1]), "Not exist.")
    elif lib["math"]:
        var, value = math.math(code)
        data[var] = value
    elif lib["os"]:
        osn.os_commands(code)
    elif code[0] == "exit":
        if len(code) > 1:
            ret = int(code[1])
            sys.exit(ret)
        sys.exit()
    elif code[0] == "end":
        if ifp == True:
            ifp = False
        return
    else:
        print(f"ERROR: line {index + 1}:", " ".join(code), "not exist.")
        sys.exit(1)

for index, lines in enumerate(code):
    parser(lines.lower().strip().split(" ", 1), index)
data.clear()