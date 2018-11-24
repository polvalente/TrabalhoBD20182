from flask import Flask, render_template, request, flash
from flask_wtf import Form
from wtforms import TextField, SubmitField, RadioField, SelectField

import mysql.connector
app = Flask(__name__)
app.secret_key = 'development key'

mydb = myusql.connector.connect(
    host='localhost',
    user='yourusername',
    passwd='yourpasswd'
)


@app.route('/', methods=["GET", "POST"])
def index():
    query_form = QueryForm()
    if request.method == 'POST':
        # executar query e mostrar resultados (o template a ser usa)
        return render_template('results.html', results=Query(query_form))
    elif request.method == 'GET':
        return render_template('index.html', form=query_form)

class QueryForm(Form):
    Sexo = SelectField('Sexo', choices = [
        ('F', 'Feminino'),
        ('M', 'Masculino')
        ])

    Cor = SelectField('Cor', choices = [
        ('Não Declarado', 'Não Declarado'),
        ('Branca', 'Branca'),
        ('Preta', 'Preta'),
        ('Parda', 'Parda'),
        ('Amarela', 'Amarela'),
        ('Indígena', 'Indígena')
        ])

    Query = SelectField('Queries', choices = [
        (0, 'Informação dos candidatos'),
        (1, 'Escolas por município'),
        (2, 'Candidatos com necessidades especiais'),
        (3, 'Métricas por tipo de escola'),
        (4, 'Número de notas acima da média por tipo de escola'),
        (5, 'Candidatos por tipo de escola'),
        (6, 'Quantidade de candidatos por sexo e cor*'),
        (7, 'Candidatos acima da média por sexo e cor*'),
        (8, 'Média por sexo e cor*')
        ])

    submit = SubmitField("Consultar")

class Query():
    def __init__(self, form):
        query_functions = {
            0: self.get_candidato_info,
            1: self.get_escolas_por_municipio,
            2: self.get_candidatos_especiais,
            3: self.get_metricas_tipo_escola,
            4: self.get_num_notas_acima_da_media_tipo_escola,
            5: self.num_candidatos_tipo_escola,
            6: self.get_candidatos_sexo_cor,
            7: self.get_sexo_cor_acima_media,
            8: self.get_media_sexo_cor
        }

        query = int(form.data['Query'])
        print(query)
        function = query_functions[query]
        if query >= 6:
            sexo = form.data['Sexo']
            cor = form.data['Cor']
            print(cor)
            print(sexo)
            self.result = function(sexo, cor)
        else:
            self.result = function()

    # select e projecao
    def get_candidato_info(self):
        cursor = mydb.cursor()
        cursor.execute("""
            select Candidato.idade as Idade,
            Candidato.sexo  as Sexo,
            Candidato.cor   as Cor
            from Candidato
        """)
        return cursor

    # 2 relacoes
    def get_escolas_por_municipio(self):
        cursor = mydb.cursor()
        cursor.execute("""
        select Endereco.Municipio as Municipio,
            Endereco.Rua as Rua,
            Endereco.UF as Estado,
            Escola.Nome as NomeDaEscola,
        from   Endereco
        left outer join Escola on Endereco.Cod_Endereco = Escola.fk_Endereco_Cod_Endereco
        """)
        return cursor

    def get_candidatos_especiais(self):
        cursor = mydb.cursor()
        cursor.execute("""
        select Candidato.idade as Idade,
            Candidato.sexo as Sexo,
            Candidato.cor as Cor
        inner join Realiza on Realiza.fk_Candidato_Nu_Inscricao = Candidato.Nu_Inscricao
        where Realiza.Especial = 'S'
        """)
        return cursor

    # 3 ou mais relacoes
    def get_metricas_tipo_escola(self):
        cursor = mydb.cursor()
        cursor.execute("""
        select Escola.Tipo as [Tipo da Escola],
            avg(Prova.Nota) as [Média das Notas],
            max(Prova.Nota) as [Nota Máxima],
            min(Prova.Nota) as [Nota Mínima]
        from Escola
        inner join Candidato on Candidato.fk_Escola_Cod_Escola = Escola.Cod_Escola
        inner join Realiza on Candidato.Nu_Inscricao = Realiza.fk_Candidato_Nu_Inscricao
        inner join Prova on Realiza.fk_Prova_Cod_Prova = Prova.Cod_Prova
        Group By [Tipo da Escola]
        """)
        return cursor

    def get_num_notas_acima_da_media_tipo_escola(self):
        cursor = mydb.cursor()
        cursor.execute("""
        select  Escola.Tipo as [Tipo da Escola],
            Count(Comp_Acima_Media.Comp_Acima_Media) as [Numero de Notas Acima da Média]
        from Escola
        inner join Candidato on Candidato.Escola_Cod_Escola = Escola.Cod_Escola
        inner join Comp_Acima_Media on Comp_Acima_Media.Comp_Acima_Media_PK = Candidato.fk_Comp_Acima_Media
        Group BY [Tipo da Escola]
        """)
        return cursor

    # Operacao sobre conjuntos

    # agregacao
    def get_candidatos_sexo_cor(self, sexo, cor):
        cursor = mydb.cursor()
        cursor.execute("""
        select Candidato.Sexo as [Sexo],
            Candidato.Cor as [Cor],
            Count(Candidato.Sexo) as [Quantidade por Sexo],
            Count(Candidato.Cor) as [Quantidade por Cor]

        from   Candidato
        Group BY [Sexo], [Cor]
        """)
        return cursor

    def get_sexo_cor_acima_media(self, sexo, cor):
        cursor = mydb.cursor()
        cursor.execute("""
        select
            Candidato.Sexo as [Sexo],
            Candidato.Cor as [Cor],
            Comp_Acima_Media.Comp_Acima_Media as [Competencia],
            Count(Comp_Acima_Media.Comp_Acima_Media) as [Numero de Ocorrencias]

        from   Candidato
        inner join Comp_Acima_Media on Candidato.fk_Comp_Acima_Media = Comp_Acima_Media.Comp_Acima_Media_PK
        Group BY [Competencia], [Sexo], [Cor]
        """)
        return cursor

    def get_media_sexo_cor(self, sexo, cor):
        cursor = mydb.cursor()
        cursor.execute("""
        select
            Candidato.Sexo,
            Candidato.Cor
            avg(Prova.Nota)
        from Prova
        inner join Realiza on Prova.Cod_Prova = Realiza.fk_Prova_Cod_Prova
        inner join Candidato on Realiza.fk_Candidato_Nu_Inscricao = Candidato.Nu_Inscricao
        """)
        return cursor

    # nested subquery
    def num_candidatos_tipo_escola(self):
        cursor = mydb.cursor()
        cursor.execute("""
            select Count(TB.[Inscricao]) as [Numero de Candidatos],
            TB.[Tipo da Escola] as [Tipo da Escola]
        from
            (select Candidato.Nu_Inscricao as [Inscricao],
                    Escola.Tipo as [Tipo da Escola]
                    inner join Escola on Candidato.fk_Escola_Cod_Escola = Escola.Cod_Escola
                )
        Group By [Tipo da Escola]
        """)
        return cursor

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')