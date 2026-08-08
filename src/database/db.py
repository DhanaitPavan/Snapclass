from src.database.config import supabase
import bcrypt

def hash_pass(password):
    # Hash the password using bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
def check_pass(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def check_teacher_exist(username):
    #Check for unique username , return false if username is already taken 
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0 # If the length of the response data is greater than 0, it means the username already exists, so return True., return False.

def create_teacher(username, password, name):
     data = {"username": username, "password":hash_pass(password), "name": name}
     response = supabase.table("teachers").insert(data).execute()
     return response.data

def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None