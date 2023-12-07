from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table
from sqlalchemy.orm import declarative_base,relationship,Session

engine = create_engine('sqlite:///manytomany.db')
Base = declarative_base()

#create the join table
association_table = Table('student_tm_association',Base.metadata,Column('student_id',Integer,ForeignKey("students.id")),Column('tm_id',Integer,ForeignKey("tms.id")))
class TM(Base):
    __tablename__ = 'tms'
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)

    #relationship
    students = relationship('Student',secondary= association_table,back_populates="tms")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer,primary_key= True)
    name = Column(String,nullable=False)
    age = Column(Integer,nullable = False)
    #relationship
    tms = relationship('TM',secondary=association_table,back_populates="students")
#create the tables
Base.metadata.create_all(engine)
session = Session(engine)

tm1 = TM(name="Steve",age=29)
tm2 = TM(name="Khalifa",age = 30)

stud1 = Student(name="Anisa",age= 22,tms=[tm1,tm2])
stud2 = Student(name="Derick",age = 24,tms=[tm2])

session.add_all([tm1,tm2,stud1,stud2])
session.commit()

students_with_tms = session.query(Student).all()
for student in students_with_tms:
    print(f"Student {student.name} belongs to the following tms: ")
    for tm in student.tms:
        print(f" - {tm.name}")
session.close()