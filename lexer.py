"""
Analizador Léxico para Identificadores y Números Reales
"""

import re


# Definición de tokens
class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor!r}, línea={self.linea}, col={self.columna})"


class AnalizadorLexico:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []

    def error(self, caracter):
        raise Exception(
            f"Carácter no válido: {caracter!r} en línea {self.linea}, columna {self.columna}"
        )

    def avanzar(self):
        """Avanza al siguiente carácter"""
        if self.pos < len(self.texto):
            if self.texto[self.pos] == "\n":
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            self.pos += 1

    def caracter_actual(self):
        """Retorna el carácter actual o None si llegamos al final"""
        if self.pos < len(self.texto):
            return self.texto[self.pos]
        return None

    def peek(self):
        """Mira el siguiente carácter sin avanzar"""
        pos_siguiente = self.pos + 1
        if pos_siguiente < len(self.texto):
            return self.texto[pos_siguiente]
        return None

    def saltar_espacios(self):
        """Salta espacios en blanco"""
        while self.caracter_actual() and self.caracter_actual().isspace():
            self.avanzar()

    def leer_numero(self):
        """Lee un número real: parte_entera(.parte_decimal)?"""
        resultado = ""
        col_inicio = self.columna
        linea_inicio = self.linea

        # Parte entera
        while self.caracter_actual() and self.caracter_actual().isdigit():
            resultado += self.caracter_actual()
            self.avanzar()

        # Parte decimal (opcional)
        if self.caracter_actual() == "." and self.peek() and self.peek().isdigit():
            resultado += self.caracter_actual()  # Agregar el punto
            self.avanzar()

            # Leer dígitos después del punto
            while self.caracter_actual() and self.caracter_actual().isdigit():
                resultado += self.caracter_actual()
                self.avanzar()

            return Token("REAL", float(resultado), linea_inicio, col_inicio)

        return Token("ENTERO", int(resultado), linea_inicio, col_inicio)

    def leer_identificador(self):
        """Lee un identificador: [a-zA-Z_][a-zA-Z0-9_]*"""
        resultado = ""
        col_inicio = self.columna
        linea_inicio = self.linea

        # Primer carácter: letra o guion bajo
        while self.caracter_actual() and (
            self.caracter_actual().isalnum() or self.caracter_actual() == "_"
        ):
            resultado += self.caracter_actual()
            self.avanzar()

        return Token("ID", resultado, linea_inicio, col_inicio)

    def analizar(self):
        """Analiza el texto completo y retorna lista de tokens"""
        self.tokens = []

        while self.caracter_actual():
            # Saltar espacios en blanco
            if self.caracter_actual().isspace():
                self.saltar_espacios()
                continue

            # Números (comienzan con dígito)
            if self.caracter_actual().isdigit():
                token = self.leer_numero()
                self.tokens.append(token)
                continue

            # Identificadores (comienzan con letra o guion bajo)
            if self.caracter_actual().isalpha() or self.caracter_actual() == "_":
                token = self.leer_identificador()
                self.tokens.append(token)
                continue

            # Carácter no reconocido
            self.error(self.caracter_actual())

        return self.tokens


# --- Programa principal ---
if __name__ == "__main__":
    # Ejemplos de prueba
    ejemplos = [
        "variable1 numero2 _privada",
        "3.14159 2.718 42",
        "x1 y2 z3 123.456",
        "miVariable 99.99 _temp 0.5",
    ]

    print("=" * 60)
    print("ANALIZADOR LÉXICO - Identificadores y Números Reales")
    print("=" * 60)

    for texto in ejemplos:
        print(f"\nEntrada: {texto!r}")
        print("-" * 40)

        lexer = AnalizadorLexico(texto)
        tokens = lexer.analizar()

        for token in tokens:
            print(f"  {token}")

    print("\n" + "=" * 60)

    # Prueba interactiva
    print("\nPrueba interactiva (escribe 'salir' para terminar):")
    while True:
        try:
            entrada = "hola mundo 123.3"  # input("\n>>> ")
            if entrada.lower() == "salir":
                break

            lexer = AnalizadorLexico(entrada)
            tokens = lexer.analizar()

            for token in tokens:
                print(f"  {token}")

        except Exception as e:
            print(f"Error: {e}")
