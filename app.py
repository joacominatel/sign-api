# GENERALES 
import flask, os
from flask import jsonify, request, render_template, redirect, session
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

# MODELOS
from backend.db import init_app, db
from backend.models.User import User
from backend.models.UserRoles import UserRoles
from backend.models.Tasks import Task
from backend.models.Groups import Group
from backend.models.Roles import Roles
from backend.models.GroupMembers import GroupMembers
from backend.models.GroupPosts import GroupPosts
from backend.models.PostUpVotes import PostUpVotes
from backend.models.GroupTasks import GroupTasks

# SQLALCHEMY
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, aliased
from sqlalchemy.sql import func, exists, and_, or_

load_dotenv('.env')

app = flask.Flask(__name__)

# Secret key
app.secret_key = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = os.environ['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = init_app(app)

# Main page
@app.route('/', methods=['GET'])
def main():
    if 'username' in session:
        # get all data of last tasks of user
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            return redirect('/errors/denied')
        
        tasks = Task.query.filter_by(user_id=user.id).order_by(Task.priority).all()
        return render_template('index.html', tasks=tasks)
    else:
        return render_template('index.html')
    
@app.route('/home', methods=['GET'])
def home():
    return redirect('/')


@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    tasks = Task.query.filter_by(user_id=user.id).order_by(Task.priority).all()

    tasks_data = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'priority': task.priority,
        'completed': task.completed
    } for task in tasks]

    return jsonify(tasks_data), 200

@app.route('/complete_task', methods=['POST'])
def complete_task():
    data = request.json
    print(data)

    if 'username' not in session:
        return jsonify({'message': 'No user logged in'}), 401
    
    task = Task.query.get(data['taskId'])
    print(task)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    try:
        task.completed = data['completed']
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error updating task'}), 500

@app.route('/delete_task', methods=['POST'])
def delete_task():
    data = request.json

    task = Task.query.get(data['taskId'])
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error deleting task'}), 500

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'username' not in session:
        return jsonify({'message': 'No user logged in'}), 401

    data = request.json
    try:
        # Busca el usuario en la base de datos
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Crea la nueva tarea
        new_task = Task(
            user_id=user.id,
            title=data['title'],
            description=data['description'],
            due_date=data.get('dueDate'),  # get retornará None si 'dueDate' no está presente
            priority=data['priority'],
            completed=False,  # Asume que la tarea no está completada al crearse
        )

        # Añade la tarea a la base de datos
        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task added successfully'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': 'Error adding task'}), 500


@app.route('/tasks', methods=['GET'])
def tasks():
    # get all data of tasks of user
    if 'username' not in session:
        return redirect('/errors/denied')
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return redirect('/errors/denied')
    
    tasks = Task.query.filter_by(user_id=user.id).order_by(Task.priority).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/register', methods=['POST'])
