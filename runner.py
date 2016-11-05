import os
import dondash
import cloudpassage
from flask import Flask
from flask import render_template
app = Flask(__name__)


halo_creds = cloudpassage.ApiKeyManager()
halo_session = cloudpassage.HaloSession(halo_creds.key_id, halo_creds.secret_key)

def fimScan(halo_session):
    agent_id = os.getenv("AGENT_ID")
    scan_types = scan_types = ["fim"]
    #scan_object = cloudpassage.Scan(halo_session)
    #scan_id = scan_object.initiate_scan(agent_id, scan_type)
    #results = scan_object.last_scan_results(agent_id, scan_type)
    #return results
    reporter = dondash.SecurityReporter()
    reporter.scan_all_modules(agent_id, scan_type)

    return

fimScan(halo_session)

def get_servers(halo_session):
    servers_object = cloudpassage.Server(halo_session)
    all_servers = servers_object.list_all()
    return all_servers

@app.route('/')
def home_page():
    #render_template('mainpage.html', results=fimScan(halo_session))
    return render_template('mainpage.html')
    #return

@app.route('/servers')
def server_list():
    return render_template('servers.html', servers=get_servers(halo_session))

#@app.route('/fim')
#def fim():
#    render_template('mainpage.html', fimScan(halo_session))
