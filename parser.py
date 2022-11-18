import subtipos_token
import analizador_lexico
import tipo_token

class Verificador:
    def __init__(self):
        self.nom_programa = ''
        self.codigo = '#include <stdio.h>\n'
        self.band = False
        self.ident = 0
        self.e = '  '
        self.identificadores = {}
        self.lista_aux = []
    
    def obtener_codigo(self):
        if not self.band:
            self.crear_archivo()
            return self.codigo
        
        # return 'Hay errores :('
    def crear_archivo(self):
        try:
            nombre_archivo = self.nom_programa + '.c'
            archivo = open(nombre_archivo, 'w')
            archivo.write(self.codigo)
            archivo.close()
        except:
            print('Ocurrio un error al crear el archivo :(')

v = Verificador()
# Creamos nuestro analizador lexico
l = analizador_lexico.AnalizadorLexico('suma.txt')
# Creamos la lista de tokens
l.crear_lista()

# Definimos la funcion error
def error(t1, t2, line):
    v.band = True
    print(f'Se esperaba {t1} en la linea {line} y se escribio {t2}')

# Definimos la funcion se_espera 
# Verifica que el tipo de token o subtipo token t que se analiza sea igual
# al preanalisis que es lo que se espera reconocer de acuerdo con la produccion
def se_espera(t, preanalisis):
    return t != None and t == preanalisis

# Se realiza las funciones para el parser

# <programa> ::= <proceso> <listaFunciones> | <proceso>
def programa():
    proceso()
    t = l.obtener_token()
    if t != None:
        l.regresar_token(t)
        lista_funciones()

# <proceso> ::= PROCESO <ID> <listaOperaciones> FINPROCESO
def proceso():
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PROCESO):
            error(subtipos_token.PROCESO, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PROCESO ')
            v.codigo += 'int main() {\n'
            # print(t)
    # <ID>
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            print('Se reconoce IDENTIFICADOR: ', t.get_lexema())
            v.nom_programa = t.lexema
            # print(t)
    v.ident += 1
    lista_operaciones()

    t = l.obtener_token()
    # FinProceso
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.FINPROCESO):
            error(subtipos_token.FINPROCESO, t.subtipo_token, t.num_linea)
        else:
            v.codigo += v.ident * v.e + 'return 0;\n'
            v.codigo += '}\n'
            v.ident -= 1
            v.identificadores.clear()
            print('Se reconoce FINPROCESO')

# <listaOperaciones> ::= <operacion> <listaOperaciones> | <operacion>
def lista_operaciones():
    operacion()
    t = l.obtener_token()
    # print('Lista de operaciones')
    # print(t)
    if (t != None and t.get_subtipo_token() != subtipos_token.FINPROCESO 
        and t.get_subtipo_token() != subtipos_token.FINSI 
        and t.get_subtipo_token() != subtipos_token.FINMIENTRAS 
        and t.get_subtipo_token() != subtipos_token.REGRESAR
        and t.get_subtipo_token() != subtipos_token.FINPARA
        and t.get_subtipo_token() != subtipos_token.FINSEGUN
        and t.get_subtipo_token() != subtipos_token.ROMPER
        and t.get_subtipo_token() != subtipos_token.FINFUNCION
        and t.get_subtipo_token() != subtipos_token.PUNTOYCOMA
        and not t.subtipo_token == subtipos_token.SINO ):
        # print('if 1')
        l.regresar_token(t)
        lista_operaciones()
    elif t != None and t.get_subtipo_token() == subtipos_token.FINPROCESO:
        l.regresar_token(t)
        # print('Fin Proceso')
        # print(t)
    elif t != None and t.get_subtipo_token() == subtipos_token.FINSI:
        # print('Fin Si')
        # print(t)
        l.regresar_token(t)
    elif t != None and t.subtipo_token == subtipos_token.SINO:
        l.regresar_token(t)
    elif t != None and t.get_subtipo_token() == subtipos_token.FINMIENTRAS:
        l.regresar_token(t)
    elif t != None and t.get_subtipo_token() == subtipos_token.REGRESAR:
        l.regresar_token(t)
    elif t != None and t.get_subtipo_token() == subtipos_token.FINPARA:
        l.regresar_token(t)
    elif t != None and t.get_subtipo_token() == subtipos_token.FINSEGUN:
        l.regresar_token(t)
    elif t != None and t.get_subtipo_token() == subtipos_token.ROMPER:
        l.regresar_token(t)
    elif t != None and t.get_subtipo_token() == subtipos_token.FINFUNCION:
        l.regresar_token(t)
    elif t != None and t.get_subtipo_token() == subtipos_token.PUNTOYCOMA:
        l.regresar_token(t)
    
