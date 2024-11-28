import streamlit as st
import requests

# Define FastAPI backend URL
BACKEND_URL = "http://badello_backend:80/tasks/"

# Fetch tasks from the backend and update the session state
def refresh_task_list():
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            st.session_state.tasks = response.json()
        else:
            st.error("Failed to fetch tasks from the backend.")
    except Exception as e:
        st.error(f"Error: {e}")

# Add a new task
def add_task(title, description, completed):
    try:
        response = requests.post(
            BACKEND_URL,
            json={"title": title, "description": description, "completed": completed},
        )
        if response.status_code == 200:
            st.success("Task added successfully!")
            refresh_task_list()  # Refresh the task list after adding a task
            st.rerun()
        else:
            st.error("Failed to add task.")
    except Exception as e:
        st.error(f"Error: {e}")

# Delete a task
def delete_task(task_id):
    try:
        response = requests.delete(f"{BACKEND_URL}{task_id}")
        if response.status_code == 200:
            st.success("Task deleted successfully!")
            refresh_task_list()  # Refresh the task list after deleting a task
            st.rerun()
        else:
            st.error("Failed to delete task.")
    except Exception as e:
        st.error(f"Error: {e}")

# Update a task
def update_task(task_id, title, description, completed):
    try:
        response = requests.put(
            f"{BACKEND_URL}{task_id}",
            json={"title": title, "description": description, "completed": completed},
        )
        if response.status_code == 200:
            st.success("Task updated successfully!")
            refresh_task_list()  # Refresh the task list after updating a task
            st.rerun()
        else:
            st.error("Failed to update task.")
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit UI
st.title("Task Manager")
st.sidebar.header("Navigation")

# Fetch tasks section (only fetch once at the start)
if 'tasks' not in st.session_state:
    refresh_task_list()  # Initialize the task list on the first run

st.subheader("Task List")
for task in st.session_state.tasks:
    st.markdown(
        f"""
        **Title**: {task['title']}  
        **Description**: {task['description']}  
        **Status**: {"Completed ✅" if task['completed'] else "Not Completed ❌"}  
        **Task ID**: {task['id']}  
        ---
        """
    )

# Add a new task
st.sidebar.subheader("Add a New Task")
with st.sidebar.form("add_task_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    completed = st.checkbox("Completed?")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        add_task(title, description, completed)

# Delete a task
st.sidebar.subheader("Delete a Task")
with st.sidebar.form("delete_task_form"):
    task_id = st.number_input("Task ID", min_value=0, step=1)
    delete_submitted = st.form_submit_button("Delete Task")
    if delete_submitted:
        delete_task(task_id)

# Update a task
st.sidebar.subheader("Update a Task")
with st.sidebar.form("update_task_form"):
    task_id = st.number_input("Task ID to Update", min_value=0, step=1, key="update_id")
    title = st.text_input("New Title", key="update_title")
    description = st.text_area("New Description", key="update_description")
    completed = st.checkbox("Completed?", key="update_completed")
    update_submitted = st.form_submit_button("Update Task")
    if update_submitted:
        update_task(task_id, title, description, completed)

