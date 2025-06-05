import typer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.branch import Branch
from app.models.employee import  Employee
from app.models.shift import  Shift
from app.models.payroll import  Payroll

app = typer.Typer()
db = SessionLocal()

@app.command()
def list_branches():
    """List all branches"""
    branches = db.query(Branch).all()
    for branch in branches:
        typer.echo(f"{branch.branch_id}: {branch.branch_name}")

@app.command()
def create_branch(name: str, address: str = None, phone: str = None):
    """Create a new branch"""
    branch = Branch(branch_name=name, address=address, phone=phone)
    db.add(branch)
    db.commit()
    typer.echo(f"Created branch: {name}")


# ...existing code...

@app.command()
def list_employees():
    """List all employees"""
    employees = db.query(Employee).all()
    for emp in employees:
        typer.echo(f"{emp.employee_id}: {emp.first_name} {emp.last_name}")

@app.command()
def create_employee(first_name: str, last_name: str, branch_id: int):
    """Create a new employee"""
    employee = Employee(first_name=first_name, last_name=last_name, branch_id=branch_id)
    db.add(employee)
    db.commit()
    typer.echo(f"Created employee: {first_name} {last_name}")

@app.command()
def list_shifts():
    """List all shifts"""
    shifts = db.query(Shift).all()
    for shift in shifts:
        typer.echo(f"{shift.shift_id}: {shift.start_time} - {shift.end_time} (Employee: {shift.employee_id})")

@app.command()
def create_shift(employee_id: int, start_time: str, end_time: str):
    """Create a new shift"""
    shift = Shift(employee_id=employee_id, start_time=start_time, end_time=end_time)
    db.add(shift)
    db.commit()
    typer.echo(f"Created shift for employee {employee_id}: {start_time} - {end_time}")

@app.command()
def list_payrolls():
    """List all payroll records"""
    payrolls = db.query(Payroll).all()
    for payroll in payrolls:
        typer.echo(f"{payroll.payroll_id}: Employee {payroll.employee_id}, Amount: {payroll.amount}, Date: {payroll.date}")

@app.command()
def create_payroll(employee_id: int, amount: float, date: str):
    """Create a new payroll record"""
    payroll = Payroll(employee_id=employee_id, amount=amount, date=date)
    db.add(payroll)
    db.commit()
    typer.echo(f"Created payroll for employee {employee_id}: {amount} on {date}")

# ...existing code...
if __name__ == "__main__":
    app()