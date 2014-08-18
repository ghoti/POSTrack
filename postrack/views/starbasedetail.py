__author__ = 'ghoti'
import ConfigParser
import evelink.api
import evelink.corp
from flask import render_template
import os
import sqlite3

from postrack import app

EVESTATICDATADUMP = os.getcwd() + '/static.db'

@app.route('/detail/<posid>')
def pos(posid):
    config = ConfigParser.ConfigParser()
    for f in os.listdir('postrack/config/'):
        if f.endswith('.cfg'):
            config.readfp(open('postrack/config/' + f))
            keyid = config.get('api', 'keyid')
            vcode = config.get('api', 'vcode')
    api = evelink.api.API(api_key=(keyid, vcode))
    corp = evelink.corp.Corp(api=api)
    conn = sqlite3.connect(EVESTATICDATADUMP)
    c = conn.cursor()

    pos = corp.starbase_details(starbase_id=posid)

    print pos.result
    fuel = {}

    for i in pos.result['fuel']:
        print pos.result['fuel'][i]
        fuel[i] = pos.result['fuel'][i]

    return render_template('detail.html', fuel=fuel)