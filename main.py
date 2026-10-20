import json
from pathlib import Path


import json
import os


class Employee:
    def __init__(self, emp_id, name, department, position, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.position = position
        self.salary = salary

    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "department": self.department,
            "position": self.position,
            "salary": self.salary
        }

    def display(self):
        print("-" * 45)
        print(f"Employee ID : {self.emp_id}")
        print(f"Name        : {self.name}")
        print(f"Department  : {self.department}")
        print(f"Position    : {self.position}")
        print(f"Salary      : Rs. {self.salary:.2f}")


class EmployeeManagementSystem:
    def __init__(self, filename="employees.json"):
        self.filename = filename
        self.employees = {}
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                emp = Employee(
                    item["emp_id"],
                    item["name"],
                    item["department"],
                    item["position"],
                    float(item["salary"])
                )
                self.employees[emp.emp_id] = emp

        except (json.JSONDecodeError, OSError, KeyError, TypeError,
                ValueError) as error:
            print("Warning: Could not load employee data:", error)

    def save_data(self):
        try:
            data = [
                employee.to_dict()
                for employee in self.employees.values()
            ]

            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

        except OSError as error:
            print("Error saving data:", error)

    def add_employee(self):
        print("\n--- Add Employee ---")

        emp_id = input("Enter employee ID: ").strip()

        if not emp_id:
            print("Employee ID cannot be empty.")
            return

        if emp_id in self.employees:
            print("This employee ID already exists.")
            return

        name = input("Enter employee name: ").strip()
        department = input("Enter department: ").strip()
        position = input("Enter job position: ").strip()

        if not name or not department or not position:
            print("Name, department and position are required.")
            return

        try:
            salary = float(input("Enter monthly salary (Rs.): "))

            if not 0 <= salary < float("inf"):
                print("Salary must be a finite, non-negative number.")
                return

        except ValueError:
            print("Invalid salary. Enter a number.")
            return

        employee = Employee(
            emp_id, name, department, position, salary
        )

        self.employees[emp_id] = employee
        self.save_data()
        print("Employee added successfully!")

    def view_employees(self):
        print("\n--- All Employees ---")

        if not self.employees:
            print("No employee records found.")
            return

        for employee in self.employees.values():
            employee.display()

    def search_employee(self):
        emp_id = input("Enter employee ID to search: ").strip()
        employee = self.employees.get(emp_id)

        if employee:
            employee.display()
        else:
            print("Employee not found.")

    def update_employee(self):
        emp_id = input("Enter employee ID to update: ").strip()
        employee = self.employees.get(emp_id)

        if not employee:
            print("Employee not found.")
            return

        print("Leave a field blank to keep its current value.")

        name = input(f"Name [{employee.name}]: ").strip()
        department = input(
            f"Department [{employee.department}]: "
        ).strip()
        position = input(
            f"Position [{employee.position}]: "
        ).strip()
        salary_text = input(
            f"Salary [{employee.salary}]: "
        ).strip()

        if name:
            employee.name = name
        if department:
            employee.department = department
        if position:
            employee.position = position

        if salary_text:
            try:
                salary = float(salary_text)

                if not 0 <= salary < float("inf"):
                    print("Invalid salary. Update cancelled.")
                    return

                employee.salary = salary

            except ValueError:
                print("Invalid salary. Update cancelled.")
                return

        self.save_data()
        print("Employee updated successfully!")

    def delete_employee(self):
        emp_id = input("Enter employee ID to delete: ").strip()
        employee = self.employees.get(emp_id)

        if not employee:
            print("Employee not found.")
            return

        confirm = input(
            f"Delete {employee.name}? (y/n): "
        ).strip().lower()

        if confirm == "y":
            del self.employees[emp_id]
            self.save_data()
            print("Employee deleted successfully!")
        else:
            print("Deletion cancelled.")

    def salary_report(self):
        print("\n--- Salary Report ---")

        if not self.employees:
            print("No employee records available.")
            return

        salaries = [
            employee.salary
            for employee in self.employees.values()
        ]

        total = sum(salaries)
        average = total / len(salaries)

        print(f"Number of employees: {len(salaries)}")
        print(f"Total monthly salary: Rs. {total:.2f}")
        print(f"Average monthly salary: Rs. {average:.2f}")

    def run(self):
        while True:
            print("\n===== EMPLOYEE MANAGEMENT SYSTEM =====")
            print("1. Add Employee")
            print("2. View All Employees")
            print("3. Search Employee")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Salary Report")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ").strip()

            try:
                if choice == "1":
                    self.add_employee()
                elif choice == "2":
                    self.view_employees()
                elif choice == "3":
                    self.search_employee()
                elif choice == "4":
                    self.update_employee()
                elif choice == "5":
                    self.delete_employee()
                elif choice == "6":
                    self.salary_report()
                elif choice == "7":
                    print("Thank you for using the system!")
                    break
                else:
                    print("Invalid choice. Select a number from 1 to 7.")

            except (EOFError, KeyboardInterrupt):
                print("\nApplication interrupted.")
                break


if __name__ == "__main__":
    system = EmployeeManagementSystem()
    system.run()
