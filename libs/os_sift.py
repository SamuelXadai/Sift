import os

def os_commands(code):
    if code[0] == "mkdir" and len(code) > 0:
        os.mkdir(code[1])
        return
    elif code[0] == "mkfile" and len(code) > 0:
        codee = code[1].split(" ", 1)
        if len(codee) < 2:
            with open(codee[0], 'w') as file:
                return
        
        with open(codee[0], 'w') as file:
            text = codee[1]
            file.write(text)
            return
    elif code[0] == ("bash" if os.name == "posix" else "batch") and len(code) > 1:
        command = code[1]
        os.system(command)
        return
