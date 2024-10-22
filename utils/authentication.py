def authenticate_user(role, password):
    credentials = {
        'your credentials'
    }
    
    if role in credentials and credentials[role] == password:
        return True
    return False
