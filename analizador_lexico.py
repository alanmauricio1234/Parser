"""
	Analizador Lexico
"""

import tipo_token
import subtipos_token
import token

class AnalizadorLexico:
# Atributos de clase
	num_linea = 1
	L = []
	codigo = ""
	palabras_reservadas=["Proceso","FinProceso","Funcion",
                         "FinFuncion","Regresar","Entero","Real","Logico",
                         "Caracter","Falso","Verdadero","Leer","Escribir",
                         "Si","Entonces","Sino","FinSi","Segun","FinSegun",
                         "Romper","Omision","Mientras","Hacer","FinMientras",
                         "Para","Con","Hasta","Paso","FinPara","Repetir","Que"
                         ]

	def __init__(self, programa):
		# Leemos el programa
		try:
			archivo = open(programa, "r")
			lineas = archivo.readlines()
			for linea in lineas:
				self.codigo += linea
			archivo.close() 
		except Exception as e:
			print('Ocurrio el siguiente error: ', e)

	def obtener_token(self):
		if len(self.L) > 0:
			return self.L.pop(0)

		return None

	def tamanio(self):
		return len(self.L)
	
	def __str__(self):
		return self.L[0]

	def regresar_token(self, t):
		self.L.insert(0, t)

	def es_palabra_reservada(self, lexema):
		for p in self.palabras_reservadas:
			#print(p)
			if lexema == p:
				return token.Token(tipo_token.PALABRA_RESERVADA, lexema, lexema, self.num_linea)

		return token.Token(tipo_token.IDENTIFICADOR, subtipos_token.NINGUNO, lexema, self.num_linea)

	def crear_lista(self):
		index = 0
		nombre_iden = ""
		numero = ""
		cadena = ''
		tam = len(self.codigo)
		while index < tam:
			c = self.codigo[index]

			# Quitar espacios en blanco
			while c.isspace() and index < tam:
				if c == '\n':
					self.num_linea += 1
				index += 1
				c = self.codigo[index]

			# Vericamos operadores aritmeticos
			if c == '+' or c == '-' or c == '*' or c == '/' or c == '%':
				if c == '-':
					t = token.Token(tipo_token.OPERADOR_ARTIMETICO, subtipos_token.OPERADOR_RESTA, c, self.num_linea)
				elif c == '+':
					t = token.Token(tipo_token.OPERADOR_ARTIMETICO, subtipos_token.OPERADOR_SUMA, c, self.num_linea)
				elif c == '*':
					t = token.Token(tipo_token.OPERADOR_ARTIMETICO, subtipos_token.OPERADOR_MULTIPLICACION, c, self.num_linea)
				elif c == '/':
					t = token.Token(tipo_token.OPERADOR_ARTIMETICO, subtipos_token.OPERADOR_DIVISION, c, self.num_linea)
				elif c == '%':
					t = token.Token(tipo_token.OPERADOR_ARTIMETICO, subtipos_token.OPERADOR_MODULO, c, self.num_linea)
				
				self.L.append( t )
				index += 1
			# Vericamos operadores relacionales
			elif c == '>' or c == '<':
				if c == '>':
					index += 1
					if index < tam:
						c = self.codigo[index]
						if c == '=':
							index += 1
							t = token.Token(tipo_token.OPERADOR_RELACIONAL, subtipos_token.OPERADOR_MAYOR_IGUAL, '>=', self.num_linea)
			
						else:
							t = token.Token(tipo_token.OPERADOR_RELACIONAL, subtipos_token.OPERADOR_MAYOR, '>', self.num_linea)
						
						self.L.append( t )
					else:
						print('Fin del archivo')
				elif c == '<':
					index += 1
					if index < tam:
						c = self.codigo[index]
						if c == '=':
							index += 1
							t = token.Token(tipo_token.OPERADOR_RELACIONAL, subtipos_token.OPERADOR_MENOR_IGUAL, '<=', self.num_linea)
							
						else:
							t = token.Token(tipo_token.OPERADOR_RELACIONAL, subtipos_token.OPERADOR_MENOR, '<', self.num_linea)
						
						self.L.append( t )
					else:
						print('Fin del archivo')

			# Verificamos operadores logicos
			elif c == '|':
				index += 1
				if index < tam:
					c = self.codigo[index]
					if c == '|':
						index += 1
						t = token.Token(tipo_token.OPERADOR_LOGICO, subtipos_token.OPERADOR_O, '||', self.num_linea)
					else:
						t = token.Token(tipo_token.SIMBOLO, subtipos_token.NINGUNO, '|', self.num_linea)

					self.L.append( t )
			elif c == '&':
				index += 1
				if index < tam:
					c = self.codigo[index]
					if c == '&':
						index += 1
						t = token.Token(tipo_token.OPERADOR_LOGICO, subtipos_token.OPERADOR_Y, '&&', self.num_linea)
					else:
						t = token.Token(tipo_token.SIMBOLO, subtipos_token.NINGUNO, '&', self.num_linea)

					self.L.append( t )
				

			# Verificamos parantesis
			elif c == '(' or c == ')':
				if c == '(':
					t = token.Token(tipo_token.PARENTESIS, subtipos_token.PARETESIS_IZQUIERDO, c, self.num_linea)
				else:
					t = token.Token(tipo_token.PARENTESIS, subtipos_token.PARETESIS_DERECHO, c, self.num_linea)

				self.L.append(t)
				index += 1

			# Verificamos corchetes
			elif c == '[' or c == ']':
				if c == '[':
					t = token.Token(tipo_token.CORCHETES, subtipos_token.CORCHETE_IZQUIERDO, c, self.num_linea)
				else:
					t = token.Token(tipo_token.CORCHETES, subtipos_token.CORCHETE_DERECHO, c, self.num_linea)

				self.L.append(t)
				index += 1

			# Verificamos Identificadores
			elif c.isalpha() or c == '_':
				nombre_iden = c
				index += 1
				f = True
				while index < tam and f:
					c = self.codigo[index]
					if c.isalpha() or c == "_" or c.isdigit():
						nombre_iden += c
						index += 1
					else:
						f = False
				# print(nombre_iden)
				t = self.es_palabra_reservada(nombre_iden)
				self.L.append( t )
				nombre_iden = ''

			# Numeros
			elif c.isdigit():
				index += 1
				numero += c
				f = True
				t = None
				while index < tam and f:
					c = self.codigo[index]
					if c.isdigit():
						index += 1
						numero += c
					elif c == '.':
						index += 1
						numero += c
						c = self.codigo[index]
						if c.isdigit():
							while c.isdigit():
								index += 1
								numero += c
								c = self.codigo[index]
							t = token.Token(tipo_token.NUMERO, subtipos_token.REAL, numero, self.num_linea)
						else:
							t = token.Token(tipo_token.SIMBOLO, subtipos_token.NINGUNO, numero, self.num_linea)

					else:
						f = False
						if t == None:
							t = token.Token(tipo_token.NUMERO, subtipos_token.ENTERO, numero, self.num_linea)

				self.L.append( t )
				numero = '' # Reestablecemos los valores

			#Cadenas

			elif c == '"':
				cadena += c
				index += 1
				c = self.codigo[index]
				while index < tam:
					cadena += c
					index += 1
					if c == '"':
						t = token.Token(tipo_token.CADENA, subtipos_token.NINGUNO, cadena, self.num_linea)
						break

					c = self.codigo[index]

				self.L.append(t)
				cadena = '' # Reestablecemos su valor

			elif c == "'":
				cadena += c
				index += 1
				c = self.codigo[index]
				cadena += c
				index += 1
				c = self.codigo[index]
				if c == "'":
					cadena += c
					index += 1
					t = token.Token(tipo_token.CHAR, subtipos_token.CARACTER, cadena, self.num_linea)
				else:
					cadena += c
					index += 1
					t = token.Token(tipo_token.SIMBOLO, subtipos_token.NINGUNO, cadena, self.num_linea)

				self.L.append(t)
				cadena = ''


			# Verificamos Asignacion o Igualdad
			elif c == '=':
				index += 1
				if index < tam:
					c = self.codigo[index]
					if c == '=':
						index += 1
						t = token.Token(tipo_token.COMPARACION, subtipos_token.IGUALDAD, '==', self.num_linea)
					else:
						t = token.Token(tipo_token.ASIGNACION, subtipos_token.NINGUNO, '=', self.num_linea)

					self.L.append( t )

			# Verificar Operadores de Comparacion
			elif c == '!':
				index += 1
				if index < tam:
					c = self.codigo[index]
					if c == '=':
						index += 1
						t = token.Token(tipo_token.COMPARACION, subtipos_token.DIFERENTE, '!=', self.num_linea)
					else:
						t = token.Token(tipo_token.COMPARACION, subtipos_token.NEGACION, '!', self.num_linea)

					self.L.append( t )
			# Verificamos Signos de puntuacion
			elif c == ',' or c == ';' or c == ':':
				if c == ',':
					t = token.Token(tipo_token.SIGNO_DE_PUNTUACION, subtipos_token.COMA, c, self.num_linea)
				elif c == ';':
					t = token.Token(tipo_token.SIGNO_DE_PUNTUACION, subtipos_token.PUNTOYCOMA, c, self.num_linea)
				elif c == ':':
					t = token.Token(tipo_token.SIGNO_DE_PUNTUACION, subtipos_token.DOSPUNTOS, c, self.num_linea)

				self.L.append( t )
				index += 1

			else:
				print('Simbolo extranio', c)
				index += 1

		# for t in self.L:
		# 	print(t)
		# print('Tamanio de elementos: ', tam)
		#print(self.L)





