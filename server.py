from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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