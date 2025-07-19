def math(code):
    if code[0] == "add" and len(code) > 1:
        codee = code[1].split(" ")
        vl1 = int(codee[0])
        vl2 = int(codee[1])
        var = codee[2]
        value = eval(f"{vl1} + {vl2}")

        return var, value
    
    if code[0] == "sub" and len(code) > 1:
        codee = code[1].split(" ")
        vl1 = int(codee[0])
        vl2 = int(codee[1])
        var = codee[2]
        value = eval(f"{vl1} - {vl2}")

        return var, value
    
    if code[0] == "mul" and len(code) > 1:
        codee = code[1].split(" ")
        vl1 = int(codee[0])
        vl2 = int(codee[1])
        var = codee[2]
        value = eval(f"{vl1} * {vl2}")

        return var, value
    
    if code[0] == "div" and len(code) > 1:
        codee = code[1].split(" ")
        vl1 = int(codee[0])
        vl2 = int(codee[1])
        var = codee[2]
        value = eval(f"{vl1} // {vl2}")

        return var, value
    
    if code[0] == "pow" and len(code) > 1:
        codee = code[1].split(" ")
        vl1 = int(codee[0])
        vl2 = int(codee[1])
        var = codee[2]
        value = eval(f"{vl1} ** {vl2}")

        return var, value
