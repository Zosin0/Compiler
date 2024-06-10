import subprocess
import sys

def main():
    print("Digite o código LPS1. Pressione Enter em uma linha vazia para finalizar a entrada.")

    pseudo_codigo = []
    while True:
        linha = input()
        if linha.strip() == "":
            break
        pseudo_codigo.append(linha)
    
    pseudo_codigo = "\n".join(pseudo_codigo)

    if pseudo_codigo:
        process = subprocess.Popen(
            [sys.executable, "analisadores.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(input=pseudo_codigo.encode('latin1'))
        print(stdout.decode('latin1'))
        if stderr:
            print(stderr.decode('latin1'), file=sys.stderr)

    else:
        print("Insira o código para prosseguir")

if __name__ == "__main__":
    main()
