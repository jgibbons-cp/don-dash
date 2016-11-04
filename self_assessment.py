import dondash
import os

reporter = dondash.SecurityReporter()
agent_id = os.getenv("AGENT_ID")
scan_types = ["csm", "svm"]

reporter.scan_all_modules(agent_id, scan_types)
