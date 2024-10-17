import streamlit as st

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.attendance_records = []
        self.leave_requests = []

class AttendanceSystem:
    def __init__(self):
        self.users = {}
    
    def register_user(self, name, role):
        if name in self.users:
            return f"{name} is already registered."
        else:
            self.users[name] = User(name, role)
            return f"{name} registered as {role}."

    def mark_attendance(self, name, entry_time, exit_time):
        if name in self.users:
            record = {
                "entry_time": entry_time,
                "exit_time": exit_time,
                "status": self.get_attendance_status(entry_time)
            }
            self.users[name].attendance_records.append(record)
            return f"Attendance marked for {name}: {record}"
        return f"{name} is not registered."

    def get_attendance_status(self, entry_time):
        return "Late" if entry_time > "09:00" else "On Time"

    def request_leave(self, name, reason):
        if name in self.users:
            self.users[name].leave_requests.append(reason)
            return f"Leave requested by {name} for reason: {reason}"
        return f"{name} is not registered."

    def show_attendance(self):
        attendance_info = ""
        for name, user in self.users.items():
            attendance_info += f"\nAttendance records for {name}:"
            for record in user.attendance_records:
                attendance_info += f"\nEntry: {record['entry_time']} - Exit: {record['exit_time']} - Status: {record['status']}"
        return attendance_info

attendance_system = AttendanceSystem()

# Streamlit user interface
st.title("Attendance Management System")

role = st.selectbox("Select Role", ["Manager", "Employee"])
name = st.text_input("Enter Name")

if st.button("Register"):
    result = attendance_system.register_user(name, role)
    st.success(result)

entry_time = st.text_input("Entry Time (HH:MM)")
exit_time = st.text_input("Exit Time (HH:MM)")

if st.button("Mark Attendance"):
    result = attendance_system.mark_attendance(name, entry_time, exit_time)
    st.success(result)

leave_reason = st.text_input("Leave Reason")

if st.button("Request Leave"):
    result = attendance_system.request_leave(name, leave_reason)
    st.success(result)

if st.button("Show Attendance Records"):
    records = attendance_system.show_attendance()
    st.text_area("Attendance Records", records, height=300)
