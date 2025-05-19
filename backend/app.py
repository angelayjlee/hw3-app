from flask import Flask, jsonify, redirect, send_from_directory, url_for, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
from flask_cors import CORS
import requests


static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
template_path = static_path


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
app.secret_key = os.urandom(24)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=False,  # True if using HTTPS
    SESSION_COOKIE_DOMAIN=None,   # Let Flask set domain to localhost
)


oauth = OAuth(app)

nonce = generate_token()

DEX_CLIENT_ID = os.getenv('OIDC_CLIENT_ID', "flask-app")
DEX_CLIENT_NAME: str = os.getenv('OIDC_CLIENT_NAME', DEX_CLIENT_ID)
DEX_CLIENT_SECRET: str = os.getenv('OIDC_CLIENT_SECRET', "flask-secret")

DEX_INTERNAL_HOST = os.getenv('DEX_INTERNAL_HOST', "http://dex:5556")
DEX_EXTERNAL_HOST = os.getenv('DEX_EXTERNAL_HOST', "http://localhost:5556")

AUTHORIZATION_ENDPOINT = f"{DEX_INTERNAL_HOST}/auth"
TOKEN_ENDPOINT = f"{DEX_INTERNAL_HOST}/token"
JWKS_URI = f"{DEX_INTERNAL_HOST}/keys"
USERINFO_ENDPOINT = f"{DEX_INTERNAL_HOST}/userinfo"
DEVICE_AUTHORIZATION_ENDPOINT = f"{DEX_INTERNAL_HOST}/device/code"
# Set up the OAuth client

oauth.register(
    name=DEX_CLIENT_NAME,
    client_id=DEX_CLIENT_ID,
    client_secret=DEX_CLIENT_SECRET,
    #server_metadata_url=f"{DEX_EXTERNAL_HOST}/.well-known/openid-configuration",
    authorization_endpoint=AUTHORIZATION_ENDPOINT,
    token_endpoint=TOKEN_ENDPOINT,
    jwks_uri=JWKS_URI,
    userinfo_endpoint=USERINFO_ENDPOINT,
    device_authorization_endpoint=DEVICE_AUTHORIZATION_ENDPOINT,
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

        # Filter articles that mention "Davis" or "Sacramento" in the title
        filtered_articles = [
            article for article in data.get('response', {}).get('docs', [])
            if 'davis' in article.get('headline', {}).get('main', '').lower() or
               'sacramento' in article.get('headline', {}).get('main', '').lower()
        ]
        
        # Send back the filtered articles
        return jsonify({'results': filtered_articles})
    except Exception as e:
        print('Error fetching NYT data:', e)
        return jsonify({'results': [], 'error': str(e)})


@app.route('/')
@app.route('/<path:path>')
def serve_frontend(path=''):
    
    path = path.lstrip('/')  

    full_path = os.path.join(static_path, path)
    if path != '' and os.path.exists(os.path.join(static_path,path)):
        return send_from_directory(static_path, path)
    else:
        return send_from_directory(template_path, 'index.html')

   
def home():
    return redirect('http://localhost:5173/')


@app.route('/login')
def login():
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:5173/authorize'
    return oauth.flask_app.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = oauth.flask_app.authorize_access_token()
    nonce = session.get('nonce')

    user_info = oauth.flask_app.parse_id_token(token, nonce=nonce) 
    session['user'] = user_info
    return redirect('/')  # <-- redirect to frontend


@app.route('/api/user')
def get_user():
    user = session.get('user')
    if user:
        return jsonify({'loggedIn': True, 'email': user.get('email'), 'name': user.get('name')})
    return jsonify({'loggedIn': False})






@app.route('/logout')
def logout():
    session.clear()
    return redirect('http://localhost:5173/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
