from merge.flow import *
from merge.merge_utils import *
from merge.xml4doc import *

creds = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}

def run():
	subs = getData(data_folder = "/Doc Merge/Test Data", data_file="testData3.xml", xform_folder = "/Doc Merge/Transforms", xform_file="ITP_9yds_TA.xml")["docroot"]#	flow1 = get_flow("/Doc Merge/Flows", "docx")
	print("Signatory")
	print(subs["agentSignatory"]["FirstName"])
	subs["roles"]=[
	        {"called":"Landlord", "values":["PropertyOwner", "AdditionalLandlord"]},
	        {"called":"Tenant", "values":["ManuallyInvitedTenant", "AdditionalTenant"]},
	        {"called":"Guarantor", "values":["Guarantor"]},
	 ]
	cwd = get_working_dir()
	flow2 = get_flow("/Doc Merge/Flows", "docx.txt")
#	print(flow2)
#	outcomes = process_flow(cwd, get_flow(flow_folder, flow), template_folder, template_name, uniq, subs, output_folder, email, email_credentials)
	#outcomes = process_flow(cwd, flow2, "/Doc Merge/Templates", "Tenancy_Agreement_v1_sect_1_2", "a100", subs, "/Doc Merge/Output", None, None)
#	outcomes = process_flow(docx_flow, "/Doc Merge/Templates", "Tenancy_Agreement", "a100", subs, "/Doc Merge/Output")
#	outcomes = process_flow(md_flow, "/Doc Merge/Templates", "AddParty_v3.md", "a200", subs, "/Doc Merge/Output", "andrew.elliott test@revolutionarysystems.co.uk", creds)
#	outcomes = process_flow(get_flow("html"), "/Doc Merge/Templates", "AddParty.html", "a300", subs, "/Doc Merge/Output")
	for step in outcomes:
		print(step["step"])
		print(step["outcome"])
