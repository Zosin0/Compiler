def geradorDeCodigo(traducao):
    codigo = "#include <stdio.h>\n\nint main(){\n" + traducao + "\nreturn 0;\n}"
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
        "W": "while ({comp}) {{\n{cmd}\n}}",
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
    bloco_aberto = False
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
                bloco_aberto = True
                codigo_c.append(traducao[comando].format(comp=comp, cmd=""))
            elif comando == "{":
                codigo_c.append("{")
            elif comando == "}":
                codigo_c.append("}")
                bloco_aberto = False
            else:
                if bloco_aberto:
                    if comando in ["+", "-", "*", "/", "%"]:
                        var = partes[0]
                        val1 = partes[1]
                        val2 = partes[2]
                        codigo_c.append(f"{traducao[comando].format(var=var, val1=val1, val2=val2)}")
                    elif comando == "P":
                        val = partes[0]
                        codigo_c.append(f"{traducao[comando].format(val=val)}")
                    elif comando == "=":
                        var = partes[0]
                        val = partes[1]
                        codigo_c.append(f"{traducao[comando].format(var=var, val=val)}")
                else:
                    # Comando desconhecido fora de bloco
                    pass

    return "\n".join(codigo_c)

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
