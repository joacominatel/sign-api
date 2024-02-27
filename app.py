import flask, psycopg2, os
from flask import jsonify, request, render_template, redirect, session
from contextlib import contextmanager
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import random
from datetime import datetime

load_dotenv('.env')

app = flask.Flask(__name__)

# Secret key
app.secret_key = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

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
        db.execute('SELECT * FROM tasks WHERE user_id = (SELECT id FROM users WHERE username = %s ORDER BY priority)', (session['username'],))
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
                db.execute('INSERT INTO tasks (user_id, title, description, due_date, priority) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s, %s, %s)', (session['username'], data['title'], data['description'], data['dueDate'], data['priority']))
            else:
                db.execute('INSERT INTO tasks (user_id, title, description, priority) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s, %s)', (session['username'], data['title'], data['description'], data['priority']))

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
            db.execute('INSERT INTO users (username, name, password, email, profile_image_url) VALUES (%s, %s, %s, %s, %s)', (data['username'], data['name'], data['password'], data['email'], '../default-user.webp'))
            db.execute('INSERT INTO user_roles (user_id, role_id) VALUES ((SELECT id FROM users WHERE username = %s), (SELECT id FROM roles WHERE name = %s))', (data['username'], 'user'))
        session['username'] = data['username']
        session['name'] = data['name']
        session['email'] = data['email']
        session['profile_image_url'] = '../default-user.webp'
        session['created_at'] = datetime.now()
        session['updated_at'] = datetime.now()
        session['role'] = 'user'
         
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
            with get_db() as db:
                db.execute('SELECT username, name, profile_image_url, created_at, updated_at, email FROM users WHERE username = %s', (session['username'],))
                data = db.fetchone()
                db.execute('SELECT roles.name FROM roles, user_roles WHERE roles.id = user_roles.role_id AND user_roles.user_id = (SELECT id FROM users WHERE username = %s)', (session['username'],))
                role = db.fetchone()
                response = {
                    'status': 'success',  # Indicate a successful login
                    'message': 'Logged in',
                    'username': data[0],
                    'name': data[1],
                    'profile_image_url': data[2],
                    'created_at': data[3],
                    'updated_at': data[4],
                    'email': data[5],
                    'role': role[0]
                }
                
                session['username'] = data[0]
                session['name'] = data[1]
                session['profile_image_url'] = data[2]
                session['created_at'] = datetime.strftime(data[3], '%Y-%m-%d %H:%M:%S')
                session['updated_at'] = datetime.strftime(data[4], '%Y-%m-%d %H:%M:%S')
                session['email'] = data[5]
                session['role'] = role[0]

                return jsonify(response), 200
        else:
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401  # Use appropriate status code
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': 'Error logging in'}), 500  # Use appropriate status code

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('/session/login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/user/update', methods=['POST'])
def update_user():
    # asegurar que el user este logueado
    if 'username' not in session:
        return redirect('/denied')
    
    data = request.json

    try:
        with get_db() as db:
            db.execute('UPDATE users SET name = %s, email = %s, updated_at = CURRENT_TIMESTAMP WHERE username = %s', (data['name'], data['email'], session['username']))
        session['name'] = data['name']
        session['email'] = data['email']
        return jsonify({'message': 'User updated'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error updating user'})

@app.route('/upload', methods=['POST'])
def upload():
    if 'username' in session:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No file selected'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename + '_' + session['username'] + '_' + str(random.randint(1000, 9999)) + '.png')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            save_image_user_db(session['username'], filename)
            session['profile_image_url'] = filename
            return jsonify({'message': 'File uploaded'})
        else:
            return jsonify({'message': 'Invalid file'})
    else:
        return redirect('/denied')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_image_user_db(username, filename):
    with get_db() as db:
        db.execute('UPDATE users SET profile_image_url = %s WHERE username = %s', (filename, username))

@app.route('/denied', methods=['GET'])
def denied():
    return render_template('denied.html', title='Acceso denegado')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        # check if users has admin role in the database
        with get_db() as db:
            db.execute('SELECT roles.name FROM roles, user_roles WHERE roles.id = user_roles.role_id AND user_roles.user_id = (SELECT id FROM users WHERE username = %s)', (session['username'],))
            role = db.fetchone()
            if role[0] == 'admin':
                return render_template('admin/dashboard.html', title='Dashboard')
            else:
                return redirect('/denied')

@app.route('/config_user', methods=['GET'])
def config_user():
    if 'username' in session:
        return render_template('config/config_user.html', title=f'Configuración de {session["username"]}')
    else:
        return redirect('/denied')
    
@app.route('/groups', methods=['GET'])
def groups():
    groups = []
    if 'username' in session:
        with get_db() as db:
            db.execute('SELECT * FROM groups WHERE owner_id = (SELECT id FROM users WHERE username = %s)', (session['username'],))
            groups = db.fetchall()
            # total tasks of a group
            total_tasks = []
            total_members = []
            user_id = []

            # get total tasks and total members of each group
            for group in groups:
                db.execute('SELECT COUNT(*) FROM tasks WHERE group_id = %s', (group[0],))
                total_tasks.append(db.fetchone()[0])
                
                db.execute('SELECT COUNT(*) FROM group_members WHERE group_id = %s', (group[0],))
                total_members.append(db.fetchone()[0])

                db.execute('SELECT id FROM users WHERE username = %s', (session['username'],))
                user_id.append(db.fetchone()[0])

        return render_template('groups/groups.html', groups=groups, total_tasks=total_tasks, total_members=total_members, user_id=user_id)
    else:
        return redirect('/denied')
    
@app.route('/groups/create', methods=['POST'])
def create_group():

    """
    CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE group_members (
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (group_id, user_id)
    );
    """
    data = request.json

    try:
        with get_db() as db:
            db.execute('INSERT INTO groups (name, description, owner_id) VALUES (%s, %s, (SELECT id FROM users WHERE username = %s))', (data['name'], data['description'], session['username']))
            db.execute('INSERT INTO group_members (group_id, user_id) VALUES ((SELECT id FROM groups WHERE name = %s), (SELECT id FROM users WHERE username = %s))', (data['name'], session['username']))
        return jsonify({'message': 'Group created'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error creating group'})

@app.route('/groups/create', methods=['GET'])
def create_group_form():
    return render_template('groups/create.html')

@app.route('/groups/<int:group_id>', methods=['GET'])
def group(group_id):
    group = {}
    if 'username' in session:
        with get_db() as db:
            db.execute('SELECT * FROM groups, group_members WHERE groups.id = group_members.group_id AND groups.id = %s AND group_members.user_id = (SELECT id FROM users WHERE username = %s)', (group_id, session['username']))
            group = db.fetchone()
            members = []
            db.execute('SELECT username, profile_image_url FROM users, group_members WHERE users.id = group_members.user_id AND group_members.group_id = %s', (group_id,))
            members = db.fetchall()
            tasks = []
            db.execute('SELECT * FROM tasks WHERE group_id = %s', (group_id,))
            tasks = db.fetchall()

        return render_template('groups/group.html', group=group, members=members, tasks=tasks)
    else:
        return redirect('/denied')

@app.route('/groups/<int:group_id>/add_member', methods=['POST'])
def add_member(group_id):
    data = request.json
    try:
        with get_db() as db:
            db.execute('INSERT INTO group_members (group_id, user_id) VALUES (%s, (SELECT id FROM users WHERE username = %s))', (group_id, data['username']))
        return jsonify({'message': 'Member added'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error adding member'})
    
@app.route('/search_users', methods=['GET'])
def search_users():
    username_query = request.args.get('username', '')
    group_id = request.args.get('group_id', None)
    users = []
    if 'username' in session:
        with get_db() as db:
            # Modifica esta consulta para que también verifique si el usuario ya es miembro del grupo
            query = """
            SELECT users.username, users.profile_image_url, 
                   CASE WHEN group_members.user_id IS NULL THEN FALSE ELSE TRUE END as is_member
            FROM users
            LEFT JOIN group_members ON users.id = group_members.user_id AND group_members.group_id = %s
            WHERE users.username ILIKE %s AND users.username != %s
            """
            db.execute(query, (group_id, f'%{username_query}%', session['username']))
            users = db.fetchall()
        return jsonify(users)
    else:
        return redirect('/denied')
    
@app.route('/groups/<int:group_id>/edit_group', methods=['POST'])
def edit_group(group_id):
    data = request.json
    try:
        with get_db() as db:
            db.execute('UPDATE groups SET name = %s, description = %s WHERE id = %s', (data['name'], data['description'], group_id))
        return jsonify({'message': 'Group updated'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error updating group'})

if __name__ == '__main__':
    app.run(debug=True, port=8001)