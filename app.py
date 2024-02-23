import flask, psycopg2, os
from flask import jsonify, request, render_template, redirect, url_for, session
from contextlib import contextmanager
from dotenv import load_dotenv
import datetime

load_dotenv('.env')

app = flask.Flask(__name__)

# Secret key
app.secret_key = os.environ['SECRET_KEY']

# Database connection
@contextmanager
def get_db():
    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )
    cur = conn.cursor()
    try:
        yield cur
    except Exception as e:
        print(e)
        raise
    finally:
        conn.commit()
        cur.close()
        conn.close()

# Main page
@app.route('/', methods=['GET'])
def main():
    if 'username' in session:
        return render_template('index.html', tasks=get_tasks())
    else:
        return render_template('index.html')
    
@app.route('/home', methods=['GET'])
def home():
    return redirect('/')


@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    # get tasks from the db of user in session searching by id
    with get_db() as db:
        db.execute('SELECT * FROM tasks WHERE user_id = (SELECT id FROM users WHERE username = %s)', (session['username'],))
        tasks = db.fetchall()
    return tasks

@app.route('/complete_task', methods=['POST'])
def complete_task():
    data = request.json
    print(data)
    try:
        with get_db() as db:
            db.execute('UPDATE tasks SET completed = %s WHERE id = %s', (data['completed'], data['taskId']))
        return jsonify({'message': 'Task completed'})
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error completing task'})
    
@app.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.json
    try:
        with get_db() as db:
            db.execute('DELETE FROM tasks WHERE id = %s', (data['taskId'],))
        return jsonify({'message': 'Task deleted'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error deleting task'})

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    try:
        with get_db() as db:
            if data['dueDate']:
                db.execute('INSERT INTO tasks (user_id, title, description, due_date) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s, %s)', (session['username'], data['title'], data['description'], data['dueDate']))
            else:
                db.execute('INSERT INTO tasks (user_id, title, description) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s)', (session['username'], data['title'], data['description']))

        return jsonify({'message': 'Task added'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error adding task'})
    
@app.route('/tasks', methods=['GET'])
def tasks():
    if 'username' in session:
        return render_template('tasks.html', tasks=get_tasks())
    else:
        return redirect('/denied')

@app.route('/register', methods=['POST'])
def register():
    # recibe un json con username, name, password, email
    data = request.json

    try:
        with get_db() as db:
            db.execute('INSERT INTO users (username, name, password, email) VALUES (%s, %s, %s, %s)', (data['username'], data['name'], data['password'], data['email']))
    
        session['username'] = data['username']
        return redirect('/')
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error creating user'})

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('/session/register.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    try:
        with get_db() as db:
            db.execute('SELECT username FROM users WHERE username = %s AND password = %s OR email = %s AND password = %s', (data['username'], data['password'], data['username'], data['password']))
            user = db.fetchone()
        if user:
            session['username'] = data['username']
            response = {
                'message': 'Logged in',
                'username': session['username']
            }
            return jsonify(response)
        else:
            return jsonify({'message': 'Invalid username or password'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error logging in'})

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('/session/login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/denied', methods=['GET'])
def denied():
    return render_template('denied.html', title='Acceso denegado')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        # check if users has admin role in the database
        with get_db() as db:
            db.execute('SELECT role FROM users WHERE username = %s', (session['username'],))
            role = db.fetchone()
        if role and role[0] == 'admin':
            return render_template('admin/dashboard.html')
        else:
            return redirect('/denied')

@app.route('/config_user', methods=['GET'])
def config_user():
    if 'username' in session:
        return render_template('config/config_user.html', title=f'Configuración de {session["username"]}')
    else:
        return redirect('/denied')

if __name__ == '__main__':
    app.run(debug=True, port=8001)