# 510_lab3
### Overview
A tp-do app and a file to store the task information.
### How to run
- Installation :```pip install -r requirements.txt```
- Usage :```streamlit run app.py```
### Lessons learned
- Learned to assign unique keys to similar components in Streamlit via the DuplicateWidgetID bug
- Learned how to use sqlite3 in Python for database operations, including creating tables, inserting data, and performing queries.
### Questions/Future improvements
- I want to add the time zone when the datetime function is applied, but this requires a specific library to be installed, and what if the user doesn't have this library when the todo app is running?
- When I add the "delete task" feature, it just rebuilds the entire todo app, but somehow my layout gets messed up and data is lost.
