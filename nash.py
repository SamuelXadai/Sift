import sys
import libs.math_nash as math
import libs.extern_nash as ext

data = {}
lib = {"math": False, "extern": False}
ifp = False

with open(sys.argv[1], 'r') as file:
    code = file.readlines()

def parser(code):
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
        elif code[1] == "extern":
            lib["extern"] = True
        else:
            print("ERROR: The library:", "".join(code[1]), "Not exist.")
    elif lib["math"]:
        var, value = math.math(code)
        data[var] = value
    elif lib["extern"]:
        ext.extern(code)
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
        if ifp == True:
            return
        print("ERROR:", " ".join(code), "not exist.")
        sys.exit(1)

for lines in code:
    parser(lines.lower().strip().split(" ", 1))
data.clear()