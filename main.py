from app import create_app

# Cria a instância da aplicação Flask
app = create_app()

# Inicia o servidor Flask quando o script for executado diretamente
if __name__ == "__main__":
    # Inicia o servidor na porta 5000 e no host 0.0.0.0
    with app.app_context():
       app.run(host="0.0.0.0", port=5000, debug=True)
