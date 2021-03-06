import cloudpassage
import pprint
import time
import json
import os
import sys

class SecurityReporter(object):
    def __init__(self):
        self.halo_creds = cloudpassage.ApiKeyManager()
        self.halo_session = cloudpassage.HaloSession(self.halo_creds.key_id,
                                                     self.halo_creds.secret_key)
        return

    def create_fim_baseline(self, agent_id):
        if os.environ.get("CONTAINER_FIM_POLICY_ID", -1) == -1:
            print "Critical: Failed to create FIM baseline, container FIM policy ID not set..."
        else:
            containerFIM_PolicyID = os.environ["CONTAINER_FIM_POLICY_ID"]

        cpFIM_BaselineObject = cloudpassage.FimBaseline(self.halo_session)
        cpFIM_BaselineID = cpFIM_BaselineObject.create(containerFIM_PolicyID, agent_id)

        baselineStatus = ""
        desiredStatus = "Active"
        INCREMENTOR = 1

        while baselineStatus != desiredStatus:
            counter = 0
            baselineStatus = "Active"
            results = cpFIM_BaselineObject.list_all(containerFIM_PolicyID)
            print "Checking if baseline is active...\n"
            for index in results:
                baselineStatus = results[counter]["status"]
                if baselineStatus != desiredStatus:
                    baselineStatus = results[counter]["status"]
                    print "Baseline is %s... will check again shortly...\n" % baselineStatus
                    time.sleep(30)
                    break
                counter = counter + INCREMENTOR
        print "Baseline is active...\n"

        return

    def scan_all_modules(self, agent_id, scan_types):

        command_ids = []
        unfinished_statuses = ['queued', 'pending']
        server_module = cloudpassage.Server(self.halo_session)

        scan_module = cloudpassage.Scan(self.halo_session)
        raw_scan_results = []
        # Initiate scans
        # print "Initiating scans for agent %s" % agent_id
        for scan_type in scan_types:
            command_id = scan_module.initiate_scan(agent_id, scan_type)["id"]
            command_ids.append(command_id)
            # print command_id
        # Wait until all are complete
        # print "Waiting for all scan jobs to be run"
        while len(command_ids) > 0:
            time.sleep(30)
            for command_id in command_ids:
                # print "Checking status of command %s" % command_id
                status = server_module.command_details(agent_id, command_id)
                if status not in unfinished_statuses:
                    command_ids.remove(command_id)
        # Get results
        for scan_type in scan_types:
            try:
                results = scan_module.last_scan_results(agent_id, scan_type)
            except cloudpassage.CloudPassageValidation as e:
                message = "Error encountered: %s" % str(e)
                result = {"result": message}
            raw_scan_results.append(results)
        # Process and print scan results
        pretty = self.print_pretty_scans(raw_scan_results)
        return

    def print_pretty_scans(self, raw_scan_results):
        pp = pprint.PrettyPrinter()
        pp.pprint(raw_scan_results)
