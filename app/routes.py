from app import app, db
from app.models import User, Item
from flask import request

@app.route('/registration/', methods=['POST'])
def register():
    try:
        assert 'login' in request.args and 'password' in request.args
    except AssertionError:
        return 'Both of login and password must be provided', 422
    else:
        login, password = request.args.get('login'), request.args.get('password')
        try:
            assert len(login) > 0 and len(password) > 0
        except AssertionError:
            return 'Both of login and password must consist of 1 character or greater', 422
        else:
            try: 
                assert login not in (u.login for u in User.query.all())
            except AssertionError:
                return f'User with login {login} already exists', 422
            else:
                u = User(login=login, password=password)
                db.session.add(u)
                db.session.commit()
                return f'User {login} has registered!'
        