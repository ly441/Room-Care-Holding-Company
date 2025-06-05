# backend/app/utils/payroll_calculator.py
def calculate_payroll(employee_id: int, start_date: date, end_date: date, db: Session):
    shifts = db.query(Shift).filter(
        Shift.employee_id == employee_id,
        Shift.shift_date >= start_date,
        Shift.shift_date <= end_date
    ).all()
    
    total_hours = sum(
        (shift.end_time.hour - shift.start_time.hour) + 
        (shift.end_time.minute - shift.start_time.minute)/60
        for shift in shifts
    )
    
    employee = db.query(Employee).get(employee_id)
    overtime = max(0, total_hours - 40)
    regular_hours = total_hours - overtime
    
    return {
        "gross_pay": (regular_hours * employee.hourly_rate) + 
                     (overtime * employee.hourly_rate * 1.5),
        "hours_worked": total_hours,
        "overtime_hours": overtime
    }