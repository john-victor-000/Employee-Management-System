from pydantic import BaseModel

class CreateEmployee(BaseModel):

    name:str
    department:str
    salary:float
    experience:int