def register():
    data = request.json

    # validan los datos
    if not data['username'] or not data['password'] or not data['name'] or not data['email']:
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400
    
    hashed_password = generate_password_hash(data['password'])

    new_user = User(
        username=data['username'],
        name=data['name'],
        password=hashed_password,
        email=data['email'],
        profile_image_url='../default-user.webp',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    try:
        db.session.add(new_user)
        db.session.flush()

        # Asigna el rol de usuario a la nueva cuenta
        new_user_role = UserRoles(user_id=new_user.id, role_id=2)
        db.session.add(new_user_role)

        db.session.commit()

        # configurar la nueva sesion del usuario
        session['username'] = data['username']
        session['name'] = data['name']
        session['email'] = data['email']
        session['profile_image_url'] = '../default-user.webp'
        session['created_at'] = datetime.strftime(new_user.created_at, '%Y-%m-%d %H:%M:%S')
        session['updated_at'] = datetime.strftime(new_user.updated_at, '%Y-%m-%d %H:%M:%S')
        session['role'] = 'user'

        return jsonify({'status': 'success', 'message': 'User registered'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'status': 'error', 'message': 'Error registering user'}), 500

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('/session/register.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'All fields are required'}), 400
    
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session['username'] = user.username
        session['name'] = user.name
        session['profile_image_url'] = user.profile_image_url
        session['created_at'] = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
        session['updated_at'] = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
        session['email'] = user.email

        # get user roles
        user_roles = db.session.query(Roles).join(UserRoles, Roles.id == UserRoles.role_id).filter(UserRoles.user_id == user.id).all()
        roles = [role.name for role in user_roles]
        session['role'] = roles[0]

        response = {
            'status': 'success',
            'message': 'User logged in',
            'username': user.username,
            'name': user.name,
            'profile_image_url': user.profile_image_url,
            'created_at': datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S'),
            'email': user.email,
            'role': roles[0]
        }
        return jsonify(response), 200
    return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
    

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('/session/login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    session.pop('name', None)
    session.pop('email', None)
    session.pop('profile_image_url', None)
    session.pop('created_at', None)
    session.pop('updated_at', None)
    session.pop('role', None)
    return redirect('/')

@app.route('/user/update', methods=['POST'])
def update_user():
    # asegurar que el user este logueado
    if 'username' not in session:
        return redirect('/errors/denied')
    
    data = request.json

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    try:
        user.name = data['name']
        user.email = data['email']
        user.updated_at = datetime.now()

        db.session.commit()

        session['name'] = user.name
        session['email'] = user.email
        session['updated_at'] = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')

        return jsonify({'message': 'User updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))
        return jsonify({'message': 'Error updating user'}), 500

@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect('/errors/denied')
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # change the name of the file to the username
        filename = f'{session["username"]}_{filename}.png'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        save_image_user_db(session['username'], filename)
        session['profile_image_url'] = f'{filename}'
        
        return jsonify({'message': 'File uploaded'}), 200
    
    return jsonify({'message': 'File not allowed'}), 400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def save_image_user_db(username, filename):
    try:
        user = User.query.filter_by(username=username).first()
        user.profile_image_url = f'{filename}'
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))


@app.route('/errors/denied', methods=['GET'])
def denied():
    return render_template('errors/denied.html', title='Acceso denegado')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect('/errors/denied')        

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return redirect('/errors/denied')
    
    # get user roles
    user_roles = db.session.query(Roles).join(UserRoles, Roles.id == UserRoles.role_id).filter(UserRoles.user_id == user.id).all()
    roles = [role.name for role in user_roles]

    if 'admin' in roles:
        #if admin
        recent_user = User.query.order_by(User.created_at.desc()).limit(5).all()
        total_users = db.session.query(func.count(User.id)).scalar()
        total_tasks = db.session.query(func.count(Task.id)).scalar()
        total_groups = db.session.query(func.count(Group.id)).scalar()
        total_roles = db.session.query(func.count(Roles.id)).scalar()

        # render dashboard
        return render_template(
            'admin/dashboard.html',
            title='Dashboard',
            users=recent_user,
            total_users=total_users,
            total_tasks=total_tasks,
            total_groups=total_groups,
            total_roles=total_roles
        )
    else:
        # if user
        return render_template('errors/denied.html', title='Acceso denegado')

@app.route('/config_user', methods=['GET'])
def config_user():
    if not 'username' in session:
        return redirect('/errors/denied')
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return redirect('/errors/denied')
    
    return render_template('config/config_user.html', title='Configuración de usuario', user=user)

    
@app.route('/groups', methods=['GET'])
def groups():
    if 'username' not in session:
        return redirect('/errors/denied')

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return redirect('/errors/denied')

    # Obtener grupos y cargar miembros y tareas con 'joinedload' para eficiencia
    user_groups = db.session.query(Group).join(GroupMembers).options(
        joinedload(Group.tasks)
    ).filter(GroupMembers.user_id == user.id).all()

    groups_data = []
    for group in user_groups:
        total_members = db.session.query(func.count(GroupMembers.id)).filter(GroupMembers.group_id == group.id).scalar()
        total_tasks = db.session.query(
            func.count(GroupTasks.id)
        ).filter(GroupTasks.group_id == group.id).scalar()
        groups_data.append({
            'group': group,
            'total_members': total_members,
            'total_tasks': total_tasks,
            'owner': group.owner_id == user.id,
        })

    return render_template('groups/groups.html',
                            groups=groups_data, 
                            user_id=user.id)
    
@app.route('/groups/create', methods=['POST'])
def create_group():
    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    data = request.json
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        new_group = Group(name=data['name'], description=data['description'], owner_id=user.id)
        db.session.add(new_group)
        db.session.flush()  # Flush to get the new group ID without committing

        # Automatically add the creator as a member of the group
        new_member = GroupMembers(group_id=new_group.id, user_id=user.id)
        db.session.add(new_member)
        
        db.session.commit()
        return jsonify(
            {
                'message': 'Group created',
                'group_id': new_group.id,
                'group_name': new_group.name
            }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error creating group'}), 500
    

@app.route('/groups/create', methods=['GET'])
def create_group_form():
    return render_template('groups/create.html')

@app.route('/groups/<int:group_id>', methods=['GET'])
def group(group_id):
    if 'username' not in session:
        return redirect('/errors/denied')

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': 'Group not found'}), 404

    # Verificar si el usuario es miembro del grupo
    is_member = GroupMembers.query.filter_by(group_id=group_id, user_id=user.id).first()
    if not is_member:
        return jsonify({'message': 'Access denied'}), 403

    try:
        members = User.query.join(GroupMembers, User.id == GroupMembers.user_id).filter(GroupMembers.group_id == group_id).all()
        tasks = GroupTasks.query.filter_by(group_id=group_id).join(Task, Task.id == GroupTasks.task_id).all()
        # get task_id from group_tasks
        task_id = [task.task_id for task in tasks]
        tasks = Task.query.filter(Task.id.in_(task_id)).all()
        user_tasks = Task.query.filter(Task.user_id == user.id, or_(Task.group_id != group_id, Task.group_id == None)).all()
        posts = GroupPosts.query.filter_by(group_id=group_id).all()
        
        upvotes = []
        for post in posts:
            count = PostUpVotes.query.filter_by(post_id=post.id).count()
            upvotes.append(count)
        
        # Aquí debes convertir los objetos a un formato adecuado para jsonify
        group_details = {
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'owner_id': group.owner_id
        }

        members_details = []
        for member in members:
            members_details.append({
                'id': member.id,
                'username': member.username,
                'name': member.name,
                'profile_image_url': member.profile_image_url
            })

        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'priority': task.priority,
                'completed': task.completed,
                'user_id': task.user_id
            })

        user_tasks_details = []
        for task in user_tasks:
            user_tasks_details.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'priority': task.priority,
                'completed': task.completed,
                'user_id': task.user_id,
                'group_id': task.group_id
            })

        posts_details = []
        for post in posts:
            posts_details.append({
                'id': post.id,
                'user_id': post.user_id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'updated_at': post.updated_at
            })

        return render_template('groups/group.html',
                               group=group_details,
                               members=members_details,
                               tasks=tasks_data,
                               user_tasks=user_tasks_details,
                               posts=posts_details,
                               upvotes=upvotes,
                               user_id=user.id
                               )
    except Exception as e:
        print(e)
        return jsonify({'message': 'Error getting group details'}), 500
    
