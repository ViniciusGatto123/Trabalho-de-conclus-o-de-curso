from flask import Flask, flash, render_template, request, redirect, url_for # Módulos e funções Flask para a criação de um aplicativo Web.
import psycopg2 # Módulo para interação com banco de dados PostgreSQL


app = Flask(__name__) # Cria o nome do aplicativo, essencial para o Flask localizar recursos associados, como templates
app.secret_key = "my_secret_key" # Define uma chave secreta para o aplicativo Flask é usada para criptografar e proteger sessões e cookies
 

# Configurações do banco de dados
db_config = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
}


# Função que mostra dados da tabela "data" 
def fetch_data_from_db():
    conn = psycopg2.connect(**db_config) # Estabelece conexão com banco de dados PostgreSQL, acessando "db_config" que foi especificado anteriormente
    cursor = conn.cursor() # Criado objeto do tipo "cursor" para realizar comandos em SQL

    cursor.execute("SELECT * FROM data") # Realiza o comando SQL para recuperar todos os dados da tabela "data"
    data = cursor.fetchall() # Recupera todos os registros resultantes da consulta SQL em uma lista chamada "data"

    conn.close() # Fecha a conexão com o banco de dados após a recuperação dos dados
    return data # Retorna a lista de dados recuperados da tabela "data"


# Coleta dados e cadastra no banco
def save_data(description, observation, code, price, quantity, category, photo_data):
    conn = psycopg2.connect(**db_config) # Estabelece conexão com banco de dados PostgreSQL, acessando "db_config" que foi especificado anteriormente
    cursor = conn.cursor() # Criado objeto do tipo "cursor" para realizar comandos em SQL

    # Realiza o comando SQL para inserir os dados
    try:
        insert_query = "INSERT INTO data (description, observation, code, price, quantity, category, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(
            insert_query,
            (description, observation, code, price, quantity, category, photo_data),
        )

        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close() # Fecha a conexão com o banco de dados criada com o "cursor"


# Exclusão por ID
@app.route("/delete/<int:id>", methods=["POST"]) # Cria a rota chamada "/delete" que responde a solicitações POST e recebe um ID para exclusão
def delete_data(id):
    conn = psycopg2.connect(**db_config) # Estabelece conexão com banco de dados PostgreSQL, acessando "db_config" que foi especificado anteriormente
    cursor = conn.cursor() # Criado objeto do tipo "cursor" para realizar comandos em SQL

    try:
        delete_query = "DELETE FROM data WHERE id = %s"  # Execute a instrução SQL para excluir o registro com base no ID
        cursor.execute(delete_query, (id,))

        conn.commit() # Commit para confirmar a exclusão no banco de dados

    except Exception as e:
        conn.rollback() # Caso aconteça erro, toda alteração realizada é desfeita

    finally:
        conn.close() # Fecha a conexão com o banco de dados criada com o "cursor"

    return redirect(url_for("data")) # Após a exclusão usuário permanece na mesma página


