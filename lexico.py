class TokenType:
    COMMAND = "COMMAND"
    VARIABLE = "VARIABLE"
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    ERROR = "ERROR"
    END = "END"

def get_next_token(source):
    length = len(source)

    # Ignorar espaços em branco
    source = source.strip()

    if length == 0:
        return (TokenType.END, '')

    c = source[0]
    if c.isupper():  
        return (TokenType.COMMAND, c)
    elif c.islower():  
        token = c
        idx = 1
        while idx < length and source[idx].islower():
            token += source[idx]
            idx += 1
        return (TokenType.VARIABLE, token)
    elif c.isdigit():  
        token = c
        idx = 1
        while idx < length and source[idx].isdigit():
            token += source[idx]
            idx += 1
        return (TokenType.NUMBER, token)
    elif c in "=<#*+-/{}":  
        return (TokenType.OPERATOR, c)
    else:
        return (TokenType.ERROR, c)  

def main():
    input_string = "G n\nG p\n= i 0\nW i # n {\n * a p i\n P a\n + i i 1\n}"

    while True:
        token_type, token_value = get_next_token(input_string)
        if token_type == TokenType.END:
            break
        print("Token:", token_type, "Valor:", token_value)
        input_string = input_string[len(token_value):].strip()  # Remover o token encontrado da string de entrada

if __name__ == "__main__":
    main()
