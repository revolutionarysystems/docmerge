from merge.flow import *
from merge.merge_utils import *
from merge.xml4doc import *
from merge.models import ClientConfig
import string
from merge.gd_service import ensure_initialised

creds = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}

compound_TA = {
	"data_file":"testData2.xml",
	"xform_file":"ITP_9yds_TA.xml",
	"flow_file":"comp_docx.txt",
	"template_subfolder":None,
	"template_file":"Wizard Move in documents/Tenancy Agreements/AST/AST.json",
	"payload":"<email>sample</email>",
	"uniq":"1011",
	"expected_outcomes": {
		'link_Generate_pdf': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
		'id_Upload_pdf': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
		'id': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
		'success': True, 
		'messages': [], 
		'link_Merge_docx': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.docx', 
		'mimeType_Upload_to_gdoc': 'application/vnd.google-apps.document', 
		'mimeType_Upload_pdf': 'application/pdf', 
		'id_Upload_to_gdoc': '1sGqmQ4taa_HhMF4Z9npDJbm3NYA-1FtvlnGAe9Eb9dI', 
		'mimeType': 'application/pdf', 
		'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
		'steps': [
			{
				'step': 'Merge docx', 
				'outcome': {
					'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.docx', 
					'file': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.docx'
				}
			}, {
				'step': 'Upload to gdoc', 
				'outcome': {
					'kind': 'drive#file', 
					'id': '1sGqmQ4taa_HhMF4Z9npDJbm3NYA-1FtvlnGAe9Eb9dI', 
					'mimeType': 
					'application/vnd.google-apps.document', 
					'name': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.docx'
				}
			}, {
				'step': 'Generate pdf', 
				'outcome': {
					'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
					'file': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.pdf'
				}
			}, {
				'step': 'Upload pdf', 
				'outcome': {
					'kind': 'drive#file', 
					'id': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
					'mimeType': 'application/pdf', 
					'name': 'Sandbox-cmpnd_doc_10101.pdf'
				}
			}
		]
	}

}


plain_TA = {
	"data_file":"testData2.xml",
	"xform_file":"ITP_9yds_email.xml",
	"flow_file":"docx.txt",
	"template_subfolder":None,
	"template_file":"Wizard Move in documents/Tenancy Agreements/AST/Copy of Tenancy_Agreement_v1_Section_1_2_3_4_5_6_DPS",
	"payload":"<email>sample</email>",
	"uniq":"1012",
	"expected_outcomes": {
		'link_Generate_pdf': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
		'id_Upload_pdf': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
		'id': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
		'success': True, 
		'messages': [], 
		'link_Merge_docx': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.docx', 
		'mimeType_Upload_to_gdoc': 'application/vnd.google-apps.document', 
		'mimeType_Upload_pdf': 'application/pdf', 
		'id_Upload_to_gdoc': '1sGqmQ4taa_HhMF4Z9npDJbm3NYA-1FtvlnGAe9Eb9dI', 
		'mimeType': 'application/pdf', 
		'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
		'steps': [
			{
				'step': 'Merge docx', 
				'outcome': {
					'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.docx', 
					'file': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.docx'
				}
			}, {
				'step': 'Upload to gdoc', 
				'outcome': {
					'kind': 'drive#file', 
					'id': '1sGqmQ4taa_HhMF4Z9npDJbm3NYA-1FtvlnGAe9Eb9dI', 
					'mimeType': 
					'application/vnd.google-apps.document', 
					'name': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.docx'
				}
			}, {
				'step': 'Generate pdf', 
				'outcome': {
					'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
					'file': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.pdf'
				}
			}, {
				'step': 'Upload pdf', 
				'outcome': {
					'kind': 'drive#file', 
					'id': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
					'mimeType': 'application/pdf', 
					'name': 'Sandbox-cmpnd_doc_10101.pdf'
				}
			}
		]
	}

}


