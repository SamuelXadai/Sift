import sys
import os
import json
import re
import requests as rqt
import libs.math_sift as math
import libs.os_sift as oss

# é o link do version.txt
# https://raw.githubusercontent.com/SamuelXadai/Sift/refs/heads/main/version.txt
version = "SIFT: 1.1"

if (sys.argv[1]) == "--version":
    last_version = rqt.get("https://raw.githubusercontent.com/SamuelXadai/Sift/refs/heads/main/version.txt").text.strip()
    if not version == last_version:
        print("New version! See https://github.com/SamuelXadai/Sift")
        print(version)
        sys.exit(0)
    print(version)
    sys.exit(0)

data = {"$true": True, "$false": False}
lib = {"math": False, "os": False}
f_stack = {}
falloc = False
function_name = None
ifp = False

# CALL
COMMAND_LINE = False

if (sys.argv[1]) == "-c":
    COMMAND_LINE = True
    if not len(sys.argv) > 1:
        print("ERROR: COMMAND_LINE")
        sys.exit(1)
    code = " ".join((sys.argv[2:]))

if COMMAND_LINE == False:
    with open(sys.argv[1], 'r') as file:
        code = file.readlines()

def parser(code, index):
    global ifp, falloc, function_name, data

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

    if falloc:
        if code[0] == "end".lower():
            falloc = False
            return
        all_line = " ".join(code)
        f_stack[function_name].append(all_line)
        return
    
    if code[0] == "print" and len(code) >= 1:
        value = code[1].strip()
        if '"' in value:
            value_str = re.findall(r'"(.*?)"', value)
            value = re.sub(r'"(.*?)"', "", value).strip()

        print("".join(value_str).strip())
        print(eval(value.replace("$", ""), 
        {key.replace("$", ""): valor for key, valor in data.items()}) if len(value) > 0 else "".strip())
        return
    elif code[0].startswith("!"):
        return
    elif code[0] == "if" and len(code) > 0:
        if COMMAND_LINE:
            print("ERROR: 'if' not is possible.")
            return
        cond = str(code[1])
        codition = eval(cond.replace("$", ""), {key.replace("$", ""): valor for key, valor in data.items()})
        if codition == True:
            return
        ifp = True
        return
    elif code[0].startswith("$") and len(code) > 1:
        if COMMAND_LINE:
            print("ERROR: Variables not is possible.")
            return
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
        codee = code[1].strip().split(" ", 1)
        if code[1] == "math":
            lib["math"] = True
            return
        elif code[1] == "os":
            lib["os"] = True
            return
        elif codee[0] == "json":
            if len(code) == 2 and os.path.exists(f"{codee[1]}.json"):
                with open(f"{codee[1]}.json", 'r') as json_file:
                    lib_json = (json.load(json_file))
                    lib_json = lib_json.copy()
                    data.update(lib_json)
                    return
                pass
        else:
            print("ERROR: The library {} not exist.".format(code[1]))
            return
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
                    commands = commands.replace('"', "")
                    parser(commands.lower().strip().split(" ", 1), index)
                    continue
            else:
                continue
    else:
        if COMMAND_LINE and index == 1000:
            print("ERROR: COMMAND_LINE error: {} command not exist".format(" ".join(code)))
            sys.exit(1)
        temp = "".join(code[0]).strip()
        if len(temp) < 1:
            return
        print(f"ERROR: line {index + 1}:", " ".join(code), "command not exist.")
        sys.exit(1)

if COMMAND_LINE == False:
    for index, lines in enumerate(code):
        lines = lines.replace('"', "\"")
        parser(lines.lower().strip().split(" ", 1), index)
else:
    code = code.replace('"', "\"")
    parser(code.lower().strip().split(" ", 1), 1000)

f_stack.clear()
data.clear()
