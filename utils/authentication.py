def authenticate_user(role, password):
    credentials = {
        'Admin': 'admin123',
        'Receptionist': 'recep123',
        'Head Nurse': 'nurse123',
        'Accountant': 'account123',
        'Services Coordinator': 'service123'
    }
    
    if role in credentials and credentials[role] == password:
        return True
    return False
