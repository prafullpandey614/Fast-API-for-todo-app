# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import Optional
# from db import collection
# app = FastAPI()

from pickle import FALSE, TRUE
from xmlrpc.client import Boolean
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from auth import AuthHandler
from schemas import AuthDetails


app = FastAPI()


auth_handler = AuthHandler()
users = []
todo_tasks = []


class Todo_Task(BaseModel):
    title : str
    status : bool

@app.get('/')
def home_page():
    return { 'Greeting': 'Hi , Please Login to Add Tasks' }
@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return {"Message": "Registered Succesfully"}


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }




@app.get('/tasks')
def show_all_tasks(username=Depends(auth_handler.auth_wrapper)):
    
    resp = []
    for task in todo_tasks:
        if task[0] == username:
            resp.append(task[1])
            
   
    return resp
@app.post('/add_task')
def add_a_task(task : Todo_Task,username=Depends(auth_handler.auth_wrapper)):
    todo_tasks.append([username,task])
    return {"message": "Task Added Successfully"}

@app.post('/change_status_of_task')
def add_a_task(task_title: str,task_completed : Boolean,username=Depends(auth_handler.auth_wrapper)):
    flag = FALSE
    for task in todo_tasks:
        if task[0] == username and task[1].title == task_title:
            task[1].status = task_completed
            flag = TRUE
    if not flag:
        return {"Message": "No task Found"}
    return {"message": "Task Status Changed Successfully"}

@app.delete('/delete_task')
def add_a_task(task_title : str,username=Depends(auth_handler.auth_wrapper)):
    for task in todo_tasks:
        if task[0] == username and task[1].title == task_title :
            todo_tasks.remove(task)
    return {"message": "Task Removed Successfully"}













# fakedb = []
# class Course(BaseModel):
#     id : int
#     name  : str
#     price: float
#     is_early_bird : Optional[bool] = None 

# @app.get("/")
# def read_root():
#     return {"greetings":"Welcome to the fastAPI"}
# @app.get("/courses")
# def get_courses():
    
#     return collection
# @app.get("/courses/{course_id}")
# def get_a_course(course_id: int):
#     course =  course_id -1
#     collection.find_one({"course_id": course})
#     return fakedb[course]
# @app.post("/courses")
# def add_course(course: Course):
#     collec
#     return fakedb[-1]
# @app.delete("/courses/{course_id}")
# def delete_course(course_id: int):
#     fakedb.pop(course_id-1)
#     return {"Task": "Deletion Succesfully"}