# <operacion> ::= <declaracion> |<leer> |<escribir>| <asignacion>| <si> ..
def operacion():
    t = l.obtener_token()
    # print('Operacion')
    # print(t)
    if t != None:
        # print('Entro a primer if')
        if t.subtipo_token == subtipos_token.SI:
            l.regresar_token(t)
            si()
        elif t.subtipo_token == subtipos_token.SINO:
            l.regresar_token(t)
        elif t.subtipo_token == subtipos_token.FUNCION:
            l.regresar_token(t)
            funcion()
        elif t.subtipo_token == subtipos_token.LEER:
            l.regresar_token(t)
            leer()
        elif t.subtipo_token == subtipos_token.ESCRIBIR:
            l.regresar_token(t)
            escribir()
        elif t.subtipo_token == subtipos_token.MIENTRAS:
            l.regresar_token(t)
            mientras()
        elif t.subtipo_token == subtipos_token.PARA:
            l.regresar_token(t)
            para()
        elif t.tipo_token == tipo_token.IDENTIFICADOR:
            aux_t = t
            t = l.obtener_token()
            # invocacion
            if t.subtipo_token == subtipos_token.PARETESIS_IZQUIERDO:
                l.regresar_token(t) # Regresamos PAR_IZQ
                l.regresar_token(aux_t) # Regresamos Identificador
                invocacion()
            elif t.tipo_token == tipo_token.ASIGNACION:
                # Se regresa la asignacion
                l.regresar_token(t)
                # Se regresa identificador
                l.regresar_token(aux_t)
                asignacion()
        elif t.subtipo_token == subtipos_token.ENTERO:
            l.regresar_token(t)
            declaracion_entero()
        elif t.subtipo_token == subtipos_token.REAL:
            l.regresar_token(t)
            declaracion_real()
        elif t.subtipo_token == subtipos_token.LOGICO:
            l.regresar_token(t)
            declaracion_logico()
        elif t.subtipo_token == subtipos_token.CARACTER:
            l.regresar_token(t)
            declaracion_caracter()
        """ else:
            print('Entro en else')
            l.regresar_token(t) """


# <listaFunciones> ::= <funcion> | <funcion> <listaFunciones>
def lista_funciones():
    funcion()
    t = l.obtener_token()
    if t != None:
        l.regresar_token(t)
        lista_funciones()

def es_tipo(t):
    if (t.subtipo_token == subtipos_token.ENTERO or 
        t.subtipo_token == subtipos_token.LOGICO):
        return v.ident * v.e + 'int'
    elif t.subtipo_token == subtipos_token.REAL:
        return v.ident * v.e + 'float'
    elif t.tipo_token == tipo_token.CHAR:
        return v.ident * v.e + 'int'

def tipo():
    t = l.obtener_token()
    if t != None:
        if (not se_espera(t.subtipo_token, subtipos_token.ENTERO) and 
            not se_espera(t.subtipo_token, subtipos_token.REAL) and
            not se_espera(t.subtipo_token, subtipos_token.LOGICO) and
            not se_espera(t.subtipo_token, subtipos_token.CARACTER)):
            print('Error: Tipo de dato incorrecto en la linea: ', t.num_linea)
        else:
            print('Se reconoce Tipo: ', t.subtipo_token)
            v.lista_aux.append( 'funcion' )
            v.lista_aux.append( es_tipo(t) )
            v.codigo += es_tipo(t) + ' '

