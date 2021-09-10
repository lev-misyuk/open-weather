from datetime import datetime
from os import access
from app import app, db
from app.models import User, Item
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@app.route('/registration', methods=['POST'])
def register():
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
            return jsonify({'message': 'Item has been created', 'item_id': item.id, 'item_name': item.name, 'item_owner': item.owner_login})
