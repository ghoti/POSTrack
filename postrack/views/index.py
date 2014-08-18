__author__ = 'ghoti'
import ConfigParser
import evelink.api
import evelink.corp
from flask import render_template
import os
import sqlite3

from postrack import app

EVESTATICDATADUMP = os.getcwd() + '/static.db'

@app.route('/')
def list():
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
    starbases = corp.starbases()

    systems = {}
    #{'state': 'anchored', 'standings_owner_id': 98114328, 'state_ts': 1388727107, 'online_ts': None, 'type_id': 20059, 'moon_id': 40287978, 'location_id': 30004553, 'id': 1011816170518L}
    for pos in starbases.result:
        system = c.execute('select itemName from mapDenormalize where itemID={}'.format(starbases.result[pos]['location_id']))
        system = system.fetchone()
        print system
        if system not in systems:
            systems[starbases.result[pos]['location_id']] = system

    return render_template("systems.html", systems=systems)