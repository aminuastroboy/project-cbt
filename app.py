# app.py — Streamlit CBT with Biometric Verification
import streamlit as st
from db import (
    init_db, get_user_by_email, email_exists, save_user,
    create_exam, get_exams, add_question, get_questions,
    save_result, get_results_for_user
)
from auth import (
    hash_password, verify_password,
    capture_face_streamlit, encode_face, verify_biometric
)

st.set_page_config(page_title="CBT with Biometrics", layout="wide")
init_db()

if "user" not in st.session_state:
    st.session_state["user"] = None

def require_login():
    if st.session_state["user"] is None:
        st.warning("Please log in first from the sidebar.")
        st.stop()

def page_login():
    st.header("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    snap = capture_face_streamlit("Capture your face to login (biometric verification)")

    if st.button("Login"):
        user = get_user_by_email(email)
        if not user:
            st.error("User not found ❌"); return
        if not verify_password(password, user["password_hash"]):
            st.error("Invalid password ❌"); return
        if snap is None:
            st.error("No image captured for biometric verification ❌"); return
        live_encoding = encode_face(snap)
        if live_encoding is None:
            st.error("No face detected ❌"); return
        if not user["biometric_template"]:
            st.error("User has no biometric template on file."); return
        if verify_biometric(live_encoding, user["biometric_template"]):
            st.success(f"Welcome {user['first_name']} {user['last_name']}! ✅")
            st.session_state["user"] = dict(user)
        else:
            st.error("Biometric verification failed ❌")

def page_register():
    st.header("📝 Register")
    cols = st.columns(2)
    with cols[0]:
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["student", "admin", "invigilator"])
    with cols[1]:
        password = st.text_input("Password", type="password")
        password2 = st.text_input("Confirm Password", type="password")

    snap = capture_face_streamlit("Capture your face to enroll (biometric template)")

    if st.button("Register"):
        if not fname or not lname or not email or not password:
            st.error("All fields are required."); return
        if password != password2:
            st.error("Passwords do not match."); return
        if email_exists(email):
            st.error("Email already registered."); return
        if snap is None:
            st.error("No image captured for biometric template."); return
        enc = encode_face(snap)
        if enc is None:
            st.error("No face detected in the captured image."); return
        pw_hash = hash_password(password)
        save_user(fname, lname, email, role, pw_hash, enc, biometric_type="face")
        st.success("Registration complete ✅ You can now log in.")

def admin_dashboard(user):
    st.subheader("⚙️ Admin Dashboard")
    tab1, tab2, tab3 = st.tabs(["Create Exam", "Add Question", "View Exams & Questions"])
    with tab1:
        exam_name = st.text_input("Exam Name", key="exam_name")
        if st.button("Save Exam", key="save_exam_btn"):
            if exam_name.strip() == "":
                st.error("Exam name is required.")
            else:
                exam_id = create_exam(exam_name, user["user_id"])
                st.success(f"Exam '{exam_name}' created ✅ (ID: {exam_id})")
    with tab2:
        exams = get_exams()
        if not exams:
            st.info("No exams found. Create an exam first.")
        else:
            exam_map = {e["exam_name"]: e["exam_id"] for e in exams}
            choice = st.selectbox("Select Exam", list(exam_map.keys()), key="exam_select_for_q")
            q_text = st.text_area("Question Text")
            colA, colB = st.columns(2)
            with colA:
                option_a = st.text_input("Option A")
                option_b = st.text_input("Option B")
            with colB:
                option_c = st.text_input("Option C")
                option_d = st.text_input("Option D")
            correct = st.selectbox("Correct Option", ["A","B","C","D"])
            if st.button("Save Question", key="save_q_btn"):
                if not q_text or not option_a or not option_b or not option_c or not option_d:
                    st.error("All fields are required for a question.")
                else:
                    add_question(exam_map[choice], q_text, option_a, option_b, option_c, option_d, correct)
                    st.success("Question added ✅")
    with tab3:
        exams = get_exams()
        if not exams:
            st.info("No exams found.")
        else:
            for e in exams:
                st.markdown(f"### 📘 {e['exam_name']} (ID: {e['exam_id']})")
                qs = get_questions(e["exam_id"])
                if not qs:
                    st.write("_No questions yet._")
                else:
                    for q in qs:
                        st.markdown(f"- **Q{q['question_id']}**: {q['question_text']}  \n"
                                    f" A) {q['option_a']}  \n B) {q['option_b']}  \n"
                                    f" C) {q['option_c']}  \n D) {q['option_d']}  \n"
                                    f"✅ Correct: **{q['correct_option']}**")

def student_dashboard(user):
    st.subheader("🎓 Student Dashboard")
    exams = get_exams()
    if not exams:
        st.info("No exams available yet."); return
    exam_map = {e["exam_name"]: e["exam_id"] for e in exams}
    choice = st.selectbox("Select Exam", list(exam_map.keys()), key="student_exam_select")
    exam_id = exam_map[choice]
    if st.button("Start Exam", key="start_exam_btn"):
        st.session_state["current_exam"] = exam_id
    if st.session_state.get("current_exam") == exam_id:
        st.markdown(f"### 📝 {choice}")
        qs = get_questions(exam_id)
        if not qs:
            st.info("No questions in this exam yet."); return
        answers = {}
        for q in qs:
            answers[q["question_id"]] = st.radio(
                f"Q{q['question_id']}: {q['question_text']}",
                ["A","B","C","D"], key=f"ans_{q['question_id']}"
            )
        if st.button("Submit Exam", key="submit_exam_btn"):
            score = save_result(user["user_id"], exam_id, answers)
            st.success(f"Submitted ✅ Your score: {score}%")
            st.session_state.pop("current_exam", None)
    st.markdown("### 📊 Your Results")
    res = get_results_for_user(user["user_id"])
    if res:
        for r in res:
            st.write(f"- {r['exam_name']}: **{r['score']}%** on {r['taken_at']}")
    else:
        st.write("_No results yet._")

def invigilator_dashboard(user):
    st.subheader("🕵️ Invigilator Dashboard")
    st.info("Monitoring module placeholder — integrate live sessions & periodic biometric checks here.")

def page_dashboard():
    if st.session_state["user"] is None:
        st.warning("Please log in first from the sidebar."); return
    user = st.session_state["user"]
    st.header(f"📊 Dashboard — {user['first_name']} {user['last_name']}")
    st.caption(f"Role: {user['role']}")
    if user["role"] == "admin":
        admin_dashboard(user)
    elif user["role"] == "student":
        student_dashboard(user)
    else:
        invigilator_dashboard(user)

st.sidebar.title("📚 CBT with Biometric Verification")
page = st.sidebar.radio("Navigate", ["Login", "Register", "Dashboard"])
if st.sidebar.button("Logout") and st.session_state["user"]:
    st.session_state["user"] = None
    st.experimental_rerun()

if page == "Login":
    page_login()
elif page == "Register":
    page_register()
else:
    page_dashboard()
