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

def get_all_students():
    response=supabase.table('students').select("*").execute()
    return response.data

def create_student(new_name, face_embedding=None, voice_embedding=None):
    data={'name':new_name, 'face_embedding':face_embedding, 'voice_embedding':voice_embedding}
    response=supabase.table('students').insert(data).execute()
    return response.data

def create_subject(subject_code, name, section, teacher_id):
    data={"subject_code":subject_code, "name":name, "section":section, "teacher_id":teacher_id}
    response=supabase.table('subjects').insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response=supabase.table('subjects').select("*, subject_students(count), attendence_log(timestamps)").eq("teacher_id", teacher_id).execute()
    subjects=response.data

    for sub in subjects:
        sub['total_student']=sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subjects_student') else 0
        attendance=sub.get('attendence_log', [])
        unique_sessions=len(set(log['timestamps'] for log in attendance))
        sub['total_classes']=unique_sessions


        sub.pop('subject_students', None)
        sub.pop('attendence_log', None)

    return subjects