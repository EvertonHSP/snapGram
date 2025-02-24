import os
from flask import Blueprint, send_from_directory, current_app


upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/uploads/fotos_posts/<filename>')
def uploaded_file(filename):
    folder = os.path.join(current_app.root_path, "..",
                          "uploads", "fotos_posts")
    folder = os.path.abspath(folder) 
    return send_from_directory(folder, filename)
