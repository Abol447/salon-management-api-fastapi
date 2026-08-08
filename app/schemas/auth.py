from pydantic import BaseModel 


class LoginSchema (BaseModel) : 
    user_name : str 
    password : str



class LoginResponse (BaseModel):
    access_token : str
    refresh_token : str

class LogOutSchema(BaseModel):
    refresh_token : str
