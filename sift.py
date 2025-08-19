import sys
import os
import json
import requests as rqt
import configparser as cfgini
import libs.math_sift as math
import libs.os_sift as oss

# é o link do version.txt
#https://raw.githubusercontent.com/SamuelXadai/Sift/refs/heads/main/version.txt

if (sys.argv[1]) == "--version":
    with open('version.txt', 'r') as file:
        version = file.read()
        last_version = rqt.get('https://raw.githubusercontent.com/SamuelXadai/Sift/refs/heads/main/version.txt').text.strip()
        if not version.__eq__(last_version):
            print("NEW Version! is {}".format(last_version))
        print(version)
        sys.exit(0)

data = {"$true": True, "$false": False}
lib = {"math": False, "os": False}
f_stack = {}
falloc = False
function_name = None
ifp = False

with open(sys.argv[1], 'r') as file:
    code = file.readlines()

def parser(code, index):
    global ifp, falloc, function_name

    if len(code[0]) == 1 or ifp:
        if code[0] == "else":
            if ifp == True:
                ifp = False
            else:
                ifp = True
        return
    
    for key in data.keys():
        if "$" in key.lower():
            pass
        else:
            print(f"ERROR: The variable \"{key}\" not have '$'.")
            sys.exit(1)
            return

    if falloc and code[0]:
        if code[0] == "end":
            falloc = False
            return
        if code[0] == "":
            return
        all_line = " ".join(code)
        f_stack[function_name].append(all_line)
        return
    
    if code[0] == "print" and len(code) >= 1:
        value = code[1].strip()
        print(data.get(value, eval(value.replace("$", ""), {key.replace("$", ""): valor for key, valor in data.items()})))
    elif code[0].startswith("!"):
        return
    elif code[0] == "if" and len(code) > 0:
        cond = str(code[1])
        codition = eval(cond.replace("$", ""), {key.replace("$", ""): valor for key, valor in data.items()})
        if codition == True:
            return
        ifp = True
        return
    elif code[0].startswith("$") and len(code) > 1:
        var = code[0].strip()
        value = code[1].strip()
        if value.startswith("="):
            pass
        elif var.endswith("="):
            if value.startswith("="):
                print("ERROR: Have two egual.")
                sys.exit(1)
            var = var.replace("=", "")
            data[var] = eval(value.replace("$", ""), {key.replace("$", ""): valor for key, valor in data.items()})
            return
        else:
            print("ERROR: Not have equal.")
            sys.exit(1)
        if value == "$input":
            data[var] = input()
            return
        elif value == "$get":
            value = data.get(codee[2], "<ERROR>")
            if value == "<ERROR>":
                print("ERROR: In \"$get\", Check you code")
                sys.exit(1)
                return
            data[var] = value
            return
        data[var] = eval(value[1:].replace("$", ""), {key.replace("$", ""): valor for key, valor in data.items()})
    elif code[0] == "func" and len(code) > 1:
        function_name = code[1]
        if not function_name in f_stack.keys():
            f_stack[function_name] = []
            falloc = [True, function_name]
            return
        print("ERROR: The function {} alreready exist.".format(function_name))
        sys.exit(1)
    elif code[0] == "use":
        if code[1] == "math":
            lib["math"] = True
            return
        elif code[1] == "os":
            lib["os"] = True
            return
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
        oss.os_commands(code)
    elif code[0] == "exit":
        if len(code) > 1:
            ret = int(code[1])
            sys.exit(ret)
        sys.exit()
    elif code[0] == "end":
        if ifp == True:
            ifp = False
        elif falloc:
            falloc = False
        return
    elif code[0] in f_stack.keys():
        func = code[0]
        for i in f_stack.keys():
            if i == func:
                for e in range(len(f_stack[func])):
                    commands = "".join(f_stack[func][e])
                    parser(commands.lower().strip().split(" ", 1), index)
                    continue
            else:
                continue
    else:
        print(f"ERROR: line {index + 1}:", " ".join(code), "not exist.")
        sys.exit(1)

for index, lines in enumerate(code):
    lines = lines.replace('"', "\"")
    parser(lines.lower().strip().split(" ", 1), index)
f_stack.clear()
data.clear()
