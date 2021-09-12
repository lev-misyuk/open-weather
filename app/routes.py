from app import app, db
from app.models import Link, User, Item
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@app.route('/registration', methods=['POST'])
def register():
    if request.method != 'POST':
        return jsonify({'message': 'Method not allowed'}), 405
    try:
        assert 'login' in request.args and 'password' in request.args
    except AssertionError:
        return jsonify({'message': 'Both of login and password must be provided'}), 422
    else:
        login, password = request.args.get('login'), request.args.get('password')
        try:
            assert len(login) > 0 and len(password) > 0
        except AssertionError:
            return jsonify({'message': 'Invalid login or password'}), 422
        else:
            try: 
                assert login not in (u.login for u in User.query.all())
            except AssertionError:
                return jsonify({'message': f'User with login {login} already exists'}), 422
            else:
                user = User(login=login, password=password)
                db.session.add(user)
                db.session.commit()
                return jsonify({'message': f'User {login} has registered'})

@app.route('/login', methods=['POST'])
def login():
    if request.method != 'POST':
        return jsonify({'message': 'Method not allowed'}), 405
    try:
        assert 'login' in request.args and 'password' in request.args
    except AssertionError:
        return jsonify({'message': 'Both of login and password must be provided'}), 422
    else:
        login, password = request.args.get('login'), request.args.get('password')
        try:
            assert len(login) > 0 and len(password) > 0
        except AssertionError:
            return jsonify({'message': 'Invalid login or password'}), 422
        else:
            user = User.query.filter_by(login=login, password=password).first()
            if user:
                token = create_access_token(identity=login)
                return jsonify({'token': token})
            
            return jsonify({'message': 'Authorization failed'}), 401

@app.route('/items/new', methods=['POST'])
@jwt_required()
def create_item():
    if request.method != 'POST':
        return jsonify({'message': 'Method not allowed'}), 405
    current_user = get_jwt_identity()
    try:
        assert 'name' in request.args
    except AssertionError:
        return jsonify({'message': 'Name must be provided'}), 422
    else:
        name = request.args.get('name')
        try:
            assert len(name) > 0
        except AssertionError:
            return jsonify({'message': 'Invalid item name'})
        else:
            item = Item(name=name, owner_login=current_user)
            db.session.add(item)
            db.session.flush()
            db.session.refresh(item)
            db.session.commit()
            return jsonify({'message': 'Item has been created', 'item_id': item.id, 'item_name': item.name})

@app.route('/items/<id>', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    if request.method != 'DELETE':
        return jsonify({'message': 'Method not allowed'}), 405
    current_user = get_jwt_identity()
    item = Item.query.filter_by(id=id, owner_login=current_user).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': f'Item with id {id} has been deleted'})
    return jsonify({'message': 'Item not found'}), 404

@app.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    if request.method != 'GET':
        return jsonify({'message': 'Method not allowed'}), 405
    current_user = get_jwt_identity()
    items = Item.query.filter_by(owner_login=current_user).all()
    return jsonify([{'item_id': item.id, 'item_name': item.name} for item in items])

@app.route('/send', methods=['POST'])
@jwt_required()
def send_item():
    if request.method != 'POST':
        return jsonify({'message': 'Method not allowed'}), 405
    current_user = get_jwt_identity()
    try:
        assert 'id' in request.args and len(request.args.get('id')) > 0
    except AssertionError:
        return jsonify({'message': 'Invalid item id'}), 422
    else:
        try:
            assert 'login' in request.args and len(request.args.get('login')) > 0
        except AssertionError:
            return jsonify({'message': 'Invalid login'}), 422
        else:
            receiver_login, id = request.args.get('login'), request.args.get('id')
            receiver = User.query.filter_by(login=receiver_login).first()
            if not receiver:
                return jsonify({'message': 'User not found'}), 404

            item = Item.query.filter_by(owner_login=current_user, id=id).first()
            if not item:
                return jsonify({'message': 'Item not found'}), 404

            link = Link(_text=f'{receiver_login}/{id}', _from=current_user, _to=receiver_login)
            db.session.add(link)
            db.session.commit()
            return jsonify({'link': link._text})

@app.route('/get', methods=['GET'])
@jwt_required()
def receive_item():
    if request.method != 'GET':
        return jsonify({'message': 'Method not allowed'}), 405
    current_user = get_jwt_identity()
    try:
        assert 'link' in request.args and len(request.args.get('link')) > 0
    except AssertionError:
        return jsonify({'message': 'Invalid link'}), 422
    else:
        link = request.args.get('link').split('/')
        if link[0] != current_user:
            return jsonify({'message': 'You are not able to receive this item'}), 403
        
        if not Link.query.filter_by(_text=request.args.get('link')).first():
            return jsonify({'message': 'Link not found'}), 404
        
        item = Item.query.filter_by(id=link[1]).first()
        item.owner_login = current_user
        db.session.commit()
        return jsonify({'message': f'Item {item.name} has been received'})

