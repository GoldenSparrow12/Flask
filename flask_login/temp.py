from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/login')
def next():
    return 'login next'

@app.route('/user/<username>')
def userr(username):
    return '{}\'s user name'.format(escape(username))

@app.route('/user/<int:inter>')
def inters(inter):
    return 'number : {}' .format(escape(inter))

@app.route('/user/<float:reno>')
def re(reno):
    return 'float:%f'%reno


# @app.route('/user/<username>')
# def profile(username):
#     return '{}\'s profile'.format(escape(username))

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('next', next='/'))
#     print(url_for('profile', username='John Doe'))

if __name__ == '__main__':
    app.run(debug=True)