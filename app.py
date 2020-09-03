from flask import Flask, jsonify, request, abort , render_template
from datetime import date
import datetime
from flask_sqlalchemy import SQLAlchemy #usado para acessar o banco de dados

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/feriados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #consultar a bd

#classe dos banco = Feriados
class Feriados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codibge  = db.Column(db.String(7))
    data  = db.Column(db.String(10))
    name  = db.Column(db.String(200))

#classe dos banco = municipios (ibge)
class Municipios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_ibge  = db.Column(db.String(7))
    nome  = db.Column(db.String(200))

def finsfe(codigo,datafer,nomefer):
    new_feriadoatual = Feriados(codibge=codigo, data=datafer, name=nomefer)
    db.session.add(new_feriadoatual)
    db.session.commit()
    return("OK")

#A sua API deve ser populada com os feriados nacionais.
#C:\Users\Casa\PycharmProjects\pythonbackend\database>set PATH=%PATCH%;C:\sqlite;
#C:\Users\Casa\PycharmProjects\pythonbackend\database>sqlite3 feriados.db
#outro terminal
#(.venv) C:\Users\Casa\PycharmProjects\pythonbackend>python
#>>> from app import db
#>>> db.create_all()
#inserindo os feriados nacionais na base de dados
def finsnacional():
    records = Feriados.query.filter_by(codibge = '1').first()
    if records == None:
        cretfer3 = finsfe('1','05-01','Dia do Trabalhador')

    records = Feriados.query.filter_by(codibge = '2').first()
    if records == None:
        cretfer3 = finsfe('2','01-01','Ano Novo')

    records = Feriados.query.filter_by(codibge = '3').first()
    if records == None:
        cretfer3 = finsfe('3','04-21','Tiradentes')


    records = Feriados.query.filter_by(codibge = '4').first()
    if records == None:
        cretfer3 = finsfe('4','09-07','Independência')

    records = Feriados.query.filter_by(codibge = '5').first()
    if records == None:
        cretfer3 = finsfe('5','10-12','Nossa Senhora Aparecida')

    records = Feriados.query.filter_by(codibge = '6').first()
    if records == None:
        cretfer3 = finsfe('6','11-02','Finados')

    records = Feriados.query.filter_by(codibge = '7').first()
    if records == None:
        cretfer3 = finsfe('7','11-15','Proclamação da República')

    records = Feriados.query.filter_by(codibge = '8').first()
    if records == None:
        cretfer3 = finsfe('8','12-25','Natal')
    return ("OK")


#(comentar abaixo para criar o banco e tabelas )
cret = finsnacional()


#existing = Feriados.query.filter(Feriados.codibge=='2').first()
#if existing != None:  cretfer = finsereferiado('2','01-01','Ano Novo')

#new_feriado2 = Feriados(codibge='2', data='01-01', name='Ano Novo')
#db.session.add(new_feriado2)
#db.session.commit()


# carrega a base de dados em json
#A sua API deve ser populada com os feriados nacionais.
# Todos os feriados estaduais e municipais consultados nos testes serão criados através da API.
#comentar abaixo para criar a tabela
cols = ['codibge', 'data', 'name']
data = Feriados.query.all()
fers = [{col: getattr(d, col) for col in cols} for d in data]

@app.route('/')
def homeprincial():
    return 'Api Feriados: Colossal'

@app.route('/feriados/', methods=['GET'])
def home():
    return jsonify(fers), 200