# Rota para a página de edição
@app.route("/edit/<int:id>", methods=["GET", "POST"]) # Cria a rota chamada "/edit" que responde a solicitações GET e POST e recebe um ID para edição
def edit_data(id):
    conn = psycopg2.connect(**db_config) # Estabelece conexão com banco de dados PostgreSQL, acessando "db_config" que foi especificado anteriormente
    cursor = conn.cursor() # Criado objeto do tipo "cursor" para realizar comandos em SQL

    if request.method == "POST":
        # Receba os novos valores dos campos do formulário de edição
        new_description = request.form["new_description"]
        new_observation = request.form["new_observation"]
        new_code = request.form["new_code"]
        new_price = request.form["new_price"]
        new_quantity = request.form["new_quantity"]
        new_category = request.form["new_category"]
        new_photo_data = None

    # Processar o upload da imagem, se houver
    if "new_photo" in request.files:
        new_photo = request.files["new_photo"]
        if new_photo:
            new_photo_data = new_photo.read()

        try:
            # Execute a instrução SQL para atualizar o registro com base no ID
            update_query = """
                UPDATE data
                SET description = %s, observation = %s, code = %s, price = %s, quantity = %s, category = %s, photo = %s
                WHERE id = %s
            """
            cursor.execute(
                update_query,
                (
                    new_description,
                    new_observation,
                    new_code,
                    new_price,
                    new_quantity,
                    new_category,
                    new_photo_data,
                    id,
                ),
            )

            # Commit para confirmar a atualização no banco de dados
            conn.commit()

        except Exception as e:
            conn.rollback() # Caso aconteça erro, toda alteração realizada é desfeita
        finally:
            conn.close() # Fecha a conexão com o banco de dados criada com o "cursor"

        return redirect(url_for("data")) # Após a edição o usuário permanece na mesma página 

    # Se for um pedido GET, exiba a página de edição com os dados atuais
    cursor.execute("SELECT * FROM data WHERE id = %s", (id,))
    data = cursor.fetchone()
    conn.close() # Fecha a conexão com o banco de dados criada com o "cursor"

    if data:
        return render_template("edit.html", data=data) # Quando selecionar o botão de edição o usuário é redirecionado para essa página
    else:
        flash("Registro não encontrado.")
        return redirect(url_for("data"))


# Página login
@app.route("/", methods=["GET", "POST"]) # Cria a rota raiz "/" que responde a solicitações GET e POST, será a primeira tela do sistema
def login():
    if request.method == "POST": # Verifica se a solicitação HTTP é do tipo POST, Isso é usado para distinguir entre o carregamento inicial da página (GET) e o envio de um formulário (POST)
        username = request.form["username"]
        password = request.form["password"]
        # Obtém os valores digitados nos formulários

        conn = psycopg2.connect(**db_config) # Estabelece conexão com banco de dados PostgreSQL, acessando "db_config" que foi especificado anteriormente
        cursor = conn.cursor() # Criado objeto do tipo "cursor" para realizar comandos em SQL

        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password),
        )
        user = cursor.fetchone()

        conn.close() # Fecha a conexão com o banco de dados criada com o "cursor"

        if user:
            # Redirecione para a página principal se usuário for válido
            return redirect(url_for("index"))
        else:
            # Mensagem de erro
            flash("Login ou senha incorretos. Tente novamente.")

    return render_template("login.html")


# Página index
@app.route("/index", methods=["GET", "POST"]) # Cria a rota chamada "/index" que responde a solicitações GET e POST
def index():
    if request.method == "POST": # Verifica se a solicitação HTTP é do tipo POST, Isso é usado para distinguir entre o carregamento inicial da página (GET) e o envio de um formulário (POST)
        description = request.form["description"]
        quantity = request.form["quantity"]
        code = request.form["code"]
        price = request.form["price"]
        category = request.form["category"]
        observation = request.form["observation"]
        # Os campos acima obtém as informações do formulário na tela de "index.html" e armazena em uma variável

        # Processar o upload da imagem
        photo = request.files.get("photo") # Recebe o arquivo da foto enviado no formulário "photo"
        if photo:
            photo_data = photo.read() # Caso exista foto no formulário é executado essa linha e a foto é salva no banco
        else:
            photo_data = None # Caso não exista foto no formulário é executado essa linha e nada é salvo

        save_data(description, observation, code, price, quantity, category, photo_data) # Executa a função "save_data" para salvar todos os dados inseridos nos formulários
        return redirect(url_for("index")) # Após a execução de "save_data" é redirecionado para o próprio "index", ou seja, salva os dados e permanece na mesma tela

    saved_data = fetch_data_from_db() # Utiliza a função para recuperar os dados cadastrados e mostrar na tela de "index"

    return render_template("index.html", save_data=saved_data) # Renderiza a página "index.html"   


# Rota para a página "data.html" através do navbar
@app.route("/data") # Cria a rota chamada "/data" que responde a solicitações GET
def data():
    saved_data = fetch_data_from_db() # Retorna função de visualização de dados

    return render_template("data.html", saved_data=saved_data) # Renderiza a página "data.html"


# Executa o aplicativo logo que o arquvio Python também é executado
if __name__ == "__main__":
    app.run(debug=True)
