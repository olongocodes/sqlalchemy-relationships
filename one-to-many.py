from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.orm import declarative_base,relationship,Session
engine = create_engine('sqlite:///onetomany.db')
Base = declarative_base()

class TM(Base):
    __tablename__ = 'tms'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    age = Column(Integer)
    #define the relationship
    students = relationship('Student',back_populates='tm')

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    age = Column(Integer)
    #define the foreignkey
    tm_id = Column(Integer,ForeignKey('tms.id'))
    tm = relationship('TM',back_populates='students')

#create the tables
Base.metadata.create_all(engine)
session = Session(engine)

tm1 = TM(name="Solomon",age = 34)
stud1 = Student(name="Jane",age = 27,tm=tm1)
stud2 = Student(name="Mark",age = 23,tm=tm1)

session.add_all([tm1,stud1,stud2])
session.commit()

tm_with_students = session.query(TM).filter_by(name="Solomon").first()
print("Tm: ",tm_with_students.name)
print("Students: ")
for student in tm_with_students.students:
    print(f"- {student.name}")
stud = session.query(Student).filter_by(name = "Mark").first()
print(stud.tm.name)
session.close()