@app.route('/feriados/<string:codibge>/<string:data>/', methods=['GET'])
def fers_per_feriado(codibge,data):

    fers_per_feriado = [fer for fer in fers
                        if fer['data'] ==  data[len(data) - 5:len(data) - 3] + "-" + data[len(data) - 2:len(data)]
                        or fer['codibge'] == codibge and fer['data'] == data]

    # 1) VERIFICAR SE A DATA PASSADA E UM FERIADO MOVEL  -> if len(fers_per_feriado)==0:
    # let query = http.get(`${BASE_URL}/feriados/2111300/2020-04-10/`);   'é Sexta-Feira Santa em São Luís':

    feriadonome = ""
    if len(fers_per_feriado) == 0:
       feriadonome = feriadomovel(data[0:4], data) # passando o ANO para ver se e a data para ver se é um feriado movel (RETORNA O NOME)
       cferiadoData = dtferiadomovel(feriadonome)  # passando o NOME DO FERIADO (RETORNA A DATA)
    if(len(feriadonome)>0): fers_per_feriado = [{'codibge': codibge,'data': cferiadoData ,'name': feriadonome } ]

    if len(fers_per_feriado)==0: abort(404, description="Resource not found")

    #Onde CODIGO-IBGE pode ser um número de dois dígitos, para representar um feriado estadual ou um número com 7 dígitos para representar um feriado municipal.
    return jsonify({'name':fers_per_feriado[0]['name']}), 200

# passando o ANO para ver se e a data para ver se é um feriado movel (RETORNA O NOME)
def feriadomovel(str_ano, str_data):
    print('feriadomovel ano:'+str_ano)
    print('feriadomovel data:'+str_data)
    cferiado = ""
    X = 24
    Y = 5
    ANO = int(str_ano)
    A = ANO % 19
    # print A
    B = ANO % 4
    # print B
    C = ANO % 7
    # print C
    D = (19 * A + X) % 30
    # print D
    E = (2 * B + 4 * C + 6 * D + Y) % 7
    # print E
    if ((D + E) > 9):
        DIA = D + E - 9
        MES = 4
        if DIA < 10:
            DIAATUAL = "0" + str(DIA)
        else:
            DIAATUAL = str(DIA)

        PASCOA = str(ANO) + "-0" + str(MES) + "-" + DIAATUAL
        if(str_data==PASCOA): cferiado = "Pascoa"
        DATA1 = date(ANO, MES, DIA)

        # O carnaval sera a subtracao de 47 dias da data da pascoa
        CARNAVAL = date.fromordinal(DATA1.toordinal() - 47)
        if (str_data == str(CARNAVAL)): cferiado = "Carnaval"

        # corpus christi ocorre 60 dias após o domingo de Páscoa
        CORPUSCRISTI = date.fromordinal(DATA1.toordinal() + 60)
        if (str_data == str(CORPUSCRISTI)): cferiado = "Corpus Christi"

        # A sexta-feira santa ocorre 2 dias antes do domingo de Páscoa
        SEXTAFEIRASANTA = date.fromordinal(DATA1.toordinal() - 2)
        if (str_data == str(SEXTAFEIRASANTA)): cferiado = "Sexta-Feira Santa"

    else:
        DIA = D + E + 22
        MES = 3

        if DIA < 10:
            DIAATUAL = "0" + str(DIA)
        else:
            DIAATUAL = str(DIA)

        PASCOA = str(ANO) + "-0" + str(MES) + "-" + DIAATUAL
        if (str_data == PASCOA): cferiado = "Pascoa"

        DATA1 = date(ANO, MES, DIA)
        CARNAVAL = date.fromordinal(DATA1.toordinal() - 47)
        if (str_data == str(CARNAVAL)): cferiado = "Carnaval"

        # corpus christi ocorre 60 dias após o domingo de Páscoa
        CORPUSCRISTI = date.fromordinal(DATA1.toordinal() + 60)
        if (str_data == str(CORPUSCRISTI)): cferiado = "Corpus Christi"

        # A sexta-feira santa ocorre 2 dias antes do domingo de Páscoa
        SEXTAFEIRASANTA = date.fromordinal(DATA1.toordinal() - 2)
        if (str_data == str(SEXTAFEIRASANTA)): cferiado = "Sexta-Feira Santa"


    return (cferiado)



