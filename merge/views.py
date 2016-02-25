from django.shortcuts import render
from django.http import JsonResponse
from .docMerge import mergeDocument
from .xml4doc import getData
from random import randint

def getParamDefault(params, key, default):
    try:
    	result = params.get(key)
    	if result != None:
    	    return result
    	else:
    	    return default
    except:
    	return default

def merge(request):
    params = request.GET
    id = getParamDefault(params, "id", str(randint(0,10000)))
    flow = getParamDefault(params, "flow", "md")
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/Doc Merge/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/Doc Merge/Output")
    templateName = getParamDefault(params, "template", "AddParty.md")
    subs = getData()["ItpDocumentRequest"]
    response = mergeDocument(flow, remoteTemplateFolder, templateName, id, subs, remoteOutputFolder)    
    return JsonResponse(response)


#doc_id="1BmoI4S_kqRDLGRb4t3k8iijIpz3NVBZrizqygfzHfns"
#subs = xml4doc2.getData()["ItpDocumentRequest"]
#subs["AgreementDate"]="2016-02-15"
#mergeDocument("docx", doc_id, "tenancy", "tenancy_01", subs)    
    
