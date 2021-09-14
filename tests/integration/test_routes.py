from app.models import Item

def register(client, login = None, password = None):
    return client.post('/registration', query_string=dict(login=login, password=password))

def login(client, login = None, password = None):
    return client.post('/login', query_string=dict(login=login, password=password))


def test_registration(client):
    res = register(client, 'lev', '123')
    assert b'User lev has registered' in res.data
    assert res.status_code == 200

    res = register(client, 'lev', '123')
    assert b'User with login lev already exists' in res.data
    assert res.status_code == 422

    res = client.get('/registration?login=lev&password=123')
    assert b'Method Not Allowed' in res.data
    assert res.status_code == 405

    res = register(client, 'lev')
    assert b'Both of login and password must be provided' in res.data
    assert res.status_code == 400

    res = register(client, 'lev', '')
    assert b'Invalid login or password' in res.data
    assert res.status_code == 400

    res = register(client, '', '123')
    assert b'Invalid login or password' in res.data
    assert res.status_code == 400

def test_login(client):
    register(client, 'lev', '123')
    res = login(client, 'lev', '123')
    assert b'token' in res.data
    assert res.status_code == 200

    res = client.get('/login?login=lev&password=123')
    assert b'Method Not Allowed' in res.data
    assert res.status_code == 405

    res = login(client, 'lev', '')
    assert b'Invalid login or password' in res.data
    assert res.status_code == 400

    res = login(client, '', '123')
    assert b'Invalid login or password' in res.data
    assert res.status_code == 400

    res = login(client, 'lev')
    assert b'Both of login and password must be provided' in res.data
    assert res.status_code == 400

    res = login(client, 'aaa', '123')
    assert b'Authorization failed' in res.data
    assert res.status_code == 401

def test_create_item(client):
    register(client, 'lev', '123')
    res = login(client, 'lev', '123')
    assert res.status_code == 200
    assert b'token' in res.data

    token = res.get_json().get('token')

    res = client.get('/items/new')
    assert b'Method Not Allowed' in res.data
    assert res.status_code == 405

    res = client.post('/items/new', query_string=dict(name='Book'))
    assert b'Missing Authorization Header' in res.data
    assert res.status_code == 401

    res = client.post('/items/new', query_string=dict(name='Book'), headers=dict(Authorization=f'Bearer {token}'))
    assert b'Item has been created' in res.data
    assert res.get_json().get('item_name') == 'Book'
    assert res.status_code == 200

    res = client.post('/items/new', headers=dict(Authorization=f'Bearer {token}'))
    assert b'Name must be provided' in res.data
    assert res.status_code == 400

    res = client.post('/items/new', query_string=dict(name=''), headers=dict(Authorization=f'Bearer {token}'))
    assert b'Invalid item name' in res.data
    assert res.status_code == 400

def test_delete_item(client):
    register(client, 'lev', '123')
    res = login(client, 'lev', '123')
    token = res.get_json().get('token')
    
    res = client.post('/items/new', query_string=dict(name='Book'), headers=dict(Authorization=f'Bearer {token}'))
    item_id = res.get_json().get('item_id')

    res = client.delete('/items/66754879648756')
    assert b'Missing Authorization Header' in res.data
    assert res.status_code == 401

    res = client.get('/items/66754879648756')
    assert b'Method Not Allowed' in res.data
    assert res.status_code == 405
    
    res = client.delete(f'/items/{item_id + 1}', query_string=dict(name='Book'), headers=dict(Authorization=f'Bearer {token}'))
    assert b'Item not found or you are not an owner of this item' in res.data

    res = client.delete(f'/items/{item_id}', query_string=dict(name='Book'), headers=dict(Authorization=f'Bearer {token}'))
    assert res.get_json().get('message') == f'Item with id {item_id} has been deleted'
    assert res.status_code == 200
    
