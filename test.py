from analizador_lexico import AnalizadorLexico

if __name__ == '__main__':
	l = AnalizadorLexico('programa1.txt')
	l.crear_lista()
	t = l.obtener_token()
	while t != None:
		print('Token: ', t)
		t = l.obtener_token()