@app.route('/groups/<int:group_id>/delete', methods=['POST'])
def delete_group(group_id):
    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    group = Group.query.get(group_id)
    print(group)
    if not group:
        return jsonify({'message': 'Group not found'}), 404

    # Verificar si el usuario es el dueño del grupo
    if group.owner_id != user.id:
        return jsonify({'message': 'Access denied'}), 403

    try:
        # get all members of the group
        members = GroupMembers.query.filter_by(group_id=group_id).all()
        for member in members:
            db.session.delete(member)

        db.session.delete(group)
        db.session.commit()
        return jsonify({'message': 'Group deleted'}), 200
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error deleting group'}), 500

    
@app.route('/groups/<int:group_id>/leave', methods=['POST'])
def leave_group(group_id):
    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Verificar si el grupo existe
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': 'Group not found'}), 404

    # Verificar si el usuario es miembro del grupo
    is_member = GroupMembers.query.filter_by(group_id=group_id, user_id=user.id).first()
    if not is_member:
        return jsonify({'message': 'Access denied'}), 403
    
    # verificar si es el dueño del grupo
    if group.owner_id == user.id:
        return jsonify({'message': 'Owner cannot leave group'}), 403
    
    # hacer un post en el grupo que el usuario se fue
    try:
        new_post = GroupPosts(group_id=group_id, user_id=user.id, title=f'{user.username} se ha ido del grupo', content=f'{user.username} se ha ido del grupo', created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(new_post)
        db.session.flush()  # Esto permite usar el ID del post antes de hacer commit

        # Añadir automáticamente un upvote del usuario al post
        upvote = PostUpVotes(post_id=new_post.id, user_id=user.id)
        db.session.add(upvote)

        db.session.delete(is_member)
        db.session.commit()
        return jsonify({'message': 'Left group'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error leaving group'}), 500


@app.route('/groups/<int:group_id>/add_member', methods=['POST'])
def add_member(group_id):
    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    data = request.json
    user_to_add = User.query.filter_by(username=data['username']).first()
    if not user_to_add:
        return jsonify({'message': 'User not found'}), 404

    # Verificar si el grupo existe
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': 'Group not found'}), 404

    # Verificar si el usuario ya es miembro del grupo
    existing_member = GroupMembers.query.filter_by(group_id=group_id, user_id=user_to_add.id).first()
    if existing_member:
        return jsonify({'message': 'User already a member'}), 409

    try:
        new_member = GroupMembers(group_id=group_id, user_id=user_to_add.id)
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Member added'}), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error adding member'}), 500
    
@app.route('/groups/<int:group_id>/delete_member', methods=['POST'])
def delete_member(group_id):
    data = request.json

    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401
    
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Verificar si el grupo existe
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': 'Group not found'}), 404
    
    # Verificar si el usuario es miembro del grupo
    is_member = GroupMembers.query.filter_by(group_id=group_id, user_id=user.id).first()
    if not is_member:
        return jsonify({'message': 'Access denied'}), 403
    
    # Verificar si el usuario a eliminar es miembro del grupo
    member_to_delete = GroupMembers.query.filter_by(group_id=group_id, user_id=data['userId']).first()
    if not member_to_delete:
        return jsonify({'message': 'User not a member'}), 404
    
    try:
        db.session.delete(member_to_delete)
        db.session.commit()
        return jsonify({'message': 'Member deleted'}), 200
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error deleting member'}), 500
    
    
@app.route('/search_users', methods=['GET'])
def search_users():
    if 'username' not in session:
        return redirect('/errors/denied')

    username_query = request.args.get('username', '')
    group_id = request.args.get('group_id', None)

    # Crear un alias para group_members para facilitar la consulta de membresía
    member_alias = aliased(GroupMembers)

    # Filtrar usuarios por criterio de búsqueda y excluir al usuario actual de los resultados
    query = db.session.query(
        User.username,
        User.profile_image_url,
        User.id.notin_(
            db.session.query(member_alias.user_id)
            .filter(member_alias.group_id == group_id)
        ).label('is_member')
    ).filter(
        User.username.ilike(f"%{username_query}%"),
        User.username != session['username']
    )

    # Ajustar la consulta si se proporciona group_id
    if group_id:
        query = query.outerjoin(GroupMembers, and_(GroupMembers.user_id == User.id, GroupMembers.group_id == group_id))
    else:
        query = query.limit(5)  # Limitar los resultados si no se busca dentro de un grupo específico

    users = query.all()

    # format results
    users_data = [{
        'username': user.username,
        'profile_image_url': user.profile_image_url,
        'is_member': not user.is_member
    } for user in users]

    return jsonify(users_data), 200
    
@app.route('/groups/<int:group_id>/edit_group', methods=['POST'])
def edit_group(group_id):
    data = request.json
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': 'Group not found'}), 404
    
    try:
        group.name = data['groupName']
        group.description = data['groupDescription']
        db.session.commit()
        return jsonify({'message': 'Group updated'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error updating group'})
    
@app.route('/groups/<int:group_id>/edit_group', methods=['GET'])
def edit_group_form(group_id):
    if 'username' not in session:
        return redirect('/errors/denied')

    group = Group.query.get(group_id)

    if not group:
        return render_template('errors/404.html', title='Grupo no encontrado', content='El grupo que buscas no existe', error_number='404')
    
    return render_template('groups/edit_group.html', title=f'Editar {group.name}', group=group)

@app.route('/groups/<int:group_id>/add_task', methods=['POST'])
def add_task_to_group(group_id):
    data = request.json
    task = Task.query.get(data['taskId'])

    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    try:
        new_group_task = GroupTasks(group_id=group_id, task_id=task.id)
        db.session.add(new_group_task)
        db.session.commit()
        return jsonify({'message': 'Task added to group'}), 200
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error adding task to group'}), 500
    
@app.route('/profile/<username>/', methods=['GET'])
def profile(username):
    if 'username' not in session:
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template('errors/user_not_found.html', title='Usuario no encontrado')
    
    # current user is admin?
    if session['role'] == 'admin':
        is_admin = True
    else:
        is_admin = False

    total_tasks = db.session.query(func.count(Task.id)).filter(Task.user_id == user.id).scalar()
    completed_tasks = db.session.query(func.count(Task.id)).filter(Task.user_id == user.id, Task.completed == True).scalar()
    pending_tasks = db.session.query(func.count(Task.id)).filter(Task.user_id == user.id, Task.completed == False).scalar()

    user_data = {
        'username': user.username,
        'name': user.name,
        'profile_image_url': user.profile_image_url,
        'created_at': user.created_at,
        'email': user.email
    }

    return render_template(
        'profile.html',
        title=f'Perfil de {user.username}', 
        total_tasks=total_tasks, 
        completed_tasks=completed_tasks, 
        pending_tasks=pending_tasks, 
        user=user_data,
        is_admin=is_admin)

@app.route('/groups/<int:group_id>/posts', methods=['POST'])
def add_post(group_id):
    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    data = request.json
    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        # Crear y añadir el post al grupo
        new_post = GroupPosts(group_id=group_id, user_id=user.id, title=data['title'], content=data['content'], created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(new_post)
        db.session.flush()  # Esto permite usar el ID del post antes de hacer commit

        # Añadir automáticamente un upvote del usuario al post
        upvote = PostUpVotes(post_id=new_post.id, user_id=user.id)
        db.session.add(upvote)

        db.session.commit()
        return jsonify({'message': 'Post added'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error adding post'}), 500

@app.route('/groups/posts/<int:post_id>/upvote', methods=['POST'])
def upvote_post(post_id):
    if 'username' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user = User.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    post = GroupPosts.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    # Verifica si el usuario ya ha votado este post
    existing_upvote = PostUpVotes.query.filter_by(post_id=post_id, user_id=user.id).first()
    if existing_upvote:
        return jsonify({'message': 'User has already upvoted this post'}), 409

    try:
        new_upvote = PostUpVotes(post_id=post_id, user_id=user.id)
        db.session.add(new_upvote)
        db.session.commit()
        return jsonify({'message': 'Post upvoted'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error upvoting post'}), 500
    
@app.route('/profile/<username>/give_admin', methods=['POST'])
def give_admin(username):
    if session['role'] != 'admin':
        return jsonify({'message': 'Access denied'}), 403

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        new_user_role = UserRoles(user_id=user.id, role_id=1)
        db.session.add(new_user_role)
        db.session.commit()
        return jsonify({'message': 'Admin role given'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Error giving admin role'}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', page_title='Página no encontrada', content='La página que buscas no existe', error_number='404'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/404.html', page_title='Error interno', content='Ha ocurrido un error interno en el servidor', error_number='500'), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('errors/404.html', page_title='Método no permitido', content='El método que intentas usar no está permitido', error_number='405'), 405

if __name__ == '__main__':
    app.run(debug=True, port=8001)