plain_TA_S7 = {
	"data_file":"testData2.xml",
	"xform_file":"ITP_9yds_email.xml",
	"flow_file":"docx.txt",
	"template_subfolder":"/Wizard Move in documents/Tenancy Agreements/AST",
	"template_file":"Copy of Tenancy_Agreement_v1_sched_7",
	"payload":None,
	"uniq":"1012",
	"expected_outcomes": {
		'link_Generate_pdf': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
		'id_Upload_pdf': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
		'id': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
		'success': True, 
		'messages': [], 
		'link_Merge_docx': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.docx', 
		'mimeType_Upload_to_gdoc': 'application/vnd.google-apps.document', 
		'mimeType_Upload_pdf': 'application/pdf', 
		'id_Upload_to_gdoc': '1sGqmQ4taa_HhMF4Z9npDJbm3NYA-1FtvlnGAe9Eb9dI', 
		'mimeType': 'application/pdf', 
		'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
		'steps': [
			{
				'step': 'Merge docx', 
				'outcome': {
					'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.docx', 
					'file': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.docx'
				}
			}, {
				'step': 'Upload to gdoc', 
				'outcome': {
					'kind': 'drive#file', 
					'id': '1sGqmQ4taa_HhMF4Z9npDJbm3NYA-1FtvlnGAe9Eb9dI', 
					'mimeType': 
					'application/vnd.google-apps.document', 
					'name': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.docx'
				}
			}, {
				'step': 'Generate pdf', 
				'outcome': {
					'link': 'localhost:8001file/?name=Sandbox-cmpnd_doc_10101.pdf', 
					'file': 'C:\\Users\\Andrew\\Documents\\GitHub\\docmerge/merge/output/Sandbox-cmpnd_doc_10101.pdf'
				}
			}, {
				'step': 'Upload pdf', 
				'outcome': {
					'kind': 'drive#file', 
					'id': '0B-R1VJ7CNz2Zc1pRX0JSbnBNOFE', 
					'mimeType': 'application/pdf', 
					'name': 'Sandbox-cmpnd_doc_10101.pdf'
				}
			}
		]
	}

}

chartest_TA = {
	"data_file":"testData3.xml",
	"xform_file":"ITP_9yds_TA.xml",
	"flow_file":"docx.txt",
	"template_subfolder":"/Sandbox",
	"template_file":"Character Sampler",
	"payload":None,
	"uniq":"11",
	"expected_outcomes": {}

}

TA = {
	"data_file":"testData3.xml",
	"xform_file":"ITP_9yds_email.xml",
	"flow_file":"comp_docx_a.txt",
	"template_subfolder":"/Wizard Move in documents/Tenancy Agreements/AST",
	"template_file":"AST.json",
	"payload":None,
	"uniq":"13",
	"expected_outcomes": {}

}



ECVTNC = {
	"data_file":"EchoCentral-Glanty.xml",
	"xform_file":None,
	"flow_file":"comp_docx.txt",
	"template_subfolder":"/Sandbox",
	"template_file":"Compound.json",
	"payload":None,
	"uniq":"14",
	"expected_outcomes": {}

}

ECVSL = {
	"data_file":"EchoCentral-Glanty.xml",
	"xform_file":None,
	"flow_file":"comp_docx_2.flo",
	"template_subfolder":"/Contracts",
	"template_file":"SLS.json",
	"payload":None,
	"uniq":"1.2",
	"expected_outcomes": {}
}


ECVInv = {
	"data_file":"EchoCentral-Glanty-Invoice.xml",
	"xform_file":None,
	"flow_file":"docx_2.flo",
	"template_subfolder":"/Invoices",
	"template_file":"Invoice.json",
	"payload":None,
	"uniq":"1.1",
	"expected_outcomes": {}
}


ECVTNC_2 = {
	"data_file":None,
	"payload_type": "params",
	"params": {"product":"EchoProd", "vendor.name":"ECVL"},
	"xform_file":None,
	"flow_file":"docx.flo",
	"template_subfolder":"/Contracts",
	"template_file":"Copy of Echo Central Ts and Cs",
	"payload":None,
	"uniq":"1.0",
	"expected_outcomes": {}

}

ITABN = {
	"data_file":"book.xml",
	"xform_file":None,
	"flow_file":"comp_docx.flo",
	"template_subfolder":"/ITABN",
	"template_file":"Book2.json",
	"payload":None,
	"uniq":"1.1",
	"expected_outcomes": {}
}

