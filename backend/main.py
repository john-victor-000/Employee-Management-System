from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import session
from fastapi.middleware.cors import CORSMiddleware


from database import engine,SessionLocal
from models import CreateEmployee
import database_models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database_models.Base.metadata.create_all(bind=engine)

employees=[
    CreateEmployee(name="John",department="IT",salary=25000.00,experience=0),
    CreateEmployee(name="Dinesh",department="DevOPS",salary=38000.00,experience=3),
    CreateEmployee(name="Raju",department="Sales",salary=35000.00,experience=2),
    CreateEmployee(name="Phani",department="HR",salary=75000.00,experience=4),
    CreateEmployee(name="Basker",department="Sales Executive",salary=70000.00,experience=3),
    CreateEmployee(name="Lokesh",department="Marketing",salary=44000.00,experience=2),
    CreateEmployee(name="Narendhra",department="CEO",salary=240000.00,experience=5),
    CreateEmployee(name="Koti Shanker",department="Marketing",salary=44000.00,experience=1),
    CreateEmployee(name="Rohit Sai",department="Sales",salary=54000.00,experience=4)
]

def initial_db():
    db = SessionLocal()

    count = db.query(database_models.Employee).count()
    if count==0:
        for employee in employees:
            db.add(database_models.Employee(**employee.model_dump()))
        db.commit()
        print("Intial data added successfully")
    db.close()
initial_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greet():
    return{
        "message":"Welcome to Employee Management System"
        }

@app.get("/employee")      
def get_all_employees(db:session=Depends(get_db)):
    emp =db.query(database_models.Employee).all()
    if not emp:
        raise HTTPException(status_code=404, detail="No Employees are recorded")
    return emp


@app.get("/employee/{emp_id}")          
def get_employee_by_id(emp_id:int, db:session=Depends(get_db)):
    emp = db.query(database_models.Employee).filter(database_models.Employee.id == emp_id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Emplouyee not found")
    return emp


@app.post("/employee")
def create_employee(employee:CreateEmployee, db:session=Depends(get_db)):
    new_emp = database_models.Employee(**employee.model_dump())
    db.add(new_emp)
    db.commit()
    return {"message": "Employee details updated successfully"}


@app.put("/employee/{emp_id}")
def update_employee(emp_id:int,employee:CreateEmployee,db:session=Depends(get_db)):
    emp = db.query(database_models.Employee).filter(database_models.Employee.id == emp_id).first()
    
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp.name = employee.name
    emp.department = employee.department
    emp.salary = employee.salary
    emp.experience = employee.experience

    db.commit()
    return {"message": "Employee updated successfully"}



@app.delete("/employee/{emp_id}")
def delete_employee(emp_id:int,db:session=Depends(get_db)):
    emp = db.query(database_models.Employee).filter(database_models.Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(emp)
    db.commit()
    
    return {"message": "Employee deleted successfully"}
