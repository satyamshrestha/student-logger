from models.student import Student

class StudentService():

    def find_student(self, db, student_id: str) -> Student | None:
        return db.query(Student).filter(Student.student_id == student_id).first()

    def add_student(self, db, student: Student):        
        if self.find_student(db, student.student_id):
            raise ValueError(f"Student with ID {student.student_id} already exists")
        
        db.add(student)
        db.commit()
        db.refresh(student)  
        return student 

    def update_student(self, db, student_id: str, name=None, age=None):
        if name is None and age is None:
            raise ValueError("No update data provided")
        
        student = self.find_student(db, student_id)

        if not student:
            raise ValueError(f"Student with ID {student_id} not found")
        
        if name is not None:
            student.name = name
        
        if age is not None:
            student.age = age
        
        db.commit()
        db.refresh(student)
        return student
    
    def count_students(self, db):
        return db.query(Student).count()

    def delete_student(self, db, student_id: str):
        student = self.find_student(db, student_id)
        if not student:
            raise ValueError(f"Student with ID {student_id} not found!")
        
        db.delete(student)
        db.commit()
        return True

    def get_all_students(self, db, age=None, min_age=None, max_age=None, name=None, sort=None, order="asc", limit=10, offset=0):
        query = db.query(Student)
        # Filtering
        if age is not None:
            query = query.filter(Student.age == age)
        else:
            if min_age is not None:
                query = query.filter(Student.age >= min_age)
            if max_age is not None:
                query = query.filter(Student.age <= max_age)
        if name is not None:
            query = query.filter(Student.name.ilike(f"%{name}%"))
        
        # Sorting
        if sort == "age":
            if order == "desc":
                query = query.order_by(Student.age.desc())
            else: 
                query = query.order_by(Student.age)
    
        # Pagination
        return query.offset(offset).limit(limit).all()