from flask import Flask, flash, render_template, request, redirect, url_for
import psycopg2

# Chave secreta para a utilização da mensagem de erro flash
app = Flask(__name__)
app.secret_key = "my_secret_key"


# Configurações do banco de dados
db_config = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
}


# Mostra dados
def fetch_data_from_db():
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM data")
    data = cursor.fetchall()

    conn.close()
    return data


# Página index e suas verificações
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        description = request.form["description"]
        quantity = request.form["quantity"]
        code = request.form["code"]
        price = request.form["price"]
        category = request.form["category"]
        observation = request.form["observation"]

        # Verifique se o preço é um número com vírgula
        if not is_valid_price(price):
            return render_template(
                "index.html",
                saved_data=fetch_data_from_db(),
                error_message="O preço deve ser um número válido.",
            )

        # Processar o upload da imagem
        photo = request.files.get("photo")
        if photo:
            photo_data = photo.read()
        else:
            photo_data = None

        save_data(description, observation, code, price, quantity, category, photo_data)
        return redirect(url_for("index"))

    saved_data = fetch_data_from_db()

    return render_template("index.html", save_data=saved_data)


# Função para verificar se o preço é um número válido
def is_valid_price(price):
    try:
        # Tente converter o preço para um número de ponto flutuante
        float_price = float(price)
        return True
    except ValueError:
        return False


# Página login e suas verificações
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password),
        )
        user = cursor.fetchone()

        conn.close()

        if user:
            # Redirecione para a página principal se usuário for válido
            return redirect(url_for("index"))
        else:
            # Mensagem de erro
            flash("Login ou senha incorretos. Tente novamente.")

    return render_template("login.html")


# Rota para a página "data.html" através do navbar
@app.route("/data")
def data():
    saved_data = fetch_data_from_db()

    return render_template("data.html", saved_data=saved_data)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_data(id):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Execute a instrução SQL para excluir o registro com base no ID
        delete_query = "DELETE FROM data WHERE id = %s"
        cursor.execute(delete_query, (id,))

        # Commit para confirmar a exclusão no banco de dados
        conn.commit()

    except Exception as e:
        conn.rollback()

    finally:
        conn.close()

    return redirect(url_for("data"))


# Rota para a página de edição
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_data(id):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    if request.method == "POST":
        # Receba os novos valores dos campos do formulário de edição
        new_description = request.form["new_description"]
        new_observation = request.form["new_observation"]
        new_code = request.form["new_code"]
        new_price = request.form["new_price"]
        new_quantity = request.form["new_quantity"]
        new_category = request.form["new_category"]
        new_photo_data = None

        if not is_valid_price(new_price):
            return render_template(
                "index.html",
                saved_data=fetch_data_from_db(),
                error_message="O preço deve ser um número válido.",
            )

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
            conn.rollback()
        finally:
            conn.close()

        return redirect(url_for("data"))

    # Se for um pedido GET, exiba a página de edição com os dados atuais
    cursor.execute("SELECT * FROM data WHERE id = %s", (id,))
    data = cursor.fetchone()
    conn.close()

    if data:
        return render_template("edit.html", data=data)
    else:
        flash("Registro não encontrado.")
        return redirect(url_for("data"))


# Coleta dados e cadastra no banco
def save_data(description, observation, code, price, quantity, category, photo_data):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    try:
        insert_query = "INSERT INTO data (description, observation, code, price, quantity, category, photo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(
            insert_query,
            (description, observation, code, price, quantity, category, photo_data),
        )

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Erro ao salvar os dados:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
