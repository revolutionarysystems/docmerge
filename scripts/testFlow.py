from merge.flow import *

creds = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}

def run():
	subs = {}
#	flow1 = get_flow("/Doc Merge/Flows", "docx")
#	print(flow1)
	flow2 = get_flow("/Doc Merge/Flows", "docx.flow")
	outcomes = process_flow(flow2, "/Doc Merge/Templates", "Tenancy_Agreement", "a100", subs, "/Doc Merge/Output")
#	outcomes = process_flow(docx_flow, "/Doc Merge/Templates", "Tenancy_Agreement", "a100", subs, "/Doc Merge/Output")
#	outcomes = process_flow(md_flow, "/Doc Merge/Templates", "AddParty_v3.md", "a200", subs, "/Doc Merge/Output", "andrew.elliott test@revolutionarysystems.co.uk", creds)
#	outcomes = process_flow(get_flow("html"), "/Doc Merge/Templates", "AddParty.html", "a300", subs, "/Doc Merge/Output")
	for step in outcomes:
		print(step["step"])
		print(step["outcome"])
