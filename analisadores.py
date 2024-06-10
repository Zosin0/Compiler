import re
import sys

# Gramática da linguagem: LPS1
LPS1 = {
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
    'NUMBER': r'\b\d+\b',  # Permitir números com mais de um dígito
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
        for token_type, regex in LPS1.items():
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
        self.commands = []
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
        self.commands.append((f'G {variable}', f'gets(str); sscanf(str, "%d", &{variable});'))
        self.proximo_token()

    def parse_assign_command(self):
        self.proximo_token()  # Skip '='
        var = self.current_token.value
        self.proximo_token()
        val = self.current_token.value
        self.c_code.append(f'{var} = {val};')
        self.commands.append((f'= {var} {val}', f'{var} = {val};'))
        self.proximo_token()

    def parse_add_command(self):
        self.proximo_token()  # Skip '+'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} + {val2};')
        self.commands.append((f'+ {var} {val1} {val2}', f'{var} = {val1} + {val2};'))
        self.proximo_token()

    def parse_sub_command(self):
        self.proximo_token()  # Skip '-'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} - {val2};')
        self.commands.append((f'- {var} {val1} {val2}', f'{var} = {val1} - {val2};'))
        self.proximo_token()

    def parse_mult_command(self):
        self.proximo_token()  # Skip '*'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} * {val2};')
        self.commands.append((f'* {var} {val1} {val2}', f'{var} = {val1} * {val2};'))
        self.proximo_token()

    def parse_div_command(self):
        self.proximo_token()  # Skip '/'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} / {val2};')
        self.commands.append((f'/ {var} {val1} {val2}', f'{var} = {val1} / {val2};'))
        self.proximo_token()

    def parse_mod_command(self):
        self.proximo_token()  # Skip '%'
        var = self.current_token.value
        self.proximo_token()
        val1 = self.current_token.value
        self.proximo_token()
        val2 = self.current_token.value
        self.c_code.append(f'{var} = {val1} % {val2};')
        self.commands.append((f'% {var} {val1} {val2}', f'{var} = {val1} % {val2};'))
        self.proximo_token()

    def parse_print_command(self):
        self.proximo_token()  # Skip 'P'
        val = self.current_token.value
        self.c_code.append(f'printf("%d\\n", {val});')
        self.commands.append((f'P {val}', f'printf("%d\\n", {val});'))
        self.proximo_token()

    def parse_while_command(self):
        self.proximo_token()  # Skip 'W'
        condition = self.parse_comparison()
        self.c_code.append(f'while ({condition}) {{')
        self.commands.append((f'W {condition}', f'while ({condition}) {{'))
        self.parse_commands()
        self.c_code.append('}')
        self.commands.append(('}', '}'))

    def parse_if_command(self):
        self.proximo_token()  # Skip 'I'
        condition = self.parse_comparison()
        self.c_code.append(f'if ({condition}) {{')
        self.commands.append((f'I {condition}', f'if ({condition}) {{'))
        self.parse_commands()
        self.c_code.append('}')
        self.commands.append(('}', '}'))

    def parse_composite_command(self):
        self.proximo_token()  # Skip '{'
        self.commands.append(('{', '{'))
        self.parse_commands()
        self.proximo_token()  # Skip '}'
        self.commands.append(('}', '}'))

    def parse_comparison(self):
        var = self.current_token.value
        self.proximo_token()
        operator = self.current_token.value
        self.proximo_token()
        val = self.current_token.value
        self.proximo_token()
        op_map = {'=': '==', '#': '!=', '<': '<'}
        return f'{var} {op_map[operator]} {val}'

def generate_table(commands):
    table = "| Comando | código em C |\n"
    table += "| --- | --- |\n"
    for command, c_code in commands:
        table += f"| {command} | {c_code} |\n"
    return table

if __name__ == "__main__":
    pseudo_codigo = sys.stdin.read()
    tokens = convertToken(pseudo_codigo)
    parser = Parser(tokens)
    codigo_c_traduzido = parser.parse()
    table = generate_table(parser.commands)

    print(codigo_c_traduzido)
    print("\nTabela de Traduções:\n")
    print(table)
