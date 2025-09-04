import streamlit as st

# Session state setup
if "user" not in st.session_state:
    st.session_state["user"] = None
if "users" not in st.session_state:
    st.session_state["users"] = []
if "exams" not in st.session_state:
    st.session_state["exams"] = []

st.set_page_config(page_title="CBT with Biometrics", layout="wide")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------
# LOGIN
# -------------------
if choice == "Login":
    st.subheader("🔑 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = next((u for u in st.session_state["users"] if u["email"] == email and u["password"] == password), None)
        if user:
            st.session_state["user"] = user
            st.success(f"Welcome {user['first_name']} ({user['role']})")
        else:
            st.error("Invalid credentials")

# -------------------
# REGISTER
# -------------------
elif choice == "Register":
    st.subheader("📝 Register")
    first = st.text_input("First Name")
    last = st.text_input("Last Name")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["student", "admin", "invigilator"])
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        st.session_state["users"].append({
            "first_name": first,
            "last_name": last,
            "email": email,
            "password": password,
            "role": role
        })
        st.success("User registered ✅")

# -------------------
# DASHBOARDS
# -------------------
if st.session_state["user"]:
    role = st.session_state["user"]["role"]

    # Admin dashboard
    if role == "admin":
        st.header("⚙️ Admin Dashboard")
        exam_title = st.text_input("Exam Title")
        q_text = st.text_area("Question")
        options = st.text_input("Options (comma-separated)")
        correct = st.text_input("Correct Answer")
        if st.button("Add Question"):
            if not any(e["title"] == exam_title for e in st.session_state["exams"]):
                st.session_state["exams"].append({"title": exam_title, "questions": []})
            exam = next(e for e in st.session_state["exams"] if e["title"] == exam_title)
            exam["questions"].append({
                "q": q_text,
                "options": [o.strip() for o in options.split(",")],
                "answer": correct.strip()
            })
            st.success(f"Added Q to {exam_title}")

        st.subheader("Existing Exams")
        for exam in st.session_state["exams"]:
            st.write(f"📘 {exam['title']} ({len(exam['questions'])} questions)")

    # Student dashboard
    elif role == "student":
        st.header("🎓 Student Dashboard")
        if not st.session_state["exams"]:
            st.info("No exams available yet.")
        else:
            exam_titles = [e["title"] for e in st.session_state["exams"]]
            selected = st.selectbox("Select Exam", exam_titles)
            exam = next(e for e in st.session_state["exams"] if e["title"] == selected)

            st.subheader(f"Exam: {exam['title']}")
            answers = {}
            for i, q in enumerate(exam["questions"], 1):
                st.write(f"**Q{i}. {q['q']}**")
                ans = st.radio(f"Answer {i}", q["options"], key=f"q{i}")
                answers[i] = ans

            if st.button("Submit Exam"):
                score = sum(1 for i, q in enumerate(exam["questions"], 1) if answers[i] == q["answer"])
                total = len(exam["questions"])
                st.success(f"Your Score: {score}/{total}")

    # Invigilator dashboard
    elif role == "invigilator":
        st.header("🕵️ Invigilator Dashboard")
        st.info("Here invigilators can monitor exams (future feature).")
