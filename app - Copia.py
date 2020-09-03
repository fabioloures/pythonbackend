from flask import Flask, jsonify, request, abort , render_template
from datetime import date
import datetime
from flask_sqlalchemy import SQLAlchemy #usado para acessar o banco de dados

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/feriados.db'
db = SQLAlchemy(app) #consultar a bd

#classe dos banco
class feriados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codibge  = db.Column(db.String(7))
    data  = db.Column(db.String(11))
    name  = db.Column(db.String(200))



fers = [
    {'codibge':'33',
     'data':'2020-01-02',
     'name': 'Carnaval'
     },
     {'codibge':'2345633',
     'data':'2020-03-02',
     'name': 'Pascoa'
      }
    ,

    {'codibge': '1',
     'data': '05-01',
     'name': 'Dia do Trabalhador',
     },
    {'codibge': '2',
     'data': '01-01',
     'name': 'Ano Novo',
     },
    {'codibge': '3',
     'data': '21-04',
     'name': 'Tiradentesr',
     },
    {'codibge': '4',
     'data': '07-09',
     'name': 'Independência',
     },
    {'codibge': '5',
     'data': '12-10',
     'name': 'Nossa Senhora Aparecida',
     },
    {'codibge': '6',
     'data': '02-11',
     'name': 'Finados',
     },
    {'codibge': '10',
     'data': '15-11',
     'name': 'Proclamação da República',
     },
    {'codibge': '11',
     'data': '22-12',
     'name': 'Natal',
     }
]


@app.route('/')
def homeprincial():
    return 'Api Feriados  Colossal'

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


       # new_feriado = feriados(codibge,cferiadoData,data) #"inserindo na BASE DE DADOS"
       # db.session.add(new_feriado)
       # db.session.commit()

    if (data[0:2].isdigit()): #fersAdd = [ {'codibge': codibge,'data': data ,'name': '' }]  #PUT  http://127.0.0.1:5000/feriados/3550308/01-25/  { "name": "Aniversário da cidade de São Paulo" }
        fersAdd = [{'codibge': '',
           'data':'',
            'name': ''
     }]
        fersAdd[0]['codibge'] = codibge
        fersAdd[0]['name']    = request.json.get('name', fersAdd[0]['name'])
        fersAdd[0]['data']    = data    #request.json.get('done', task[0]['done'])
    #if (len(data) > 0 and data.isdigit()()):  # caso feriado NACIONAIS

    fers.append(fersAdd[0])
    return jsonify({'Feriado Adicionado' : fersAdd})


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

    return '', 204
    #return jsonify(fers.remove(task[0]))

if __name__ == '__main__':
    #app.run(debug=False)
    app.run(debug=True)



