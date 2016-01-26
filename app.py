from flask import Flask, render_template
from simplemysql import SimpleMysql
from config import config

app = Flask(__name__)

def getdb():
    db = SimpleMysql(
            host = config['db_host'], 
            db = config['db_name'], 
            user = config['db_username'],
            passwd = config['db_password']
            )
    return db

@app.route('/')
def index():
    db = getdb()
    checks = db.getAll('checks')
    return render_template('index.html', checks = checks)

if __name__ == '__main__':
    app.run(debug=True)