# <funcion> ::= <tipo> FUNCION <ID> (<parametros>) <listaOperaciones> REGRESAR <expresion> PCOMA FINFUNCION
def funcion():
    tipo()
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.FUNCION):
            error(subtipos_token.FUNCION, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce FUNCION')
            # print(t)
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.tipo_token, t.get_num_linea())
        else:
            print('Se reconoce IDENTIFICADOR: ', t.get_lexema())
            v.codigo += v.ident * v.e
            # v.codigo += v.lista_aux[0] + ' '
            v.codigo += t.lexema
            # print(t)
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PARETESIS_IZQUIERDO):
            error(subtipos_token.PARETESIS_IZQUIERDO, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce (')
            v.codigo += t.lexema 
            # print(t)

    # <parametros>
    parametros()

    # )
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PARETESIS_DERECHO):
            error(subtipos_token.PARETESIS_DERECHO, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce )')
            v.codigo += t.lexema + ' {\n'
            # print(t)
    v.ident += 1
    # <listaOperaciones>
    lista_operaciones()

    # REGRESAr
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.REGRESAR):
            error(subtipos_token.REGRESAR, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce REGRESAR')
            v.codigo += v.ident * v.e
            v.codigo += 'return '
            # print(t)

    # Expresion
    expresion()

    #PUNTOCOMA
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PUNTOYCOMA')
            v.codigo += t.lexema + '\n'

    # FINFUNCION
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.FINFUNCION):
            error(subtipos_token.FINFUNCION, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce FINFUNCION')
            v.ident -= 1
            v.codigo += '}\n'
            v.lista_aux.clear() # Limpiamos la lista auxiliar
            # print(t)


# <parametros> ::= <hayParametros> | @
def parametros():
    t = l.obtener_token()
    if t != None:
        if se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            l.regresar_token(t)
            hay_parametros()
        else:
            # No hay parametros
            l.regresar_token(t)

# La funcion hay_parametros implementa las dos reglas de produccion
# <hayParametros> ::= <unParametro> | <masParametros>
# <unParametro> ::= ID
def hay_parametros():
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            # Si hay un parametro
            # <unParametro> ::= ID
            print('Se reconoce IDENTIFICADOR: ', t.get_lexema())
            if 'funcion' in v.lista_aux:
                v.codigo += v.lista_aux[1] + ' '
            v.codigo += t.lexema
            # print(t)

    t = l.obtener_token()
    if t != None:
        # <hayParametro> ::= <unParametro> | <masParametros>
        # <masParametro>
        if t.get_subtipo_token() == subtipos_token.COMA:
            # print(t)
            print('Se reconoce Coma: ,')
            v.codigo += ', '
            hay_parametros()
        else:
            # <unParametro>
            l.regresar_token(t)

# <declaracionEntero> ::= ENTERO <listadE> PCOMA
def declaracion_entero():
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.ENTERO):
            error(subtipos_token.ENTERO, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce la palabra Entero')
            v.codigo += v.ident * v.e
            v.codigo += 'int '
            # print(t)
    lista_entero()
    # PCOMA
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PUNTOYCOMA ;')
            v.codigo += ';\n'
            # print(t) 

# <listaE> ::= <de> | <de> COMA <listaE>
def lista_entero():
    de()
    # COMA
    t = l.obtener_token()
    if t != None:
        if t.get_subtipo_token() == subtipos_token.COMA:
            print('Se reconoce COMA ,')
            v.codigo += ', '
            # print(t)
            lista_entero()
        else:
            l.regresar_token(t)
    else:
        print('Error en la declaracion')

# <de> ::= <ID> | <ID> = Int
def de():
    # <ID>
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            print('Se reconoce IDENTIFICADOR: ', t.lexema)
            # Agregamos identificador
            v.identificadores[t.lexema] = "%d"
            v.codigo += t.lexema
            # print(t)
    # <ID> = Int
    t = l.obtener_token()
    if t != None:
        if t.get_tipo_token() == tipo_token.ASIGNACION:
            print('Se reconocio ASIGNACION =')
            v.codigo += ' = '
            # print(t)
            t = l.obtener_token()
            # # print(t)
            if t != None:
                # print(se_espera(t.subtipo_token, subtipos_token.NUMERO_ENTERO))
                if not se_espera(t.get_subtipo_token(), subtipos_token.NUMERO_ENTERO):
                    error(subtipos_token.NUMERO_ENTERO, t.get_subtipo_token(), t.get_num_linea())
                else:
                    print('Se reconoce el Int: ', t.get_lexema())
                    v.codigo += t.lexema
                    # print(t)
            else:
                print('Error: se esperaba un entero')
        else:
            l.regresar_token(t)

# <declaracionReal> ::= REAL <listadR> PCOMA
def declaracion_real():
    # Real
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.REAL):
            error(subtipos_token.REAL, t.subtipo_token, t.num_linea)
        else:
            print('Se conoce la palabra Real')
            v.codigo += v.ident * v.e
            v.codigo += 'float '
            # print(t)
    lista_real()
    # PCOMA
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PUNTOYCOMA ;')
            v.codigo += ';\n'
            # print(t)

# <listadR> ::= <dr> | <dr> COMA <listadR>
def lista_real():
    dr()
    # COMA
    t = l.obtener_token()
    if t != None:
        if t.get_subtipo_token() == subtipos_token.COMA:
            print('Se reconoce COMA ,')
            v.codigo += ', '
            # print(t)
            lista_real()
        else:
            l.regresar_token(t)
    else:
        print('Error en la declaracion')

# <dr> ::= <ID> | <ID> = Float
def dr():
    # <ID>
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            print('Se reconoce IDENTIFICADOR: ', t.lexema)
            v.identificadores[t.lexema] = '%f'
            v.codigo += t.lexema
            # print(t)
    # <ID> = Float
    t = l.obtener_token()
    if t != None:
        if t.get_tipo_token() == tipo_token.ASIGNACION:
            print('Se reconocio ASIGNACION =')
            v.codigo += ' = '
            # print(t)
            t = l.obtener_token()
            if t != None:
                if not se_espera(t.get_subtipo_token(), subtipos_token.NUMERO_REAL):
                    error(subtipos_token.NUMERO_REAL, t.get_subtipo_token(), t.get_num_linea())
                else:
                    print('Se reconoce el Float: ', t.get_lexema())
                    v.codigo += t.lexema
                    # print(t)
            else:
                print('Error: se esperaba un real')
        else:
            l.regresar_token(t)

# <declaracionLogico> ::= LOGICO <listadL> PCOMA
def declaracion_logico():
    # Logico
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.LOGICO):
            error(subtipos_token.LOGICO, t.subtipo_token, t.num_linea)
        else:
            print('Se conoce la palabra Logico')
            v.codigo += v.ident * v.e
            v.codigo += 'int '
            # print(t)
    lista_logico()
    # PUNTO y Coma
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PUNTOYCOMA ; ')
            v.codigo += ';\n'
            # print(t)

# <listadL> ::= <dr> | <dr> COMA <listadL>
def lista_logico():
    dl()
    t = l.obtener_token()
    if t != None:
        if t.get_subtipo_token() == subtipos_token.COMA:
            print('Se reconoce COMA ,')
            v.codigo += ', '
            lista_logico()
        else:
            l.regresar_token(t)
    else:
        print('Error en la declaracion')
