from flask import Flask, redirect, url_for, session, jsonify, send_from_directory
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

load_dotenv()

print("Loaded NYT_API_KEY:", os.getenv("NYT_API_KEY"))



app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)


oauth = OAuth(app)

nonce = generate_token()


oauth.register(
    name=os.getenv('OIDC_CLIENT_NAME'),
    client_id=os.getenv('OIDC_CLIENT_ID'),
    client_secret=os.getenv('OIDC_CLIENT_SECRET'),
    #server_metadata_url='http://dex:5556/.well-known/openid-configuration',
    authorization_endpoint="http://localhost:5556/auth",
    token_endpoint="http://dex:5556/token",
    jwks_uri="http://dex:5556/keys",
    userinfo_endpoint="http://dex:5556/userinfo",
    device_authorization_endpoint="http://dex:5556/device/code",
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/api/key')
def get_key():
    return jsonify({'apiKey': os.getenv('NYT_API_KEY')})

@app.route('/api/articles')
def get_articles():
    nyt_api_key = os.getenv('NYT_API_KEY')
    url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=davis+or+sacramento&api-key={nyt_api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()

        filtered_articles = [
            article for article in data.get('response', {}).get('docs', [])
            if 'davis' in article.get('headline', {}).get('main', '').lower() or
               'sacramento' in article.get('headline', {}).get('main', '').lower()
        ]
        
        return jsonify({'results': filtered_articles})
    except Exception as e:
        print('Error fetching NYT data:', e)
        return jsonify({'results': [], 'error': str(e)})


@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f"<h2>Logged in as {user['email']}</h2><a href='/logout'>Logout</a>"
    return '<a href="/login">Login with Dex</a>'

@app.route('/login')
def login():
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:5173/authorize'
    return oauth.flask_app.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = oauth.flask_app.authorize_access_token()
    nonce = session.get('nonce')

    user_info = oauth.flask_app.parse_id_token(token, nonce=nonce)  # or use .get('userinfo').json()
    session['user'] = user_info
    return redirect('/')

@app.route('/api/user')
def get_user():
    user = session.get('user')
    if user:
        return jsonify({'loggedIn': True, 'email': user.get('email'), 'name': user.get('name')})
    return jsonify({'loggedIn': False})


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)