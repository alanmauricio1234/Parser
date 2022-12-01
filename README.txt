
# Parser

Se construye un Parser por traducción dirigida por sintáxis.
Dada una gramática el parser realiza el análisis sintactico y 
realiza su traducción a un código intermedio como lo es el
lenguaje C.


## Documentación
Se utilizó la notación Backus-Naur (BNF) el cual es un metalenguaje
usado para expresar grámaticas libres de contexto: es decir, una manera
formal de describir lenguajes formales.


Dada la siguiente gramática se realizó el parser:

<programa> ::= <proceso> <listaFunciones> | <proceso>

<listaFunciones> ::= <funcion> | <funcion> <listaFunciones>

<funcion> ::= <tipo> FUNCION <ID> (<parametros>) <listaOperaciones> REGRESAR <expresion> PCOMA FINFUNCION

<parametros> ::= <hayParametros> |@

<hayParametros> ::= <unParametro> | <masParametros>

<unParametro> ::= <ID>

<masParametros> ::= <ID> | <ID> COMA <masParametros>

<tipo> :: = ENTERO | REAL | LOGICO | CARACTER

<declaracion> ::= <declaracionEntero> | <declaracionReal> | <declaracionCaracter>
| <declaracionBoolean>

<declaracionEntero> ::=ENTERO <listadE> PCOMA

<listadE> ::=<de> | <de> COMA <listadE>

<de> ::= <ID> | <ID> = Int

<declaracionReal> ::=REAL <listadR> PCOMA

<listadR> ::= <dr> | <dr> COMA <listaR>

<dr> ::= <ID> | <ID> = Float

<declaracionLogico> ::=LOGICO <listadL> PCOMA

<listadL> ::=<dr> | <dr> COMA <listadL>

<dl> ::= <ID> | <ID> = Boolean

<declaracionChar> ::=CHAR <listadL> PCOMA

<listadC> ::= <dr> | <dc> COMA <listadL>

<dc> ::= <ID> | <ID> = Char

<invocacion> :: <ID> ( <parametros> )

<proceso>::=PROCESO <ID> <listaOperaciones> FINPROCESO

<listaOperaciones> ::= <operacion> <listaOperaciones> | <operacion>

<operacion>::= <declaracion> | <leer> | <escribir> | <asignacion> | <si> | ...

<asignacion> ::= <ID> = <expresion> PCOMA

<leer>::= LEER <listaLeer> PCOMA

<listaLeer>::= <ID>| <ID> COMA <listaLeer>

<escribir>::= ESCRIBIR <listaValor> PCOMA

<listaValor>::= <valor>| <valor> COMA <listaValor>

<valor>::= <expresion>| String

<si>::= SI ( <expresion> ) ENTONCES <listaOperaciones> FINSI |
SI (<expresion> )ENTONCES <listaOperaciones> SINO <listaOperaciones> FINSI

<mientras> ::= MIENTRAS (<expresion>) HACER <listaOperaciones> FINMIENTRAS

<para> ::= PARA <ID> = <op> HASTA <op> HACER <listaOperaciones> FINPARA |
PARA <ID> = <op> HASTA <op> CON PASO <op> HACER <listaOperaciones> FINPARA

<op> ::= Int | <ID>

<segun>::=SEGUN ( <op> ) HACER <listaCasos> OMISION DPUNTOS <listaOperaciones> ROMPER

<listaCasos> ::= <listaEnteros> DPUNTOS <listaOperaciones> ROMPER PCOMA | <listaCasos> <listaEnteros> DPUNTOS <listaOperaciones> ROMPER PCOMA

<listaEnteros> ::= ENTERO | ENTERO PCOMA <listaEnteros>

<expresion> ::= <expresion>||<Y> | <Y>

<Y> ::= <Y>&&<C> | <C>

<C> ::= <C>==<R> | <C>!=<R> | <R>

<R> ::= <R><<ASR> | <R>><A> | <R><=<ASR> | <R>>=<ASR> | <ASR>

<ASR> ::= <ASR>+<AMDM> | <ASR>-<AMDM> | <AMDM>

<AMDM> ::= <AMDM>*<N> | <AMDM>/<N> | <AMDM>%<N> | <N>

<N> ::= !<F> | <F>

<F> ::= Int | Float | <ID> | (expresion)

<ID>::= ([A-Z,a-z,_][A-Z,a-z,_,0-9]*
