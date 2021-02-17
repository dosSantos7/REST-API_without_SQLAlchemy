from models.user import UserModel


# returns the user if the password is correct, else None
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


# identifies the user based of the user_id retrieved from payload
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
