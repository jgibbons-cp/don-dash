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

    def getHaloPolicyBody(self, fqpOfDataFile):
        jsonData = None

        try:
            with open(fqpOfDataFile) as jDataFile:
                jsonData = json.load(jDataFile)
        except IOError as err:
            error_message = "Unable to load user server ID data from file: %s" % err
            print error_message
            sys.exit(-1)

        return jsonData

    def scan_all_modules(self, agent_id):
        #fimPolicyName = "CoreSystemFilesUbuntu_v2.1-FIM.json"
        #fimPolicyLocation = "/tmp"
        #fqpToPolicyFile = "%s/%s" % (fimPolicyLocation, fimPolicyName)
        #scan_types = ["csm", "svm", "fim"]
        #scan_types = ["csm", "svm"]
        scan_types = ["csm"]
        command_ids = []
        unfinished_statuses = ['queued', 'pending']
        server_module = cloudpassage.Server(self.halo_session)

        #cpFIM_Object = cloudpassage.FimPolicy(self.halo_session)
        #cpFIM_PolicyBody = self.getHaloPolicyBody(fqpToPolicyFile)
        #print "This is policy body %s" % cpFIM_PolicyBody
        #cpFIM_PolicyID = cpFIM_Object.create(cpFIM_PolicyBody)
        #print "This is FIM policy ID %s" % cpFIM_PolicyID
        #cpFIM_BaselineObject = cloudpassage.FimBaseline(self.halo_session)
        #cpFIM_BaselineID = cpFIM_BaselineObject.create(cpFIM_PolicyID, agent_id)
        #print "this is baseline id %s" % cpFIM_BaselineID

        scan_module = cloudpassage.Scan(self.halo_session)
        raw_scan_results = []
        # Initiate scans
        #print "Initiating scans for agent %s" % agent_id
        for scan_type in scan_types:
            command_id = scan_module.initiate_scan(agent_id, scan_type)["id"]
            command_ids.append(command_id)
            #print command_id
        # Wait until all are complete
        #print "Waiting for all scan jobs to be run"
        while len(command_ids) > 0:
            time.sleep(30)
            for command_id in command_ids:
                #print "Checking status of command %s" % command_id
                status = server_module.command_details(agent_id, command_id)
                if status not in unfinished_statuses:
                    command_ids.remove(command_id)
        # Get results
        #print "Getting scan results"
        for scan_type in scan_types:
            try:
                results = scan_module.last_scan_results(agent_id, scan_type)
                print "This is dir listing"
                if os.path.isfile('/app/.cloudpassage.yml') is False:
                    os.listdir("./")
                    with open("/app/.cloudpassage.yml", 'a') as yDataFile:
                        dataString = "FIM_Environment_Variables:"
                        yDataFile.write(dataString)
                        dataString = "  CONTAINER_SERVER_ID : %s" % results["id"]
                        yDataFile.write(dataString)
                        yDataFile.close()
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
        ##print raw_scan_results
        #with open("testFile", 'w') as fout:
        #    pp = pprint.PrettyPrinter(stream=fout)
        #    pp.pprint(raw_scan_results)
