import time
import datetime
#from datetime import date
print (' _______________________________________')
anoatual = datetime.date.today().year #date.today()
#ano=input('Digite o ano desejado para calcularmos o dia da páscoa: ')
ano= int(input('Digite o ano desejado para calcularmos o dia da páscoa: '))
a=ano%19
b=int(ano/100)
c=ano%100
d=int(b/4)
e=b%4
f=int((b+8)/25)
g=int((b-f+1)/3)
h=((19*a+b-d-g+15)%30)
i=int(c/4)
k=c%4
L=((32+2*e+2*i-h-k)%7)
m=int(a+11*h+22*L)/451
mes=int((h+L-7*m+114)/31)
if mes==1 : mes='Janeiro'
elif mes==2 : mes='Fevereiro'
elif mes==3 : mes='Março'
elif mes==4 : mes='Abril'
elif mes==5 : mes='Maio'
elif mes==6 : mes='Junho'
elif mes==7 : mes='Julho'
elif mes ==8 : mes ='Agosto'
elif mes ==9 : mes ='Setembro'
elif mes ==10 : mes ='Outubro'
elif mes ==11 : mes ='Novembro'
else : mes ='Dezembro'
mes1=mes
dia=((h+L-7*m+114)%31)+1
if anoatual>ano :
    print("A pascoa caiu no dia: %s." % dia)
    #   print ("A pascoa ira cair no dia:"+str(dia))
    print("Do mês: %s" % mes1)
else :
    print("A pascoa ira cair no dia: %s." % dia)
    print("Do mês: %s" % mes1)

    #print ("Do m�s: %s"+str(mes1))
