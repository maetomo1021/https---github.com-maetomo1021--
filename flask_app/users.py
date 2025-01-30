from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# サンプルユーザーの作成
users = {
    1: User(1, 'user1', 'password1'),
    2: User(2, 'user2', 'password2')
}

def get_user(user_id):
    return users.get(user_id)

def get_user_by_username(username):
    return next((user for user in users.values() if user.username == username), None)

def add_user(username, password):
    user_id = max(users.keys()) + 1
    users[user_id] = User(user_id, username, password)
    return users[user_id]