#CADASTRO -> PUT /feriados/5108402/carnaval/
@app.route('/feriados/<string:codibge>/<string:data>/', methods=['PUT'])
def editOne(codibge, data, name =None):

    # se codigo ibge nao existe na tabela nao deixa cadastrar
    existcodibge = Municipios.query.filter_by(codigo_ibge=codibge).first()
    if existcodibge == None: return (abort(404)) # se codigo ibge nao existe na tabela nao deixa cadastrar

    #data erro validando data - completa
    cretdt = True
    if(len(data)==10 and data[0:4].isdigit()): cretdt = fvalidadt(data[0:4],data[5:7],data[8:10]) ##2021-04-20 #2021-04-20  #validando as datas antes de inserir
    if  not cretdt:  return (abort(404))

    # data erro validando data - mes e dia
    cretdt = True
    print('data[0:2]:'+data[0:2])
    print('data[3:5]:'+data[3:5])
    if (len(data) == 5 and data[0:1].isdigit()): cretdt = fvalidadt1(data[0:2], data[3:5])  ##04-20 mes e dia
    if not cretdt:  return (abort(404))

    # Se já existir um feriado cadastrado neste dia para o estado ou município especificado,
    # o nome do feriado deve ser atualizado.
    existbd = Feriados.query.filter_by(codibge=codibge).filter_by(data=data).first()
    #if existbd != None: print("existbd != None EXISTE NO BANCO")

    cmsgadd = ""
    #1) calcular pelo nome a DATA (FERIADOS MOVEL) , PASSOu UM NOME NO TEXTO PARA INSERIR PUT /feriados/5108402/carnaval/  /feriados/4312658/corpus-christi/
    cferiadoData = ""
    if (len(data) > 0 and data[0:2].isalpha()):
        cferiadoData = dtferiadomovel(data)  # passando o NOME DO FERIADO (RETORNA A DATA)
        if(data=="corpus-christi"): data = "Corpus Christi"
        #print('nome do feriado cferiadoData RETORNADO:' + cferiadoData)
    if (len(cferiadoData) > 0): fersAdd = [ {'codibge': codibge, 'data': cferiadoData, 'name': data}]

    if (data == "corpus-christi"): data = "Corpus Christi"

    if ( len(data) > 0 and  data[0:2].isalpha() ):
        fersAdd = [{'codibge': codibge,'data': cferiadoData,'name': data } ]  # NACIONAL http://127.0.0.1:5000/feriados/4312658/corpus-christi/    /feriados/5108402/carnaval/

#
    if (data[0:1].isdigit() or (existbd != None) ) : #fersAdd = [ {'codibge': codibge,'data': data ,'name': '' }]  #PUT  http://127.0.0.1:5000/feriados/3550308/01-25/  { "name": "Aniversário da cidade de São Paulo" }
        fersAdd = [{'codibge': '',
           'data':'',
            'name': ''
     }]
        fersAdd[0]['codibge'] = codibge
        fersAdd[0]['name']    = request.json.get('name', fersAdd[0]['name'])
        fersAdd[0]['data']    = data    #request.json.get('done', task[0]['done'])
    #if (len(data) > 0 and data.isdigit()()):  # caso feriado NACIONAIS

  # ADD ABAIXO PARA NAO DEIXAR DUPLICAR
    exist = Feriados.query.filter_by(codibge=fersAdd[0]['codibge']).filter_by(data=fersAdd[0]['data']).first() # confere primeiro se o registro existe no BD
    if ( len(fersAdd) > 0  and cmsgadd=="" and exist == None ): cmsgadd =  inserebd(fersAdd[0]['codibge'],fersAdd[0]['data'],fersAdd[0]['name'] ) #cod, cdata, cnome

    #caso existe na BD e nao foi inserido
    if (existbd != None and cmsgadd=="" and len(fersAdd) > 0): cmsgupd = updatebd(fersAdd[0]['codibge'],fersAdd[0]['data'],fersAdd[0]['name'] ) #cod, cdata, cnome

    if exist == None:  fers.append(fersAdd[0])

    return jsonify({'Feriado Adicionado' : fersAdd})

