import sqlite3
import random
import sys

def make_bot(idx, userid, current_token=None, override=False):
    connection = sqlite3.connect('API.db')
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row

    cursor.execute('SELECT * FROM bots WHERE id = ?', (idx,))
    bots = [x for x in cursor.fetchall()]

    token = ''.join([random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.+:') for _ in range(16)])

    if bots and current_token is None:
        return None, 'Already exists.'

    elif bots:
        if current_token == dict(bots[0])['token'] or override:
            cursor.execute('UPDATE bots SET owner = ?, token = ? WHERE id = ?', (userid, token, idx))
            connection.commit()
            connection.close()
            return token, None

        else:
            return None, 'Please provide current token or contact an admin.'

    else:
        cursor.execute('INSERT INTO bots VALUES (?, 0, 0, ?, ?)', (idx, token, userid))
        connection.commit()
        connection.close()
        return token, None


if __name__ == '__main__':
    try:
        print(make_bot(*sys.argv[1:]))
    except TypeError:
        print('Required arguments: Bot ID and author ID. Optional arguments: token, override')
