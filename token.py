"""
	clase Token
"""

class Token:
	num_linea = 0 # atributo de clase

	def __init__(self, tipo_token, subtipo_token, lexema, num_linea):
		self.tipo_token = tipo_token
		self.subtipo_token = subtipo_token
		self.lexema = lexema
		self.num_linea = num_linea

	def __str__(self):
		return f'[ {self.tipo_token} --- {self.subtipo_token} --- {self.lexema} --- {self.num_linea} ]'


	def get_tipo_token(self):
		return self.tipo_token

	def get_subtipo_token(self):
		return self.subtipo_token

	def get_lexema(self):
		return self.lexema

	def get_num_linea(self):
		return self.num_linea

	def set_num_linea(self, num_linea):
		self.num_linea = num_linea