def fvalidadt1(mes, dia) : ##04-20 mes e dia
    cRet = True
    if (int(mes) == 0):
        cRet = False
    if (int(mes) > 12):
        cRet = False
    if (int(dia) > 31):
        cRet = False

    if (mes == "01" and int(dia) > 31):  # janeiro
        cRet = False
    if (mes == "02" and int(dia) > 30):  # fevereiro
        cRet = False
    if (mes == "03" and int(dia) > 31):  # março
        cRet = False
    if (mes == "04" and int(dia) > 30):  # abril
        cRet = False
    if (mes == "05" and int(dia) > 31):  # maio
        cRet = False
    if (mes == "06" and int(dia) > 30):  # jun
        cRet = False
    if (mes == "07" and int(dia) > 31):  # jul
        cRet = False
    if (mes == "08" and int(dia) > 31):  # ago
        cRet = False
    if (mes == "09" and int(dia) > 30):  # set
        cRet = False
    if (mes == "10" and int(dia) > 31):  # out
        cRet = False
    if (mes == "11" and int(dia) > 30):  # nov
        cRet = False
    if (mes == "12" and int(dia) > 31):  # dez
        cRet = False
    return (cRet)

#O MES deve ser um mês válido, ou seja, entre 1 e 12. Mesmo cuidado deve ser tomado com o dia. Espere um ano com 4 números, mês com 2 números e dia também com 2 números, ou seja, "AAAA-MM-DD".
def fvalidadt(ano,mes,dia): ##2021-04-20
    cRet = True
    if(len(ano)<4):
        cRet = False
    if (int(mes)==0):
        cRet = False
    if (int(mes) >12):
        cRet = False
    if (int(dia) >31):
        cRet = False

    if (mes=="01" and int(dia) >31): # janeiro
        cRet = False
    if (mes=="02" and int(dia) >30): # fevereiro
        cRet = False
    if (mes=="03" and int(dia) >31): # março
        cRet = False
    if (mes=="04" and int(dia) >30): # abril
        cRet = False
    if (mes=="05" and int(dia) >31): # maio
        cRet = False
    if (mes=="06" and int(dia) >30): # jun
        cRet = False
    if (mes == "07" and int(dia) > 31):  # jul
        cRet = False
    if (mes == "08" and int(dia) > 31):  # ago
        cRet = False
    if (mes == "09" and int(dia) > 30):  # set
        cRet = False
    if (mes == "10" and int(dia) > 31):  # out
        cRet = False
    if (mes == "11" and int(dia) > 30):  # nov
        cRet = False
    if (mes == "12" and int(dia) > 31):  # dez
        cRet = False
    return (cRet)

def inserebd(cod, cdata, cnome):
    new_feriado = Feriados(codibge=cod,data=cdata,name=cnome)
    db.session.add(new_feriado)
    db.session.commit()
    return ("ok")

def updatebd(cod, cdata, cnome):
    feriadoupd = Feriados.query.filter_by(codibge=cod).filter_by(data=cdata).first()
    feriadoupd.name = cnome
    db.session.commit()
    return ("ok")



