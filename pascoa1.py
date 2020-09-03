from datetime import date


X = 24
Y = 5
ANO = int(input("Informe o ANO :"))
A = ANO % 19
#print A
B = ANO % 4
#print B
C = ANO % 7 
#print C
D = ( 19 * A + X ) % 30
#print D
E = ( 2 * B + 4 * C + 6 * D + Y ) % 7
#print E
if ( (D + E ) > 9 ):
    DIA = D + E - 9
    #print ("A Pascoa sera dia "+str(DIA)+" de Abril")
    MES = 4
    if DIA < 10: DIAATUAL = "0"+str(DIA)
    else:  DIAATUAL = str(DIA)

    print ("A Pascoa sera dia "+str(DIA)+" de Março")

    PASCOA = str(ANO)+"-0"+str(MES)+"-"+DIAATUAL
    print("A Pascoa sera dia " + PASCOA)

    DATA1 = date(ANO, MES, DIA )
    # O carnaval sera a subtracao de 47 dias da data da pascoa
    CARNAVAL = date.fromordinal(DATA1.toordinal()-47 )
    print ("O Carnaval sera na data :"+str(CARNAVAL))

    #corpus christi ocorre 60 dias após o domingo de Páscoa
    CORPUSCRISTI = date.fromordinal(DATA1.toordinal()+60 )
    print ("O corpus christi sera na data :"+str(CORPUSCRISTI))

   #A sexta-feira santa ocorre 2 dias antes do domingo de Páscoa
    SEXTAFEIRASANTA = date.fromordinal(DATA1.toordinal()-2 )
    print ("A sexta-feira santa sera na data :"+str(SEXTAFEIRASANTA))

else:
    DIA = D + E + 22
    print ("A Pascoa sera dia "+str(DIA)+" de Março")
    MES = 3
    if DIA < 10: DIAATUAL = "0"+str(DIA)
    else:  DIAATUAL = str(DIA)

    PASCOA = str(ANO)+"-0"+str(MES)+"-"+DIAATUAL
    print("A Pascoa sera dia " + PASCOA)

    DATA1 = date(ANO, MES, DIA )
    CARNAVAL = date.fromordinal(DATA1.toordinal()-47 )
    print ("O Carnaval sera na data :"+str(CARNAVAL))

    CARNAVAL = date.fromordinal(DATA1.toordinal()-47 )
    print ("O Carnaval sera na data :"+str(CARNAVAL))

    #corpus christi ocorre 60 dias após o domingo de Páscoa
    CORPUSCRISTI = date.fromordinal(DATA1.toordinal()+60 )
    print ("O corpus christi sera na data :"+str(CORPUSCRISTI))

    #A sexta-feira santa ocorre 2 dias antes do domingo de Páscoa
    SEXTAFEIRASANTA = date.fromordinal(DATA1.toordinal()-2 )
    print ("A sexta-feira santa sera na data :"+str(SEXTAFEIRASANTA))