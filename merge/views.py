from django.shortcuts import render
from django.http import JsonResponse
from .docMerge import mergeDocument
from .xml4doc import getData
from random import randint

def getParamDefault(params, key, default):
    try:
    	result = params.get(key)
    	if result != None:
    	    return result.replace("+"," ")
    	else:
    	    return default
    except:
    	return default

def merge(request):
    params = request.GET
    id = getParamDefault(params, "ident", str(randint(0,10000)))
    flow = getParamDefault(params, "flow", "md")
    xml_payload = getParamDefault(params, "xml_payload", None)
    json_payload = getParamDefault(params, "json_payload", None)
    test_case = getParamDefault(params, "test_case", None)
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/Doc Merge/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/Doc Merge/Output")
    data_folder = getParamDefault(params, "data_folder", "/Doc Merge/Test Data")
    data_file = getParamDefault(params, "data_file", None)
    templateName = getParamDefault(params, "template", "AddParty.md")
    email = getParamDefault(params, "email", None)
    subs = getData(test_case=test_case, xml_payload=xml_payload, json_payload=json_payload, data_folder = data_folder, data_file=data_file)["ItpDocumentRequest"]
    response = mergeDocument(flow, remoteTemplateFolder, templateName, id, subs, remoteOutputFolder, email=email)    
    return JsonResponse(response)

#"andrew.elliott@revolutionarysystems.co.uk"

#doc_id="1BmoI4S_kqRDLGRb4t3k8iijIpz3NVBZrizqygfzHfns"
#subs = xml4doc2.getData()["ItpDocumentRequest"]
#subs["AgreementDate"]="2016-02-15"
#mergeDocument("docx", doc_id, "tenancy", "tenancy_01", subs)    
    