Sample = {
	"data_file":"sample.xml",
	"xform_file":None,
	"flow_file":"docx_2.flo",
	"template_subfolder":"",
	"template_file":"Sample Document",
	"payload":None,
	"uniq":"1.2",
	"expected_outcomes": {}
}

Sample = {
	"data_file":"sample.xml",
	"xform_file":None,
	"flow_file":"test.txt",
	"template_subfolder":"",
	"template_file":"Sample Document",
	"payload":None,
	"uniq":"1.2",
	"expected_outcomes": {}
}



Strong = {
	"data_file":"strongman.xml",
	"xform_file":None,
	"flow_file":"docx_2.flo",
	"template_subfolder":"",
	"template_file":"Job Description",
	"payload":None,
	"uniq":"1.2",
	"expected_outcomes": {}
}


ITABN_Summary = {
	"data_file":"book.xml",
	"xform_file":None,
	"flow_file":"docx.flo",
	"template_subfolder":"/ITABN",
	"template_file":"ITABN Summary",
	"payload":None,
	"uniq":"1.1",
	"expected_outcomes": {}
}

Library = {
	"data_file":"sample.xml",
	"xform_file":None,
	"flow_file":"md.flo",
	"template_subfolder":"/EP Documents",
	"template_file":"library_page.md",
	"payload":None,
	"uniq":"1",
	"expected_outcomes": {}
}


EPDemo = {
	"data_file":"sample.xml",
	"xform_file":None,
	"flow_file":"docx.flo",
	"template_subfolder":"",
	"template_file":"Sample Document",
	"payload":None,
	"uniq":"122",
	"expected_outcomes": {}
}



def get(dct, item):
	try:
		return dct[item]
	except KeyError:
		return None


def test_data(config, test_case):
	subs = getData(config, remote_data_folder = "/Echo Publish Demo/Test Data", local_data_folder = "test_data", 
	                   data_file=test_case["data_file"], xform_folder = "/Doc Merge/Transforms", 
	                   xform_file=test_case["xform_file"])["docroot"]#	flow1 = get_flow("/Doc Merge/Flows", "docx")
	print(subs)
	print(type(subs))

#	print(subs["Request"]["Guarantors"])
#	print(subs["Request"]["Landlords"])


def test_flow(config, test_case):
	remote = "/Doc Merge"
	subs = getData(config, remote_data_folder = remote+"/Test Data", local_data_folder = "test_data", 
	                   data_file=test_case["data_file"], payload_type=get(test_case,"payload_type"), 
	                   params=get(test_case,"params"), xform_folder = remote+"/Transforms", 
	                   xform_file=test_case["xform_file"])["docroot"]#	flow1 = get_flow("/Doc Merge/Flows", "docx")
	subs["site"]="localhost:8001"
	cwd = get_working_dir()
	flow = get_flow(cwd, config, "flows", remote+"/Flows", test_case["flow_file"])
	outcomes = process_flow(cwd, config, flow, remote+"/Templates", 
		test_case["template_subfolder"], 
		test_case["template_file"], 
		test_case["uniq"], subs, remote+"/Output", None, None, None, 
		payload=test_case["payload"])
#	assert (outcomes["success"]==(test_case["expected_outcomes"]["success"]))
	#assert (len(outcomes["steps"])==(len(test_case["expected_outcomes"]["steps"])))
	for step in outcomes["steps"]:
		print(step["step"])
		print(step["time"])
		print(step["outcome"])
	print(outcomes["success"])
	print(outcomes["messages"])
	try:
		print(outcomes["traceback"])
	except:
		pass

def run():
	config = ClientConfig()
	config.tenant="."
	ensure_initialised(config)
#	test_flow(compound_TA)	test_flow(ECVInv)

#	test_data(config, TA)
	test_flow(config, Sample)
#	test_flow(Library)
#	test_flow(ECVSL)
#	test_flow(plain_TA)
#	test_flow(plain_TA_S7)
#	test_data(EPDemo)



