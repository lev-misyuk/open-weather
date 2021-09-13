from app.models import Link, User, Item

def test_new_user():
    user = User(login='lev', password='123')
    assert user.login == 'lev'
    assert not user.login == 'lev1'
    assert user.password == '123'
    assert user.__repr__() == 'User lev'

def test_new_item():
    item = Item(name='Book', owner_login='lev')
    assert item.name == 'Book'
    assert not item.name == 'Fork'
    assert item.owner_login == 'lev'
    assert not item.owner_login != 'lev'
    assert item.__repr__() == 'Item Book'

def test_new_link():
    link = Link(_from='aaa', _to='bbb', _text='aaa/bbb')
    assert link._from == 'aaa'
    assert not link._from == 'bbb'
    assert link._to == 'bbb'
    assert not link._text == 'bbb/aaa'
    assert link._text  == 'aaa/bbb'
    assert link.__repr__() == 'Link aaa/bbb from aaa to bbb'