# <dl> ::= <ID> | <ID> = Boolean
def dl():
    # <ID>
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            print('Se reconoce IDENTIFICADOR: ', t.lexema)
            v.identificadores[t.lexema] = '%d'
            v.codigo += t.lexema
            # print(t)
    # <ID> = Boolean
    t = l.obtener_token()
    if t != None:
        if t.get_tipo_token() == tipo_token.ASIGNACION:
            print('Se reconocio ASIGNACION =')
            v.codigo += ' = '
            # print(t)
            t = l.obtener_token()
            if t != None:
                if not se_espera(t.get_subtipo_token(), subtipos_token.VERDADERO) and not se_espera(t.get_subtipo_token(), subtipos_token.FALSO):
                    error(subtipos_token.LOGICO, t.get_subtipo_token(), t.get_num_linea())
                else:
                    print('Se reconoce BOOLEANO: ', t.get_lexema())
                    if t.subtipo_token == subtipos_token.VERDADERO: 
                        v.codigo += '1'
                    else:
                        v.codigo += '0'
                    # print(t)
            else:
                print('Error: se esperaba un Logico')
        else:
            l.regresar_token(t)

# <declaracionChar> ::= CARACTER <listadC> PCOMA
def declaracion_caracter():
    # Real
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.CARACTER):
            error(subtipos_token.CARACTER, t.subtipo_token, t.num_linea)
        else:
            print('Se conoce la palabra Caracter')
            v.codigo += v.ident * v.e
            v.codigo += 'char '
            # print(t)
    lista_caracter()
    # punto y coma
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PUNTOYCOMA ;')
            v.codigo += ';\n'
            # print(t)

def lista_caracter():
    dc()
    t = l.obtener_token()
    if t != None:
        if t.get_subtipo_token() == subtipos_token.COMA:
            print('Se reconoce COMA ,')
            v.codigo += ', '
            # print(t)
            lista_caracter()
        else:
            l.regresar_token(t)
    else:
        print('Error en la declaracion')

def dc():
    # <ID>
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            print('Se reconoce IDENTIFICADOR: ', t.get_lexema())
            v.identificadores[t.lexema] = '%c'
            v.codigo += t.lexema
            # print(t)
    # <ID> = Char
    t = l.obtener_token()
    if t != None:
        if t.get_tipo_token() == tipo_token.ASIGNACION:
            print('Se reconocio ASIGNACION =')
            v.codigo += ' = '
            # print(t)
            t = l.obtener_token()
            if t != None:
                if not se_espera(t.get_tipo_token(), tipo_token.CHAR):
                    error(tipo_token.CHAR, t.get_tipo_token(), t.get_num_linea())
                else:
                    print('Se reconoce el Char: ', t.get_lexema())
                    v.codigo += t.lexema
                    # print(t)
            else:
                print('Error: se esperaba un char')
        else:
            l.regresar_token(t)

# <invocacion> ::= <ID> (<parametros)
def invocacion():
    # <ID>
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            v.codigo += v.ident * v.e
            v.codigo += t.lexema
            print('Se reconoce IDENTIFICADOR: ', t.get_lexema())
            # print(t)
    # (
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PARETESIS_IZQUIERDO):
            error(subtipos_token.PARETESIS_IZQUIERDO, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PARENTESIS_IZQUIERDO: (')
            v.codigo += '('
            # print(t)
    # <parametros>
    parametros()

    # )
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PARETESIS_DERECHO):
            error(subtipos_token.PARETESIS_DERECHO, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PARENTESIS_DERECHO: )')
            v.codigo += ')'
            # print(t)

# <asignacion> ::= <ID> = <expresion> PCOMA
def asignacion():
    # <ID>
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            print('Se reconoce IDENTIFICADOR: ', t.get_lexema())
            v.codigo += v.ident * v.e
            v.codigo += t.lexema
            # print(t)
    # IGUAL
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.ASIGNACION):
            error(tipo_token.ASIGNACION, t.get_tipo_token(), t.get_num_linea())
        else:
            print('Se reconoce Asignacion: ', t.get_lexema())
            v.codigo += ' = '
            # print(t)
    # Invocacion o Expresion
    t = l.obtener_token()
    if t != None:
        # Vericamos Invocacion
        if t.tipo_token == tipo_token.IDENTIFICADOR:
            aux_t = t
            t = l.obtener_token()
            if t != None:
                if t.subtipo_token == subtipos_token.PARETESIS_IZQUIERDO:
                    # Regresamos los tokens
                    # print('Se reconoce Invocacion')
                    l.regresar_token( t ) # Regresamos el (
                    l.regresar_token( aux_t ) # Regresamos el ID
                    invocacion()
                else:
                    l.regresar_token( t )
                    l.regresar_token( aux_t )
                    expresion()
        else:
            l.regresar_token( t ) # Regresamos el token
            expresion()
    # expresion
    # expresion()
    
    # PUNTO y Coma 
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PUNTOYCOMA: ;')
            v.codigo += ';\n'
            # print(t)

