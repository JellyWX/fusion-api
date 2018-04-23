from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import sqlite3
import sys

subdomain = 'api'
domain = 'jellywx.co.uk'

app = FlaskAPI(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'
app.config['SERVER_NAME'] = domain
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['10 per minute']
)

@app.route('/', methods=['GET'], subdomain=subdomain)
@cross_origin()
def get_bots():
    with sqlite3.connect('API.db') as connection:
        
        cursor = connection.cursor()
        
        cursor.execute('SELECT id FROM bots')
        return [x for x in cursor.fetchall()]

    
@app.route('/int:idx')
@app.route('/<int:idx>/', methods=['GET', 'POST'], subdomain=subdomain)
@cross_origin()
def update(idx):
    with sqlite3.connect('API.db') as connection:

        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row

        cursor.execute('SELECT * FROM bots WHERE id = ?', (idx,))
        bot = [x for x in cursor.fetchall()]

        if len(bot) != 1:
            print('Failed lookup')
            return '', status.HTTP_404_NOT_FOUND

        members = dict(bot[0])['members']
        guilds = dict(bot[0])['guilds']

        if request.method == 'POST':

            token = dict(bot[0])['token']

            if not token == str(request.data.get('token')):
                return '', status.HTTP_401_UNAUTHORIZED

            try:
                members = int(request.data.get('members'))
            except:
                pass

            try:
                guilds = int(request.data.get('guilds'))
            except:
                pass

            cursor.execute('UPDATE bots SET members = ?, guilds = ? WHERE id = ?', (members, guilds, idx))
            connection.commit()

    return {'members' : members, 'guilds' : guilds}

if 'debug' in sys.argv:
    app.run(debug=True)
else:
    app.run(host=domain, port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/{}.{}/fullchain.pem'.format(subdomain, domain), '/etc/letsencrypt/live/{}.{}/privkey.pem'.format(subdomain, domain)))
