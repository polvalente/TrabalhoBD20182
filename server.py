from flask import Flask, render_template, request, flash
from flask_wtf import Form
from wtforms import TextField, SubmitField, RadioField, SelectField
app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=["GET", "POST"])
def index():
    query_form = QueryForm()
    if request.method == 'POST':
        if query_form.validate() == False:
            flash('Preenchimento inválido do formulário')
            return render_template('index.html/#query', form=query_form)
        else:
            # executar query e mostrar resultados
            return render_template('results.html', results=query_from_form(query_form)))
    elif request.method == 'GET':
        return render_template('index.html', form=query_form)

class QueryForm(Form):
    Sexo = SelectField('Sexo', choices = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('X', 'Outros')
        ])

    Cor = SelectField('Cor', choices = [
        ('1', 'Cor1'),
        ('2', 'Cor2')
        ])

    Query = SelectField('Queries', choices = [
        ('1', 'Informação dos candidatos'),
        ('2', 'Escolas por Município')
        ])

    submit = SubmitField("Consultar")

# select e projecao
def get_candidato_info():
    raise NotImplementedError

# 2 relacoes
def get_escolas_por_municipio():
    raise NotImplementedError

def get_candidatos_especiais():
    raise NotImplementedError

# 3 ou mais relacoes
def get_metricas_tipo_escola():
    raise NotImplementedError

def get_num_notas_acima_da_media_tipo_escola():
    raise NotImplementedError

# Operacao sobre conjuntos

# agregacao
def get_candidatos_sexo_cor(sexo, cor):
    raise NotImplementedError

def get_sexo_cor_acima_media(sexo, cor):
    raise NotImplementedError

def get_media(sexo, cor):
    raise NotImplementedError

# nested subquery
def num_candidatos_tipo_escola():
    raise NotImplementedError

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')