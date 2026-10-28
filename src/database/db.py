from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())

def teacher_exists(username):
    response=supabase.table("teacher").select("username").eq("username",username).execute()
    return len(response.data)>0
 


def create_teacher(username,name,passward):
    data={"username":username,"passward":hash_pass(passward),"name":name}
    response=supabase.table("teacher").insert(data).execute()
    return response.data

def teacher_login(username,passward):
    response=supabase.table("teacher").select("*").eq("username",username).execute()
    if response.data:
        teacher=response.data[0]
        if check_pass(passward,teacher['passward']):
            return teacher
    return None


def get_all_students():
    response=supabase.table('student').select("*").execute()
    return response.data
    
def create_student(new_name,face_embedding=None,voice_embedding=None):
    data={'name':new_name,'face_embed':face_embedding,'voice_embed':voice_embedding}
    respone=supabase.table('student').insert(data).execute()
    return respone.data

def create_subject(subject_code,name,section,teacher_id):
    data={'subject_code':subject_code,'name':name,'section':section,'teacher_id':teacher_id}
    response=supabase.table('subject').insert(data).execute()
    return response.data

def get_teacher_subject(teacher_id):
    response=supabase.table('subject').select('*,subject_student(count),attendence(timestamp)').eq('teacher_id',teacher_id).execute()
    subjects=response.data

    for sub in subjects:
        sub['total_students']=sub.get('subject_student',[{}])[0].get('count',0) if sub.get('subject_student') else 0
        attendence=sub.get('attendence',[])
        unique_sessions=len(set(log['timestamp'] for log in attendence))
        sub['total_classes']=unique_sessions

        sub.pop('subject_student',None)
        sub.pop('attendence',None)

    return subjects


def enroll_student_to_subject(studnet_id,subject_id):
    data={'student_id':studnet_id,'subject_id':subject_id}
    response=supabase.table('subject_student').insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id,subject_id):
    response=supabase.table('subject_student').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data


def get_student_subject(student_id):
    response=supabase.table('subject_student').select('*,subject(*)').eq('student_id',student_id).execute()
    return response.data

def get_student_attendence(student_id):
    response=supabase.table('attendence').select('*,subject(*)').eq('student_id',student_id).execute()
    return response.data

def create_attendence(logs):
    response=supabase.table('attendence').insert(logs).execute()
    return response.data


def get_attendence_for_teacher(teacher_id):
    response=supabase.table('attendence').select('*,subject!inner(*)').eq('subject.teacher_id',teacher_id).execute()
    return response.data

