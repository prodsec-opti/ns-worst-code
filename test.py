# sql_injection.py
import sqlite3
from flask import Flask, request
from articles.config import Config


app = Flask(__name__)
DB = "test.db"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=Config.DEBUG, port=Config.FLASK_PORT, use_reloader=Config.USE_RELOADER)