def test_get_items(client):
    register(client, 'lev', '123')
    res = login(client, 'lev', '123')
    token = res.get_json().get('token')

    res = client.post('/items/new', query_string=dict(name='Book'), headers=dict(Authorization=f'Bearer {token}'))

    res = client.post('/items')
    assert b'Method Not Allowed' in res.data
    assert res.status_code == 405

    res = client.get('/items', headers=dict(Authorization=f'Bearer {token}'))
    items = [
        {
            'item_id': item.id,
            'item_name': item.name
        } for item in Item.query.filter_by(owner_login='lev').all()
    ]
    assert res.get_json() == items
    assert res.status_code == 200

def test_send_item(client):
    register(client, 'lev', '123')
    register(client, 'aaa', '123')

    res = login(client, 'lev', '123')
    lev_token = res.get_json().get('token')

    res = client.post('/items/new', query_string=dict(name='Book'), headers=dict(Authorization=f'Bearer {lev_token}'))
    item_id = res.get_json().get('item_id')

    res = client.get('/send')
    assert b'Method Not Allowed' in res.data
    assert res.status_code == 405

    res = client.post('/send')
    assert b'Missing Authorization Header' in res.data
    assert res.status_code == 401

    res = client.post('/send', headers=dict(Authorization=f'Bearer {lev_token}'))
    assert b'Invalid item id' in res.data
    assert res.status_code == 400

    res = client.post('/send', query_string=dict(id=item_id), headers=dict(Authorization=f'Bearer {lev_token}'))
    assert b'Invalid login' in res.data
    assert res.status_code == 400

    res = client.post('/send', query_string=dict(id=item_id, login='bbb'), headers=dict(Authorization=f'Bearer {lev_token}'))
    assert b'User not found' in res.data
    assert res.status_code == 404

    res = client.post('/send', query_string=dict(id=item_id+1, login='aaa'), headers=dict(Authorization=f'Bearer {lev_token}'))
    assert b'Item not found' in res.data
    assert res.status_code == 404

    res = client.post('/send', query_string=dict(id=item_id, login='aaa'), headers=dict(Authorization=f'Bearer {lev_token}'))
    assert b'link' in res.data
    assert res.status_code == 200

def test_receive_item(client):
    register(client, 'lev', '123')
    register(client, 'aaa', '123')

    res = login(client, 'lev', '123')
    lev_token = res.get_json().get('token')

    res = login(client, 'aaa', '123')
    aaa_token = res.get_json().get('token')

    res = client.post('/items/new', query_string=dict(name='Book'), headers=dict(Authorization=f'Bearer {lev_token}'))
    item_id = res.get_json().get('item_id')
    item = Item.query.filter_by(id=item_id).first()

    res = client.post('/send', query_string=dict(id=item_id, login='aaa'), headers=dict(Authorization=f'Bearer {lev_token}'))
    link = res.get_json().get('link')

    res = client.post('/get')
    assert b'Method Not Allowed' in res.data
    assert res.status_code == 405

    res = client.get('/get')
    assert b'Missing Authorization Header' in res.data
    assert res.status_code == 401

    res = client.get('/get', headers=dict(Authorization=f'Bearer {aaa_token}'))
    assert b'Invalid link' in res.data
    assert res.status_code == 400

    res = client.get('/get', query_string=dict(link=f'bbb/{item_id}'), headers=dict(Authorization=f'Bearer {aaa_token}'))
    assert b'You are not able to receive this item' in res.data
    assert res.status_code == 403

    res = client.get('/get', query_string=dict(link=f'aaa/{item_id + 1}'), headers=dict(Authorization=f'Bearer {aaa_token}'))
    assert b'Link not found' in res.data
    assert res.status_code == 404

    res = client.get('/get', query_string=dict(link=link), headers=dict(Authorization=f'Bearer {aaa_token}'))
    assert res.get_json().get('message') == f'Item {item.name} has been received'
    assert res.status_code == 200
