from models.student import Student

class StudentService():

    def find_student(self, db, student_id: str) -> Student | None:
        return db.query(Student).filter(Student.student_id == student_id).first()

    def add_student(self, db, data):
        student = Student(**data.model_dump())        
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

    def get_all_students(self, db, query):
        q = db.query(Student)
        # Filtering
        if query.age is not None:
            q = q.filter(Student.age == query.age)
        else:
            if query.min_age is not None:
                q = q.filter(Student.age >= query.min_age)
            if query.max_age is not None:
                q = q.filter(Student.age <= query.max_age)
        if query.name is not None:
            q = q.filter(Student.name.ilike(f"%{query.name}%"))
        
        # Sorting
        if query.sort == "age":
            if query.order == "desc":
                q = q.order_by(Student.age.desc())
            else: 
                q = q.order_by(Student.age)
    
        # Pagination
        return q.offset(query.offset).limit(query.limit).all()