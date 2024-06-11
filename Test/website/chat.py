from flask import Blueprint, render_template, request, session, redirect
from flask_login import login_required, current_user
from . import socketio
from flask_socketio import emit, join_room, leave_room

chat_function = Blueprint('chat', __name__)

# Store the connected clients (users and admins)
users = {}
admins = {}
# Store the chat messages
chat_history = {}

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    assign_admin = data['admin'] 

    join_room(room)

    # Store the user and assigned admin in its respective dictionaries
    users[username] = room
    admins[assign_admin] = room

    # Check if the user is an admin
    is_admin = current_user.is_admin 

    if not chat_history.get(room):
        emit('user_joined', {'username': username, 'isAdmin': is_admin}, room=room)
    else:
        # Send the chat_history to the newly joined user
        emit('chat_history', chat_history[room], room=request.sid)

    emit('new_admin', is_admin, room=room)

@socketio.on('message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = users.get(username)

    is_admin = current_user.is_admin

    # Store the message in the chat_history
    if not chat_history.get(room):
        chat_history[room] = []
    chat_history[room].append({'username': username, 'message': message, 'isAdmin': is_admin})

    emit('new_message', {'username': username, 'message': message, 'isAdmin': is_admin}, room=room)

@socketio.on('disconnect')
def handle_disconnect():
    username = current_user.username
    room = users.get(username)

    if room:
        leave_room(room)

        # Delete the user from the user dictionary
        del users[username]

        # Check if the user was assigned an admin
        if username in admins:
            admin = admins[username]
            emit('admin_left', {'admin': admin}, room=room)

            # Remove the admin from the admin dictionary
            del admins[username]

@chat_function.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    username = current_user.username

    # Check if the user is assigned an admin
    if username in admins:
        admin = admins[username]
    else:
        admin = None

    return render_template('chat.html', user=current_user, username=username, admin=admin)
