__author__ = 'ghoti'
import ConfigParser
import evelink.api
import evelink.corp
from flask import render_template
import os
import sqlite3

from postrack import app

EVESTATICDATADUMP = os.getcwd() + '/static.db'

@app.route('/system/<systemid>')
def system(systemid):
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

    poses = {}
    #{'state': 'anchored', 'standings_owner_id': 98114328, 'state_ts': 1388727107, 'online_ts': None, 'type_id': 20059, 'moon_id': 40287978, 'location_id': 30004553, 'id': 1011816170518L}
    #for pos in starbases.result:
    #    system = c.execute('select itemName from mapDenormalize where itemID={}'.format(starbases.result[pos]['location_id']))
    #    system = system.fetchone()
    #    if system not in systems:
    #        systems[starbases.result[pos]['location_id']] = system

    for moon in starbases.result:
        if int(starbases.result[moon]['location_id']) == int(systemid):
            print 'added', starbases.result[moon]['location_id']
            p = c.execute('select itemName from mapDenormalize where itemID={}'.format(starbases.result[moon]['moon_id']))
            p = p.fetchone()
            print p
            if starbases.result[moon]['id'] not in poses:
                poses[starbases.result[moon]['id']] = p
    print poses
    system = c.execute('select itemName from mapDenormalize where itemID={}'.format(systemid))
    system = system.fetchone()[0]

    return render_template("system.html", poses=poses, system=system)