def dtferiadomovel(cnomeferiado):
    cferiadodt = ""
    X = 24
    Y = 5
    ANO = datetime.date.today().year
    A = ANO % 19
    # print A
    B = ANO % 4
    # print B
    C = ANO % 7
    # print C
    D = (19 * A + X) % 30
    # print D
    E = (2 * B + 4 * C + 6 * D + Y) % 7
    # print E
    if ((D + E) > 9):
        DIA = D + E - 9
        MES = 4
        if DIA < 10:
            DIAATUAL = "0" + str(DIA)
        else:
            DIAATUAL = str(DIA)

        PASCOA = str(ANO) + "-0" + str(MES) + "-" + DIAATUAL
        if (cnomeferiado == "pascoa"): cferiadodt= PASCOA

        DATA1 = date(ANO, MES, DIA)
        # O carnaval sera a subtracao de 47 dias da data da pascoa
        CARNAVAL = date.fromordinal(DATA1.toordinal() - 47)

        if (cnomeferiado == "carnaval"): cferiadodt= str(CARNAVAL)

        # corpus christi ocorre 60 dias após o domingo de Páscoa
        CORPUSCRISTI = date.fromordinal(DATA1.toordinal() + 60)
        if (cnomeferiado) == "corpus-christi": cferiadodt= str(CORPUSCRISTI)
        if (cnomeferiado) == "corpus christi": cferiadodt=str(CORPUSCRISTI)

        # A sexta-feira santa ocorre 2 dias antes do domingo de Páscoa
        SEXTAFEIRASANTA = date.fromordinal(DATA1.toordinal() - 2)
        if (cnomeferiado == "sexta-feira santa"): cferiadodt= str(SEXTAFEIRASANTA)
        if (cnomeferiado == "sexta-feira-santa"): cferiadodt= str(SEXTAFEIRASANTA)
    else:
        DIA = D + E + 22
        MES = 3
        if DIA < 10:
            DIAATUAL = "0" + str(DIA)
        else:
            DIAATUAL = str(DIA)

        PASCOA = str(ANO) + "-0" + str(MES) + "-" + DIAATUAL
        if (cnomeferiado == "pascoa"): cferiadodt= str(DIAATUAL)

        DATA1 = date(ANO, MES, DIA)
        CARNAVAL = date.fromordinal(DATA1.toordinal() - 47)
        if (cnomeferiado == "carnaval"): cferiadodt= str(CARNAVAL)

        # corpus christi ocorre 60 dias após o domingo de Páscoa
        CORPUSCRISTI = date.fromordinal(DATA1.toordinal() + 60)
        if (cnomeferiado) == "corpus-christi": cferiadodt= str(CORPUSCRISTI)
        if (cnomeferiado) == "Corpus christi": cferiadodt= str(CORPUSCRISTI)
        if (cnomeferiado) == "corpus christi": cferiadodt= str(CORPUSCRISTI)
        if (cnomeferiado) == "Corpus Christi": cferiadodt= str(CORPUSCRISTI)

        # A sexta-feira santa ocorre 2 dias antes do domingo de Páscoa
        SEXTAFEIRASANTA = date.fromordinal(DATA1.toordinal() - 2)
        if (cnomeferiado == "sexta-feira santa"): cferiadodt= str(SEXTAFEIRASANTA)
        if (cnomeferiado == "sexta-feira-santa"): cferiadodt = str(SEXTAFEIRASANTA)
    return (cferiadodt)


# DELETE /feriados/3550308/01-25/   Exemplo de remoção do aniversário de São Paulo:
#O endpoint deve retornar 404 se esse feriado não existir ou 204 se a requisição foi aceita e o feriado removido com sucesso.
#Uma tentativa de remover um feriado estadual num município deve retornar 403. Uma tentativa de remover um feriado nacional em um município ou em uma unidade federativa também deve retornar 403.
#@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@app.route('/feriados/<string:codibge>/<string:data>/', methods=['DELETE'])
def delete_task(codibge,data):
    task = [task for task in fers if
            task['data'] == data or task['codibge'] == codibge]
    if len(task) > 0 and len(data) < 6 and len(codibge) > 4 : #and task['data'] == data: #and task['data'] != data[len(data) - 5:len(data) - 3] + "-" + data[len(data) - 2:len(data)] :
        abort(403);



    if len(task)>0: fers.remove(task[0])


    #existing = Feriados.query.filter(codibge == task[0]['codibge'], data == data).first()
    #print("task[0]['codibge']:"+task[0]['codibge'])
    #print("task[0]['data']:"+task[0]['data'])

    #existing = Feriados.query.filter(Feriados.codibge == task[0]['codibge']).filter(Feriados.data == task[0]['data']).first()
    #print("existing.codibge"+existing.codibge)
    #if existing != None:
    #    print('Exists para excluir')

    if len(task[0]) > 0: cret = deletBd(task[0]['codibge'], task[0]['data']) # removendo do banco de dados


    return '', 204
    #return jsonify(fers.remove(task[0]))


def deletBd(ccodigo, cdata): # removendo do banco de dados
    #Feriados.query.filter_by(Feriados.codibge == ccodigo, Feriados.data == cdata).delete()  # removendo do banco de dados
#    Feriados.query.filter_by(Feriados.codibge == ccodigo).filter_by(Feriados.data == cdata).delete()
    Feriados.query.filter(Feriados.codibge == ccodigo).filter(Feriados.data == cdata).delete()
    db.session.commit()
    return ("ok")


if __name__ == '__main__':
    #app.run(debug=False)
    app.run(debug=True)



