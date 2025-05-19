from flask import Flask, jsonify, redirect, send_from_directory, url_for, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
import os
from flask_cors import CORS
import requests


static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
template_path = static_path


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


# Route to get NYT API key
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
    user = session.get('user')
    if user:
        return f"<h2>Logged in as {user['email']}</h2><a href='/logout'>Logout</a>"
    return '<a href="/login">Login with Dex</a>'

@app.route('/login')
def login():
    session['nonce'] = nonce
    redirect_uri = 'http://localhost:8000/authorize'
    return oauth.flask_app.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize')
def authorize():
    token = oauth.flask_app.authorize_access_token()
    nonce = session.get('nonce')

    user_info = oauth.flask_app.parse_id_token(token, nonce=nonce)  # or use .get('userinfo').json()
    session['user'] = user_info
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)),debug=debug_mode)