import streamlit as st
import re

class User:
    def __init__(self, user_id, password, role):
        self.user_id = user_id
        self.password = password
        self.role = role
        self.attendance_records = []
        self.leave_requests = []

class AttendanceSystem:
    def __init__(self):
        self.users = {}

    def is_valid_user_id(self, user_id):
        # Validate User ID: alphanumeric, periods, and underscores only
        pattern = r'^[a-zA-Z0-9._]+$'
        return re.match(pattern, user_id) is not None

    def register_user(self, user_id, password, role):
        if not self.is_valid_user_id(user_id):
            return "Invalid User ID. Only alphanumerical values, periods, and underscores are allowed."

        if user_id in self.users:
            return "User ID already registered. Please log in with your credentials."
        else:
            self.users[user_id] = User(user_id, password, role)
            print(f"Registered Users: {self.users.keys()}")  # Debugging line
            return f"{user_id} registered as {role}."

    def login_user(self, user_id, password):
        print("Trying to log in with User ID:", user_id)  # Debugging line
        if user_id in self.users:
            print("User found. Checking password...")  # Debugging line
            if self.users[user_id].password == password:
                return True, self.users[user_id]
            else:
                print("Incorrect password.")  # Debugging line
        else:
            print("User ID not found.")  # Debugging line
        return False, None

    def mark_attendance(self, user, entry_time, exit_time):
        record = {
            "entry_time": entry_time,
            "exit_time": exit_time,
            "status": self.get_attendance_status(entry_time)
        }
        user.attendance_records.append(record)
        return f"Attendance marked for {user.user_id}: {record}"

    def get_attendance_status(self, entry_time):
        return "Late" if entry_time > "09:00" else "On Time"

    def request_leave(self, user, reason):
        user.leave_requests.append(reason)
        return f"Leave requested by {user.user_id} for reason: {reason}"

    def show_attendance(self, user):
        attendance_info = f"\nAttendance records for {user.user_id}:"
        for record in user.attendance_records:
            attendance_info += f"\nEntry: {record['entry_time']} - Exit: {record['exit_time']} - Status: {record['status']}"
        return attendance_info

attendance_system = AttendanceSystem()

# Streamlit user interface
st.title("Attendance Management System")

# Instructions for User ID and Password
st.subheader("User ID Requirements:")
st.markdown("""
- Must be alphanumerical (letters and numbers).
- Can include periods (.) and underscores (_).
- Cannot include spaces or other special characters.
""")

st.subheader("Password Requirements:")
st.markdown("""
- Must include at least one special character (e.g., @, #, $, etc.).
- Must be a combination of uppercase and lowercase letters.
""")

menu = st.selectbox("Menu", ["Register", "Login"])

if menu == "Register":
    st.subheader("Register")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["Manager", "Employee"])

    if st.button("Register"):
        result = attendance_system.register_user(user_id, password, role)
        st.success(result)

elif menu == "Login":
    st.subheader("Login")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        logged_in, current_user = attendance_system.login_user(user_id, password)
        if logged_in:
            st.success(f"Welcome {current_user.user_id}!")

            entry_time = st.text_input("Entry Time (HH:MM)")
            exit_time = st.text_input("Exit Time (HH:MM)")

            if st.button("Mark Attendance"):
                result = attendance_system.mark_attendance(current_user, entry_time, exit_time)
                st.success(result)

            leave_reason = st.text_input("Leave Reason")

            if st.button("Request Leave"):
                result = attendance_system.request_leave(current_user, leave_reason)
                st.success(result)

            if st.button("Show Attendance Records"):
                records = attendance_system.show_attendance(current_user)
                st.text_area("Attendance Records", records, height=300)
        else:
            st.error("Invalid User ID or Password.")
