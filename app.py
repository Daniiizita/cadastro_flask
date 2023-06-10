from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'tasks_flask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'



mysql = MySQL(app)

tasks = []

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       task VARCHAR(255) NOT NULL
                   )''')
    mysql.connection.commit()
    cursor.close()

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
    mysql.connection.commit()
    cursor.close()
    return redirect('/')


@app.teardown_appcontext
def close_db_connection(exception=None):
    mysql.connection.rollback()
    mysql.connection.close()

if __name__ == '__main__':
    app.run(debug=True)

