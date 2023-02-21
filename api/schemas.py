from pydantic import BaseModel

class TodoTask(BaseModel):
    title : str
    pendind_status : bool #task is completed or not
class AuthDetails(BaseModel):
    username: str
    password: str