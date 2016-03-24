from merge.flow import *
from merge.merge_utils import *

creds = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}

def run():
	subs = {}
#	flow1 = get_flow("/Doc Merge/Flows", "docx")
#	print(flow1)
	cwd = get_working_dir()
	flow2 = get_flow("/Doc Merge/Flows", "docx.txt")
#	outcomes = process_flow(cwd, get_flow(flow_folder, flow), template_folder, template_name, uniq, subs, output_folder, email, email_credentials)
	outcomes = process_flow(cwd, flow2, "/Doc Merge/Templates", "Deposit_v1", "a100", subs, "/Doc Merge/Output", None, None)
#	outcomes = process_flow(docx_flow, "/Doc Merge/Templates", "Tenancy_Agreement", "a100", subs, "/Doc Merge/Output")
#	outcomes = process_flow(md_flow, "/Doc Merge/Templates", "AddParty_v3.md", "a200", subs, "/Doc Merge/Output", "andrew.elliott test@revolutionarysystems.co.uk", creds)
#	outcomes = process_flow(get_flow("html"), "/Doc Merge/Templates", "AddParty.html", "a300", subs, "/Doc Merge/Output")
	for step in outcomes:
		print(step["step"])
		print(step["outcome"])
