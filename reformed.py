import re

# Gramática da linguagem: LPS1
LSP1 = {
    'G': r'\bG\b',
    'P': r'\bP\b',
    'W': r'\bW\b',
    'I': r'\bI\b',
    '=': r'=',
    '+': r'\+',
    '-': r'-',
    '*': r'\*',
    '/': r'/',
    '%': r'%',
    '#': r'#',
    '<': r'<',
    'VARIABLE': r'\b[a-z]\b',
    'NUMBER': r'\b\d\b',
    '{': r'\{',
    '}': r'\}',
    'WHITESPACE': r'\s+',
    'UNKNOWN': r'.'
}

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def convertToken(code):
    tokens = []
    indice = 0
    while indice < len(code):
        match = None
        for token_type, regex in LSP1.items():
            pattern = re.compile(regex)
            match = pattern.match(code, indice)
            if match:
                if token_type != 'WHITESPACE':
                    tokens.append(Token(token_type, match.group(0)))
                indice = match.end(0)
                break
        if not match:
            tokens.append(Token('UNKNOWN', code[indice]))
            indice += 1
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.proximo_token()
        self.c_code = []
    
    def proximo_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None
    
    def parse(self):
        self.c_code.append("#include <stdio.h>")
        self.c_code.append("int main() {")
        self.c_code.append("int a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, w, x, y, z;")
        self.c_code.append('char str[512];')
        self.parse_commands()
        self.c_code.append("return 0;")
        self.c_code.append("}")
        return "\n".join(self.c_code)
    
    def parse_commands(self):
        while self.current_token and self.current_token.type != '}':
            self.parse_command()
    
    def parse_command(self):
        if self.current_token.type == 'G':
            self.parse_get_command()
        elif self.current_token.type == '=':
            self.parse_assign_command()
        elif self.current_token.type == '+':
            self.parse_add_command()
        elif self.current_token.type == '-':
            self.parse_sub_command()
        elif self.current_token.type == '*':
            self.parse_mult_command()
        elif self.current_token.type == '/':
            self.parse_div_command()
        elif self.current_token.type == '%':
            self.parse_mod_command()
        elif self.current_token.type == 'P':
            self.parse_print_command()
        elif self.current_token.type == 'W':
            self.parse_while_command()
        elif self.current_token.type == 'I':
            self.parse_if_command()
        elif self.current_token.type == '{':
            self.parse_composite_command()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")
    
    def parse_get_command(self):
        self.proximo_token()  # Skip 'G'
        variable = self.current_token.value
        self.c_code.append(f'gets(str); sscanf(str, "%d", &{variable});')
        self.proximo_token()
    
    def parse_assign_command(self):
        self.proximo_token()  # Skip '='
        var = self.current_token.value
        self.proximo_token()
        val = self.current_token.value
        self.c_code.append(f'{var} = {val};')
        self.proximo_token()
    
    def parse_add_command(self):
        self.proximo_token()  # Skip '+'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} + {val2};')
        self.proximo_token()
    
    def parse_sub_command(self):
        self.proximo_token()  # Skip '-'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} - {val2};')
        self.proximo_token()
    
    def parse_mult_command(self):
        self.proximo_token()  # Skip '*'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} * {val2};')
        self.proximo_token()
    
    def parse_div_command(self):
        self.proximo_token()  # Skip '/'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} / {val2};')
        self.proximo_token()
    
    def parse_mod_command(self):
        self.proximo_token()  # Skip '%'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} % {val2};')
        self.proximo_token()
    
    def parse_print_command(self):
        self.proximo_token()  # Skip 'P'
        val = self.current_token.value
        self.c_code.append(f'printf("%d\\n", {val});')
        self.proximo_token()
    
    def parse_while_command(self):
        self.proximo_token()  # Skip 'W'
        condition = self.parse_comparison()
        self.c_code.append(f'while ({condition}) {{')
        self.parse_command()
        self.c_code.append('}')
    
    def parse_if_command(self):
        self.proximo_token()  # Skip 'I'
        condition = self.parse_comparison()
        self.c_code.append(f'if ({condition}) {{')
        self.parse_command()
        self.c_code.append('}')
    
    def parse_composite_command(self):
        self.proximo_token()  # Skip '{'
        self.parse_commands()
        self.proximo_token()  # Skip '}'
    
    def parse_comparison(self):
        var = self.current_token.value
        self.proximo_token()
        operator = self.current_token.value
        self.proximo_token()
        val = self.current_token.value
        self.proximo_token()
        op_map = {'=': '==', '#': '!=', '<': '<'}
        return f'{var} {op_map[operator]} {val}'

def geradorDeCodigo(traducao):
    #codigo = "#include <stdio.h>\n\nint main() {\n" + traducao + "\nreturn 0;\n}"
    codigo = traducao
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
        "W": "while ({comp}){{\n{cmd}\n}}",
        "{": "{",
        "}": "}"
    }
    
    operadores = {
        "=": "==",
        "<": "<",
        "#": "!="
    }

    linhas = codigo.strip().split('\n')
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
                bloco_comandos.append((traducao[comando].format(comp=comp, cmd="{cmd}"), comando, len(codigo_c)))
                codigo_c.append(traducao[comando].format(comp=comp, cmd="{cmd}"))
            elif comando == "{":
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
    = i 2
    % a n i
    W i < n {
        I a = 0 = i n
        + i i 1
        % a n i
    }
    I a = 0 P 0
    I a # 0 P 1

    """
    
    tokens = convertToken(pseudo_codigo)
    parser = Parser(tokens)
    codigo_c_traduzido = parser.parse()
    codigo_c = geradorDeCodigo(codigo_c_traduzido)
    print(codigo_c)