# <leer>::= LEER <listaLeer> PCOMA
def leer():
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.LEER):
            error(subtipos_token.LEER, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce LEER: ')
            v.codigo += v.ident * v.e
            v.codigo += 'scanf("'
            # print(t)
    lista_leer()
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PUNTOYCOMA ; ')
            v.codigo += '", '
            for i in range(len(v.lista_aux)):
                v.codigo += '&' + v.lista_aux[i]
                if i+1 != len(v.lista_aux):
                    v.codigo += ','
                else:
                    v.codigo += ')'
            v.lista_aux.clear()
            v.codigo += ';\n'
            # print(t)



# <listaLeer> ::= ID | ID COMA <listaLeer>
def lista_leer():
    # <ID>
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_tipo_token(), tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.get_tipo_token(), t.get_num_linea())
        else:
            print('Se reconoce IDENTIFICADOR: ', t.lexema)
            try:
                v.codigo += v.identificadores[t.lexema]
                # v.codigo += t.lexema
                v.lista_aux.append(t.lexema)
            except:
                print(f'Error en la linea {t.num_linea}, la variable: {t.lexema} no fue declarada')
                v.band = True
            # print(t)
    
    t = l.obtener_token()
    if t != None:
        if t.get_subtipo_token() == subtipos_token.COMA:
            print('Se reconoce COMA ,')
            v.codigo += ', '
            # print(t)
            lista_leer()
        else:
            l.regresar_token(t)

# <escribir> ::= ESCRIBIR <listaValor> PCOMA
def escribir():
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.ESCRIBIR):
            error(subtipos_token.ESCRIBIR, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce ESCRIBIR: ')
            # v.codigo += v.ident * v.e 
            # v.codigo += 'printf('
            # print(t)
    lista_valor()
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.get_subtipo_token(), subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.get_subtipo_token(), t.get_num_linea())
        else:
            print('Se reconoce PUNTOYCOMA ; ')
            # v.codigo += ');\n'
            # print(t)

# <Valor> ::= <valor> | <valor> COMA <listaValor>
def lista_valor():
    valor()
    t = l.obtener_token()
    if t != None:
        if t.get_subtipo_token() == subtipos_token.COMA:
            print('Se reconoce COMA: ,')
            v.codigo += ' '
            # print(t)
            lista_valor()
        else:
            l.regresar_token(t)

# <valor> ::= <expresion> | String 
def valor():
    # String o Cadenas
    t = l.obtener_token()
    if t != None:
        if t.tipo_token == tipo_token.CADENA:
            print('Se reconocio una String: ', t.lexema)
            v.codigo += v.ident * v.e 
            v.codigo += 'printf('
            v.codigo += t.lexema + ');\n'
            # print(t)
        else:
            l.regresar_token(t)
            # Es una expresion
            # Puede ser Identificador o Int o Float o Bool o Char
            v.codigo += v.ident * v.e 
            v.codigo += 'printf("'
            v.lista_aux.append( 'escribir' )
            expresion()
            v.codigo += ');\n'
            v.lista_aux.clear()

