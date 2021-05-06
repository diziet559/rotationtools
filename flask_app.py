

import rotationtools
import damage
import json
import io

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def number(s):
    try:
        return int(s)
    except:
        pass
    try:
        return float(s)
    except:
        return 0



app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return app.send_static_file('simulator.html')

@app.route('/rotation/<string:rot>')
def rotplot(rot):
    r = rotationtools.rotationplot('bm')
    r.init_fig()
    r.melee.haste = 1.05 # drums
    r.ranged.haste = r.melee.haste * 1.2 * 1.15 # serpent + quiver
    r.change_haste()
    r.add_rotation(rot)
    r.complete_fig('Rotation: '+rot, legend=0)

    output = io.BytesIO()
    FigureCanvas(plt.gcf()).print_png(output)
    plt.close(plt.gcf())
    res = Response(output.getvalue(), mimetype='image/png')
    res.set_cookie('rotation', rot, max_age=60*60*24*365)

    return res

@app.route('/test', methods = ['POST', 'GET'])
def test():
    #data = {'success':'true','message':'The Command Completed Successfully'};

    #myjson = json.loads(data);

    return 'Muh' #str(myjson);

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    return jsdata@app.route('/sim')

@app.route('/sim')
def sim():
    fight_length = 180

    r = rotationtools.rotationplot()
    r.loadData('gear.yaml')
    r.loadSet('Preraid')
    #r.character.gear.addWeapon(r.data, 'Wolfslayer', 'RangedWeapons')
    #r.character.gear.addWeapon(r.data, 'QuantumBlade', 'Twohanders')

    r.character.gear.agi = number(request.args.get('agi'))
    r.character.gear.total_rap = number(request.args.get('rap'))
    r.character.gear.total_map = number(request.args.get('map'))
    r.character.gear.crit_rating = number(request.args.get('cr'))
    r.character.gear.hit_rating = number(request.args.get('hr'))
    r.character.gear.haste_rating = number(request.args.get('haste'))

    rspd = number(request.args.get('rspd'))
    rdps = number(request.args.get('rdps'))
    mspd = number(request.args.get('mspd'))
    mdps = number(request.args.get('mdps'))

    r.character.gear.rweapon = damage.Weapon(rdps, rspd)
    r.character.gear.mweapon = damage.Weapon(mdps, mspd)
    #r.reloadChar()

    t, dps, rhaste, mhaste = r.mean_dps(fight_length, weaving=1, use_drums = 1, silent = 1)
    t_sparse = []
    dps_sparse = []
    for n, val in enumerate(dps):
        if n==0 or n==len(dps)-1 or dps[n-1] != dps[n] or dps[n] != dps[n+1]:
            t_sparse.append(t[n])
            dps_sparse.append(round(dps[n]))

    #session['t'] = t_sparse
    #session['dps'] = dps_sparse

    mean_dps = sum(dps)/len(dps)

    result = {}
    result['success'] = True
    result['status'] = "Simulation completed successfully."
    result['sim_length'] = len(dps)
    result['data_length'] = len(dps_sparse)
    result['t'] = t_sparse
    result['dps'] = dps_sparse

    msg = 'Simulation complete. Average dps: {dps:.0f}.'.format(dps=mean_dps)

    res = Response(msg, mimetype='text/plain')
    res.set_cookie('sim', json.dumps(result))

    return res

@app.route('/dpsplot')
def dpsplot():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    cookie = request.cookies.get('sim')
    data = json.loads(cookie)
    t = data.get('t', 0)
    dps = data.get('dps', 0)
    ax.plot(t, dps)
    ax.set_xlabel('time [s]')
    ax.set_ylabel('dps')
    ax.set_xlim([0, max(t)])

    output = io.BytesIO()
    FigureCanvas(plt.gcf()).print_png(output)
    plt.close(fig)

    res = Response(output.getvalue(), mimetype='image/png')
    res.cache_control.max_age = 0
    return res #json.dumps(data.get('dps', 0))#res