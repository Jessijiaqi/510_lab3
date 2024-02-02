import sqlite3
import os
import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp
from datetime import datetime
from enum import Enum

# Database connection setup
DB_CONFIG = os.getenv("DB_TYPE")
if DB_CONFIG == 'PG':
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")
    # You should add PostgreSQL connection setup here
else:
    con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
cur = con.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        state TEXT,
        created_at DATETIME,
        created_by TEXT,
        category TEXT
    );
""")

# Define enums
class State(str, Enum):
    planned = 'planned'
    in_progress = 'in-progress'
    done = 'done'

class Category(str, Enum):
    school = 'school'
    work = 'work'
    personal = 'personal'

# Task model
class Task(BaseModel):
    name: str
    description: str
    state: State
    created_at: datetime
    created_by: str
    category: Category

# Function to update task state
def toggle_state(current_state, row):
    new_state = 'done' if current_state != 'done' else 'planned'
    cur.execute("UPDATE tasks SET state = ? WHERE id = ?", (new_state, row[0]))

# Function to delete a task
def delete_task(task_id):
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

# Main function
def main():
    st.title("Todo App")

    # Add new task
    data = sp.pydantic_form(key="task_form", model=Task)
    if data:
        cur.execute("INSERT INTO tasks (name, description, state, created_at, created_by, category) VALUES (?, ?, ?, ?, ?, ?)",
                    (data.name, data.description, data.state.value, datetime.now(), data.created_by, data.category.value))

    # Search and filter UI
    search_query = st.text_input("Search tasks", key="search_query")
    category_filter = st.selectbox("Filter by category", ["All", "school", "work", "personal"], key="category_filter")

    # Build and execute query
    query = "SELECT * FROM tasks WHERE name LIKE ?"
    params = [f"%{search_query}%"]
    if category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)

    filtered_data = cur.execute(query, params).fetchall()

    # Show filtered data with delete option
    if filtered_data:
        for row in filtered_data:
            with st.container():
                cols = st.columns((1, 3, 3, 2, 2, 2, 1))  # Adjust column widths as needed
                cols[0].checkbox('Done', row[3] == 'done', label_visibility='hidden', key=f"done_{row[0]}", on_change=toggle_state, args=(row[3], row))
                cols[1].write(row[1])
                cols[2].write(row[2])
                cols[3].write(row[4])
                cols[4].write(row[5])
                cols[5].write(row[6])
                # Delete button
                if cols[6].button("Delete", key=f"delete_{row[0]}"):
                    delete_task(row[0])
                    st.experimental_rerun()  # Rerun the app to refresh the displayed tasks

main()
