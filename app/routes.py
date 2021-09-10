from datetime import date, datetime
from app import app, db
from app.models import User, Item
from flask import request, jsonify
import datetime
import jwt

@app.route('/registration/', methods=['POST'])
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
                return jsonify({'message': f'User {login} has registered!'})

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
            user = User.query.filter_by(login=login).first()
            if not user:
                return jsonify({'message': f'User with login {login} does not exist'}), 404
            
            if user.password == password:
                token = jwt.encode({'login': user.login, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config.get('SECRET_KEY'), 'HS256')
                return jsonify({'token': token.decode('utf-8')})
            
            return jsonify({'message': 'Authorization failed'}), 401