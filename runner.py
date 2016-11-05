import os
import cloudpassage
from flask import Flask
from flask import render_template
app = Flask(__name__)


halo_creds = cloudpassage.ApiKeyManager()
halo_session = cloudpassage.HaloSession(halo_creds.key_id, halo_creds.secret_key)


def get_servers(halo_session):
    servers_object = cloudpassage.Server(halo_session)
    all_servers = servers_object.list_all()
    return all_servers

def fimScan(halo_session):
    agent_id = os.getenv("AGENT_ID")
    scan_type = "fim"
    scan_object = cloudpassage.Scan(halo_session)
    scan_id = scan_object.initiate_scan(agent_id, scan_type)
    results = last_scan_results(agent_id, scan_type)
    return results

@app.route('/')
def home_page():
    #render_template('mainpage.html', results=fimScan(halo_session))
    return render_template('mainpage.html')
    #return

@app.route('/servers')
def server_list():
    return render_template('servers.html', servers=get_servers(halo_session))
