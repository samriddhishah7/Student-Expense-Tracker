from flask import Flask, jsonify
import os
from .config import DATABASE_PATH, API_PORT


def create_app():
    app = Flask(__name__)
    app.config['DATABASE_PATH'] = DATABASE_PATH

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"}), 200

    return app


def init_db_file(path=None):
    """Ensure the database file and parent directory exist.

    This function will create the parent directory if needed and create an empty
    database file if it does not exist. It will NOT overwrite an existing file.
    """
    p = path or DATABASE_PATH
    if p == ':memory:':
        return p

    parent = os.path.dirname(p)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    # Create the file if it does not exist; do not truncate/overwrite
    if not os.path.exists(p):
        open(p, 'a').close()

    return p


if __name__ == '__main__':
    app = create_app()
    init_db_file()
    app.run(host='0.0.0.0', port=API_PORT)
