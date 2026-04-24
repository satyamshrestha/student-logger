class Student():
    def __init__(self, student_id, name, age):
        self._validate_student_id(student_id)
        self._validate_name(name)
        self._validate_age(age)
        
        self.student_id = student_id
        self.name = name
        self.age = age
    
    def _validate_student_id(self, student_id: str):
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Invalid student ID!")

    def _validate_age(self, age: int):
        if not isinstance(age, int) or age < 0:
            raise ValueError("Invalid age!")

    def _validate_name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid Name!")
    
    def to_dict(self):
        return {
            "student_id": self.student_id, 
            "name": self.name, 
            "age": self.age
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["age"])
    
    def update_age(self, new_age):
        self._validate_age(new_age)
        self.age = new_age
    
    def update_name(self, new_name):
        self._validate_name(new_name)
        self.name = new_name