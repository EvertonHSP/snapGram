import os
from flask import Blueprint, send_from_directory, current_app

# Cria um Blueprint para as rotas de upload
upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/uploads/fotos_posts/<filename>')
def uploaded_file(filename):
    folder = os.path.join(current_app.root_path, "..",
                          "uploads", "fotos_posts")
    folder = os.path.abspath(folder)  # Garante que o caminho seja absoluto
    print(f"Usando caminho absoluto: {folder}")  # Debug

    return send_from_directory(folder, filename)