# <Si> ::= SI (<expresion>) ENTONCES <listaOperaciones> FINSI
#         |SI (<expresion>) ENTONCES <listaOperaciones> SINO <listaOperaciones> FINSI
def si():
    # SI
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.SI):
            error(subtipos_token.SI, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce SI')
            v.codigo += v.ident * v.e
            v.codigo += 'if '
            # print(t)
    # (
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.PARETESIS_IZQUIERDO):
            error(subtipos_token.PARETESIS_IZQUIERDO, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce PARENTESIS IZQ: (')
            v.codigo += '('
            # print(t)
    # <expresiones>
    expresion()

    # )
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.PARETESIS_DERECHO):
            error(subtipos_token.PARETESIS_DERECHO, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce PARENTESIS DER: )')
            v.codigo += ')'
            # print(t)
    
    # Entonces
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.ENTONCES):
            error(subtipos_token.ENTONCES, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce ENTONCES: ')
            v.codigo += ' {\n'
            v.ident += 1
            # print(t)
    
    # <listaOperaciones>	
    lista_operaciones()

    # SINO
    t = l.obtener_token()
    # print('Sino')
    # print(t)
    if t != None:
        if t.subtipo_token == subtipos_token.SINO:
            print('Se reconoce Sino')
            v.ident -= 1
            v.codigo += v.ident * v.e
            v.codigo += '} '
            # v.codigo += v.ident * v.e
            v.codigo += 'else {\n'
            v.ident += 1
            # print(t)
            lista_operaciones()
            
            t = l.obtener_token()
            if t != None:
                if t.subtipo_token == subtipos_token.FINSI:
                    print('Se reconoce FinSI')
                    v.ident -= 1
                    v.codigo += v.ident * v.e
                    v.codigo += '}\n'
                    # print(t)
        # FinSi
        elif t.subtipo_token == subtipos_token.FINSI:
            print('Se reconoce FinSi')
            v.ident -= 1
            v.codigo += v.ident * v.e
            v.codigo += '}\n'
            # v.ident -= 1
            # print(t)
    

# <mientras> ::= MIENTRAS (<expresion>) HACER <listaOperaciones> FINMIENTRAs
def mientras():
    # MIENTRAs
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.MIENTRAS):
            error(subtipos_token.MIENTRAS, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce MIENTRAS')
            v.codigo += v.ident * v.e
            v.codigo += 'while '
            # print(t)
    # (
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.PARETESIS_IZQUIERDO):
            error(subtipos_token.PARETESIS_IZQUIERDO, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce PARENTESIS IZQ: (')
            v.codigo += '('
            # print(t)
    # <expresiones>
    expresion()

    # )
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.PARETESIS_DERECHO):
            error(subtipos_token.PARETESIS_DERECHO, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce PARENTESIS DER: )')
            v.codigo += ')'
            # print(t)
    
    # HACER
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.HACER):
            error(subtipos_token.HACER, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce HACER: ')
            v.codigo += ' {\n'
            v.ident += 1
            # print(t)
    
    # <listaOperaciones>
    lista_operaciones()

    # FINMIENTRAS
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.FINMIENTRAS):
            error(subtipos_token.FINMIENTRAS, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce FINMIENTRAS:')
            v.ident -= 1
            v.codigo += v.ident * v.e
            v.codigo += '}\n'
            # v.ident -= 1
            # print(t)

# <para>::= PARA <ID> = <op> HASTA <op> HACER <listaOperacoones> FINPARA
#      | PARA <ID> = <op> CON PASO <op> HACER <listaOperaciones> FINPARA
def para():
    # PARA
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.PARA):
            error(subtipos_token.PARA, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce PARA')
            v.codigo += v.ident * v.e
            v.codigo += 'for ('
            # print(t)
    # ID
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.tipo_token, tipo_token.IDENTIFICADOR):
            error(tipo_token.IDENTIFICADOR, t.tipo_token, t.num_linea)
        else:
            print('Se reconoce IDENTIFICADOR: ', t.lexema)
            v.lista_aux.append(t.lexema)
            v.codigo += t.lexema + ' '
            # print(t)
    
    # Asignacion
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.tipo_token, tipo_token.ASIGNACION):
            error(tipo_token.ASIGNACION, t.tipo_token, t.num_linea)
        else:
            print('Se reconoce ASIGNACION: ', t.lexema)
            v.codigo += '= '
            # print(t)
    # <op>
    op()

    # HASTA
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.HASTA):
            error(subtipos_token.HASTA, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce HASTA')
            lexema = v.lista_aux[0]
            v.codigo += '; ' + lexema +' < '
            # print(t)
    
    # CON PASO
    t = l.obtener_token()
    if t != None:
        if t.subtipo_token == subtipos_token.CON:
            print('Se reconocio CON')
            # <op>
            op()
            v.codigo += '; ' + v.lista_aux[0] + ' = ' + v.lista_aux[0]
            # print(t)
            t = l.obtener_token()
            if t != None:
                if not se_espera(t.subtipo_token, subtipos_token.PASO):
                    error(subtipos_token.PASO, t.subtipo_token, t.num_linea)
                else:
                    print('Se reconocio PASO')
                    # print(t)
                    v.codigo += ' + '
                    op()
        else:
            l.regresar_token(t)
            op()
            v.codigo += '; ' + v.lista_aux[0] + '++'
    
    # HACER
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.HACER):
            error(subtipos_token.HACER, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce HACER')
            v.codigo += ') {\n'
            v.ident += 1
            v.lista_aux.clear()
            # print(t)
    
    # <listaOperaciones>
    lista_operaciones()

    # FINPARA
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.FINPARA):
            error(subtipos_token.FINPARA, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce FINPARA')
            v.ident -= 1
            v.codigo += v.ident * v.e
            v.codigo += '}\n'
            # v.ident -= 1
            # print(t)

# <op> ::= Int | <ID>
def op():
    # Int | ID
    t = l.obtener_token()
    if t != None:
        if t.tipo_token == tipo_token.IDENTIFICADOR:
            print('Se reconoce IDENTIFICADOR: ', t.lexema)
            v.codigo += t.lexema
            # print(t)
        else:
            if not se_espera(t.subtipo_token, subtipos_token.ENTERO):
                error(subtipos_token.ENTERO, t.subtipo_token, t.num_linea)
            else:
                print('Se reconoce INT: ', t.lexema)
                v.codigo += t.lexema
                # print(t)

# <segun> ::= SEGUN ( <op> ) HACER <listaCasos> OMISION DOSPUNTOS <listaOperaciones> ROMPER
def segun():
    # SEGUN
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.SEGUN):
            error(subtipos_token.SEGUN, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce SEGUN')
            v.codigo += v.ident * v.e
            v.codigo += 'switch '
    # (
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.PARETESIS_IZQUIERDO):
            error(subtipos_token.PARETESIS_IZQUIERDO, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce PARETESIS_IZQ')
            v.codigo += '('
    # <op>
    op()

    # )
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.PARETESIS_DERECHO):
            error(subtipos_token.PARETESIS_DERECHO, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce PARENTESIS_DER')
            v.codigo += ')'
    # HACER
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.HACER):
            error(subtipos_token.HACER, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce HACER')
            v.codigo += '{\n'
            v.ident += 1
    # <listaCasos>
    lista_casos()

    # OMISION
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.OMISION):
            error(subtipos_token.OMISION, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce OMISION')
    
    # DOSPUNTOS
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.DOSPUNTOS):
            error(subtipos_token.DOSPUNTOS, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce DOSPUNTOS')
    
    # <listaOperaciones>
    lista_operaciones()

    # ROMPER
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.ROMPER):
            error(subtipos_token.ROMPER, t.subtipo_token, t.num_linea)
        else:
            v.codigo += v.ident * v.e
            v.codigo += 'break'
            print('Se reconoce ROMPER')
    
    # PCOMA
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.PUNTOYCOMA):
            error(subtipos_token.PUNTOYCOMA, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce PUNTO Y COMA')
            v.codigo += ';\n'
    
    # FINSEGUN
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.FINSEGUN):
            error(subtipos_token.FINSEGUN, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce FINSEGUN')
            v.ident -= 1
            v.codigo += v.ident * v.e
            v.codigo += '}\n'

# <listaCasos> ::= <listaEnteros> DOSPUNTOS <listaOperaciones> ROMPER PCOMA
# | <listaCasos> <listaEnteros> DOSPUNTOS <listaOperaciones> ROMPER PCOMA
def lista_casos():
    # Verificar si es una lista de Enteros o lista de casos
    t = l.obtener_token()
    if t != None:
        if t.subtipo_token == subtipos_token.ENTERO:
            l.regresar_token(t)
            lista_enteros()
            t = l.obtener_token()
            # DOSPuntos
            if t != None:
                if not se_espera(t.subtipo_token, subtipos_token.DOSPUNTOS):
                    error(subtipos_token.DOSPUNTOS, t.subtipo_token, t.num_linea)
                else:
                    print('Se reconocen DOS PUNTOS :')
            # listaOperaciones
            lista_operaciones()
            # Romper
            t = l.obtener_token()
            if t != None:
                if not se_espera(t.subtipo_token, subtipos_token.ROMPER):
                    error(subtipos_token.ROMPER, t.subtipo_token, t.num_linea)
                else:
                    print('Se reconoce Romper')
                    v.codigo += v.ident * v.e
                    v.codigo += 'break'
            # Punto y coma
            t = l.obtener_token()
            if t != None:
                if not se_espera(t.subtipo_token, subtipos_token.PUNTOYCOMA):
                    error(subtipos_token.PUNTOYCOMA, t.subtipo_token, t.num_linea)
                else:
                    print('Se reconoce PUNTO Y COMA: ;')
                    v.codigo += ';\n'
                    v.ident -= 1
        
        elif t.subtipo_token != subtipos_token.OMISION:
            lista_casos()
        elif t.subtipo_token == subtipos_token.OMISION:
            l.regresar_token(t)
        

# <listaEnteros> ::= Entero | Entero PCOMA <listaEnteros>
def lista_enteros():
    t = l.obtener_token()
    if t != None:
        if not se_espera(t.subtipo_token, subtipos_token.ENTERO):
            error(subtipos_token.ENTERO, t.subtipo_token, t.num_linea)
        else:
            print('Se reconoce ENTERO: ', t.lexema)
            t = l.obtener_token()
            if t != None:
                if t.subtipo_token == subtipos_token.PUNTOYCOMA:
                    print('Se reconoce PUNTO Y COMA: ;')
                    lista_enteros()
                else:
                    l.regresar_token(t)

    
            

# <expresion> ::= <expresion> || <Y> | <Y>
def expresion():
    # <Y>
    Y()
    # <<expresion> || <Y>
    expresion_p()

def expresion_p():
    t = l.obtener_token()
    if t != None:
        if se_espera(t.subtipo_token, subtipos_token.OPERADOR_O):
            print('Se reconocio: ', t.lexema)
            v.codigo += ' || '
            # print(t)
            Y()
            expresion_p()
        else:
            l.regresar_token(t)

# <Y> ::= <Y> && <C> | <C>
def Y():
    C()
    YP()

def YP():
    t = l.obtener_token()
    if t != None:
        if se_espera(t.subtipo_token, subtipos_token.OPERADOR_Y):
            print('Se reconocio: ', t.lexema)
            v.codigo += t.lexema + ' '
            # print(t)
            C()
            CP()
        else:
            l.regresar_token(t)

# <C> ::= <C> == <R> | <C> != <R> | <R>
def C():
    # <R>
    R()
    CP()

def CP():
    #INCLUYE TU CÓDIGO
    t = l.obtener_token()
    if t != None:
        # <C> == <R>
        if (t.subtipo_token == subtipos_token.IGUALDAD or
            t.subtipo_token == subtipos_token.DIFERENTE):
            print('Se reconocio: ', t.lexema)
            v.codigo += t.lexema + ' '
            # print(t)
            R()
            CP()
        else:
            l.regresar_token(t)

# <R> :== <R> < <ASR> | <R> > <ASR> | <R> <= <ASR> | <R> >= <ASR>  | <ASR>
def R():
    #INCLUYE TU CÓDIGO
    # <ASR>
    E()
    RP()

def RP():
    #INCLUYE TU CÓDIGO
    t = l.obtener_token()
    if t != None:
        if (t.subtipo_token == subtipos_token.OPERADOR_MENOR or
            t.subtipo_token == subtipos_token.OPERADOR_MAYOR or
            t.subtipo_token == subtipos_token.OPERADOR_MENOR_IGUAL or
            t.subtipo_token == subtipos_token.OPERADOR_MAYOR_IGUAL):
            print('Se reconocio: ', t.lexema)
            v.codigo += t.lexema + ' '
            # print(t)
            E()
            RP()
        else:
            l.regresar_token(t)

# <E> ::= <E> + <T> | <E> - <T>| <T>
def E():
    #INCLUYE TU CÓDIGO
    T()
    EP()

def EP():
    #INCLUYE TU CÓDIGO
    t = l.obtener_token()
    if t != None:
        if (t.subtipo_token == subtipos_token.OPERADOR_SUMA or
            t.subtipo_token == subtipos_token.OPERADOR_RESTA):
            print('Se reconocio: ', t.lexema)
            v.codigo += t.lexema + ' '
            # print(t)
            T()
            EP()
        else:
            l.regresar_token(t)

# <T> ::= <T> * <N> | <T> / <N> | <T> % <N> | <N>
def T():
    #INCLUYE TU CÓDIGO
    N()
    TP()

def TP():
    #INCLUYE TU CÓDIGO
    t = l.obtener_token()
    if t != None:
        if (t.subtipo_token == subtipos_token.OPERADOR_MULTIPLICACION or
            t.subtipo_token == subtipos_token.OPERADOR_DIVISION or
            t.subtipo_token  == subtipos_token.OPERADOR_MODULO):
            print('Se reconocio : ', t.lexema)
            v.codigo += t.lexema + ' '
            # print(t)
            N()
            TP()
        else:
            l.regresar_token(t)

# <N> ::= !<F> | <F>
def N():
    #INCLUYE TU CÓDIGO
    t = l.obtener_token()
    if t != None:
        if t.subtipo_token == subtipos_token.NEGACION:
            print('Se reconoce NEGACION !')
            v.codigo += '!'
            # print(t)
        else:
            l.regresar_token(t)
    F()

# <F> ::= Int | Float | <ID> | (<expresion>) | Char | Bool
def F():
    #INCLUYE TU CÓDIGO
    # Int | Float | Bool | Char
    t = l.obtener_token()
    if t != None:
        # Int
        if (t.subtipo_token == subtipos_token.ENTERO):
            print('Se reconoce ENTERO: ', t.lexema)
            if 'escribir' in v.lista_aux:
                v.codigo += t.lexema + '"'
            else:
                v.codigo += t.lexema
            # v.codigo += t.lexema
            # print(t)
        # Float
        elif t.subtipo_token == subtipos_token.REAL:
            print('Se reconoce REAL: ', t.lexema)
            if 'escribir' in v.lista_aux:
                v.codigo += t.lexema + '"'
            else:
                v.codigo += t.lexema
            # v.codigo += t.lexema
            # print(t)
        # Bool
        elif t.subtipo_token == subtipos_token.VERDADERO:
            print('Se reconoce LOGICO: ', t.lexema)
            if 'escribir' in v.lista_aux:
                v.codigo += t.lexema + '"'
            else:
                v.codigo += '1'
        elif t.subtipo_token == subtipos_token.FALSO:
            print('Se reconocio LOGICO: ', t.lexema)
            if 'escribir' in v.lista_aux:
                v.codigo += t.lexema + '"'
            else:
                v.codigo += '0'
        # Char
        elif t.tipo_token == tipo_token.CHAR:
            print('Se reconoce CHAR: ', t.lexema)
            if 'escribir' in v.lista_aux:
                v.codigo += t.lexema[1] + '"'
            else:
                v.codigo += t.lexema
        # identificador
        elif t.tipo_token == tipo_token.IDENTIFICADOR:
            print('Se reconoce IDENTIFICADOR: ', t.lexema)
            if 'escribir' in v.lista_aux:
                try:
                    v.codigo += v.identificadores[t.lexema] + '", '
                    v.codigo += t.lexema
                except:
                    print(f'Error en la linea {t.num_linea}, la variable: {t.lexema} no fue declarada')
                    v.band = True
            else:
                v.codigo += t.lexema
            # v.codigo += t.lexema
            # print(t)
        # (
        elif t.subtipo_token == subtipos_token.PARETESIS_IZQUIERDO:
            print('Se reconoce PARENTESIS_IZQ: ', t.lexema)
            v.codigo += '('
            # print(t)
            expresion()
            # )
            t = l.obtener_token()
            if t != None:
                if not se_espera(t.subtipo_token, subtipos_token.PARETESIS_DERECHO):
                    error(subtipos_token.PARETESIS_DERECHO, t.subtipo_token, t.num_linea)
                else:
                    print('Se reconoce PARENTESIS_DER: ', t.lexema)
                    v.codigo += ')'
                    # print(t)
        else :
            print('Se esperaba Entero o Real o Identificador o Parentesis izquierdo')
        



programa()
v.obtener_codigo()
#if not v.band:
# print(v.obtener_codigo())
#print(v.identificadores)