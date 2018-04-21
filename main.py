from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

import sqlite3

app = FlaskAPI(__name__)

@app.route('/<int:idx>')
@app.route('/<int:idx>/', methods=['GET', 'POST'])
def update(idx):
    with sqlite3.connect('API.db') as connection:

        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row

        cursor.execute('SELECT * FROM bots WHERE id = ?', (idx,))
        bot = [x for x in cursor.fetchall()]

        if len(bot) != 1:
            return '', status.HTTP_404_NOT_FOUND

        members = dict(bot[0])['members']
        guilds = dict(bot[0])['guilds']

        if request.method == 'POST':

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

app.run(host='0.0.0.0', port=8080, threaded=True, ssl_context=('/etc/letsencrypt/live/jellywx.co.uk/fullchain.pem', '/etc/letsencrypt/live/jellywx.co.uk/privkey.pem'))
