from merge.flow import *
from merge.merge_utils import *
from merge.xml4doc import *

creds = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}

flow_test_case = {
	"data_file":"testData25-1.xml",
	"xform_file":"ITP_9yds_TA.xml",
	"flow_file":"comp_docx.txt",
	"template_subfolder":"/Sandbox",
	"template_file":"cmpnd_doc.json",
	"payload":"<email>sample</email>",
	"uniq":"10101"
}

def test_flow(test_case):
	subs = getData(remote_data_folder = "/Doc Merge/Test Data", local_data_folder = "test_data", data_file=test_case["data_file"], xform_folder = "/Doc Merge/Transforms", xform_file="ITP_9yds_email.xml")["docroot"]#	flow1 = get_flow("/Doc Merge/Flows", "docx")
	subs["site"]="localhost:8001"
	#print(subs)
	print(subs["Request"]["SubjectDocument"]["EndDate"])
	print(subs["Tenancy"]["EndDate"])
	print(type(subs["Request"]["SubjectDocument"]["EndDate"]))
	print(type(subs["Tenancy"]["EndDate"]))
	cwd = get_working_dir()
	flow2 = get_flow(cwd,"flows", "/Doc Merge/Flows", "comp_docx.txt")
#	outcomes = process_flow(cwd, flow2, "/Doc Merge/Templates", "/Sandbox", 
#		"cmpnd_doc.json", test_case["uniq"], subs, "/Doc Merge/Output", None, None, None, payload=test_case["payload"])
#	for step in outcomes["steps"]:
#		print(step["step"])
#		print(step["outcome"])

def run():
	test_flow(flow_test_case)

def run0():
	test = flow_test_case
	payload="<email>sample</email>"
	subs = getData(remote_data_folder = "/Doc Merge/Test Data", local_data_folder = "test_data", data_file="testData3.xml", xform_folder = "/Doc Merge/Transforms", xform_file="ITP_9yds_TA.xml")["docroot"]#	flow1 = get_flow("/Doc Merge/Flows", "docx")
	subs["site"]="localhost:8001"
	cwd = get_working_dir()
	#flow2 = get_flow(cwd,"flows", "/Doc Merge/Flows", "pet.txt")
	flow2 = get_flow(cwd,"flows", "/Doc Merge/Flows", "comp_docx.txt")
#	print(flow2)
#	outcomes = process_flow(cwd, get_flow(flow_folder, flow), template_folder, template_name, uniq, subs, output_folder, email, email_credentials)
#                     process_flow(cwd, flow, template_remote_folder, template_subfolder, template_name, uniq, subs, output_folder, output_subfolder, you, email_credentials, payload=None, require_template=True):
	outcomes = process_flow(cwd, flow2, "/Doc Merge/Templates", "/Sandbox", "cmpnd_doc.json", test["uniq"], subs, "/Doc Merge/Output", None, None, None, payload=payload)
#	outcomes = process_flow(docx_flow, "/Doc Merge/Templates", "Tenancy_Agreement", "a100", subs, "/Doc Merge/Output")
#	outcomes = process_flow(md_flow, "/Doc Merge/Templates", "AddParty_v3.md", "a200", subs, "/Doc Merge/Output", "andrew.elliott test@revolutionarysystems.co.uk", creds)
#	outcomes = process_flow(get_flow("html"), "/Doc Merge/Templates", "AddParty.html", "a300", subs, "/Doc Merge/Output")
	#print(outcomes)
	for step in outcomes["steps"]:
		print(step["step"])
		print(step["outcome"])

#def run():
#	print("ok")