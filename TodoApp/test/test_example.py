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