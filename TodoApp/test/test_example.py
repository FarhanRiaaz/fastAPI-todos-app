import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    
def test_is_instance():
    assert isinstance('this is a string',str)
    
def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False   

def test_type():
    assert type('hello' is str)
    assert type('world' is not int)


def test_ranges():
    assert 5>4
    assert 4>1

class Student:
    def __init__(self,first_name:str,last_name:str,major:str,year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year
@pytest.fixture
def default_employee():
    return Student('john','doe','computer science',3)
        
def test_person_initialization(default_employee):
    # p = Student('john','doe','computer science',3)
  #  assert p.first_name == 'john','First name should be john'  
    assert default_employee.first_name == 'john','First name should be john'  
    assert default_employee.last_name == 'doe','Last name should be doe'  
    assert default_employee.major == 'computer science'  
    assert default_employee.year == 3
                