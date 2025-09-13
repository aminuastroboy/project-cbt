import streamlit as st
from db import init_db, get_user_by_username, add_user, add_exam, add_question, get_exams, get_questions, save_result
from auth import hash_password, verify_password, encode_face, verify_face

st.set_page_config(page_title="CBT System", layout="wide")

# Initialize database
init_db()

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    camera = st.camera_input("Biometric Login")
    
    if st.button("Login"):
        user = get_user_by_username(username)
        if user and verify_password(password, user[2]):
            if camera:
                if verify_face(camera, user[4]):
                    st.session_state.user = user
                    st.success("Login successful with biometrics")
                else:
                    st.error("Biometric verification failed")
            else:
                st.session_state.user = user
                st.success("Login successful")
        else:
            st.error("Invalid username or password")

def register():
    st.subheader("Register")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    role = st.selectbox("Role", ["student", "examiner", "admin"])
    camera = st.camera_input("Capture Face for Biometric Login")
    
    if st.button("Register"):
        if camera:
            face_encoding = encode_face(camera)
            add_user(username, hash_password(password), role, face_encoding)
            st.success("User registered successfully")
        else:
            st.warning("Please capture your face")

def student_dashboard(user):
    st.title(f"Welcome {user[1]} (Student)")
    exams = get_exams()
    if not exams:
        st.info("No exams available")
        return
    exam = st.selectbox("Choose Exam", [e[1] for e in exams])
    if exam:
        chosen_exam = [e for e in exams if e[1] == exam][0]
        questions = get_questions(chosen_exam[0])
        score = 0
        for q in questions:
            st.write(q[2])
            answer = st.radio("Choose answer", [q[3], q[4], q[5], q[6]], key=q[0])
            if answer == q[7]:
                score += 1
        if st.button("Submit Exam"):
            save_result(user[0], chosen_exam[0], score)
            st.success(f"Exam submitted. Score: {score}/{len(questions)}")

def examiner_dashboard(user):
    st.title(f"Welcome {user[1]} (Examiner)")
    exam_name = st.text_input("Exam Name")
    if st.button("Create Exam"):
        add_exam(exam_name, user[0])
        st.success("Exam created")
    
    exams = get_exams()
    if exams:
        exam = st.selectbox("Choose Exam to Add Questions", [e[1] for e in exams])
        if exam:
            chosen_exam = [e for e in exams if e[1] == exam][0]
            question = st.text_area("Question")
            opt_a = st.text_input("Option A")
            opt_b = st.text_input("Option B")
            opt_c = st.text_input("Option C")
            opt_d = st.text_input("Option D")
            correct = st.selectbox("Correct Answer", [opt_a, opt_b, opt_c, opt_d])
            if st.button("Add Question"):
                add_question(chosen_exam[0], question, opt_a, opt_b, opt_c, opt_d, correct)
                st.success("Question added")

def admin_dashboard(user):
    st.title(f"Welcome {user[1]} (Admin)")
    st.write("Admin dashboard features can be added here")

def main():
    st.sidebar.title("CBT Navigation")
    choice = st.sidebar.radio("Go to", ["Login", "Register", "Dashboard"])

    if choice == "Login":
        login()
    elif choice == "Register":
        register()
    elif choice == "Dashboard":
        if st.session_state.user:
            user = st.session_state.user
            if user[3] == "student":
                student_dashboard(user)
            elif user[3] == "examiner":
                examiner_dashboard(user)
            elif user[3] == "admin":
                admin_dashboard(user)
        else:
            st.warning("Please log in first")

if __name__ == "__main__":
    main()
