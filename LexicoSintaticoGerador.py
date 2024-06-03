def geradorDeCodigo(traducao):
    codigo = "#include <stdio.h>\n\nint main() {\n" + traducao + "\nreturn 0;\n}"
    return codigo

def tradutorC(codigo):
    traducao = {
        "=": "{var} = {val};",
        "G": "scanf(\"%d\", &{var});",
        "+": "{var} = {val1} + {val2};",
        "-": "{var} = {val1} - {val2};",
        "*": "{var} = {val1} * {val2};",
        "/": "{var} = {val1} / {val2};",
        "%": "{var} = {val1} % {val2};",
        "P": "printf(\"%d\\n\", {val});",
        "I": "if ({comp}) {{\n{cmd}\n}}",
        "W": "while ({comp}){abre}  {cmd}",
        "{": "{",
        "}": "}"
    }
    
    operadores = {
        "=": "==",
        "<": "<",
        "#": "!="
    }

    linhas = codigo.split('\n')
    codigo_c = []
    bloco_comandos = []
    for linha in linhas:
        partes = linha.strip().split()
        if not partes:
            continue
        comando = partes[0]
        if comando in traducao:
            if comando in ["=", "G"]:
                var = partes[1]
                val = partes[2] if comando == "=" else ""
                codigo_c.append(traducao[comando].format(var=var, val=val))
            elif comando in ["+", "-", "*", "/", "%"]:
                var = partes[1]
                val1 = partes[2]
                val2 = partes[3]
                codigo_c.append(traducao[comando].format(var=var, val1=val1, val2=val2))
            elif comando == "P":
                val = partes[1]
                codigo_c.append(traducao[comando].format(val=val))
            elif comando in ["I", "W"]:
                var = partes[1]
                oper = operadores.get(partes[2], partes[2])
                val = partes[3]
                comp = f"{var} {oper} {val}"

                bloco_comandos.append((traducao[comando].format(comp=comp, abre=linha[-1], cmd="{cmd}"), comando, len(codigo_c)))
                codigo_c.append((traducao[comando].format(comp=comp, abre=linha[-1], cmd="{cmd}")))

            elif comando[-1] == "{":

                bloco_comandos.append(("{", comando, len(codigo_c)))
            elif comando == "}":
                cmd_codigo = []
                while bloco_comandos and bloco_comandos[-1][1] != "{":
                    bloco = bloco_comandos.pop()
                    cmd_codigo.insert(0, codigo_c.pop())
                if bloco_comandos:
                    bloco = bloco_comandos.pop()
                    codigo_c[bloco[2]] = bloco[0].replace("{cmd}", "\n".join(cmd_codigo))
                codigo_c.append("}")

    codigo_c_final = "\n".join(codigo_c)
    return codigo_c_final.replace("{cmd}", "")

if __name__ == "__main__":
    # Exemplo de uso:
    pseudo_codigo = """
    G n
    G p
    = i 0
    W i # n {
    * a p i
    P a
    + i i 1
    }
    """
    
    codigo_c_traduzido = tradutorC(pseudo_codigo)
    codigo_c = geradorDeCodigo(codigo_c_traduzido)
    print(codigo_c)
