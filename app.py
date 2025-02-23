from app import create_app
from app.extensions import db
import os

# Cria o aplicativo Flask
app = create_app()

# Verifica se o banco de dados existe
with app.app_context():
    db_path = os.path.join(app.instance_path, 'site.db')
    if not os.path.exists(db_path):
        print("Banco de dados não encontrado. Criando banco de dados...")
        db.create_all()  # Cria todas as tabelas definidas nos modelos
        print("Banco de dados criado com sucesso!")
    else:
        print("Banco de dados já existe.")

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
