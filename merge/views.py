from django.shortcuts import render
from django.http import JsonResponse
from .docMerge import mergeDocument
from .xml4doc import getData
from random import randint
from datetime import datetime

def getParamDefault(params, key, default):
    try:
        result = params.get(key)
        if result == None:
            return default
        elif result == "":
            return default
        else:
            return result.replace("+"," ")
    except:
        return default

def merge_raw(request):
    params = request.GET
    id = getParamDefault(params, "identifier", str(randint(0,10000)))
    flowFolder = getParamDefault(params, "flow_folder", "/Doc Merge/Flows")
    flow = getParamDefault(params, "flow", "md")
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/Doc Merge/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/Doc Merge/Output")
    payload = getParamDefault(params, "payload", None)
    payload_type = getParamDefault(params, "payload_type", None)
    test_case = getParamDefault(params, "test_case", None)
    data_folder = getParamDefault(params, "data_folder", "/Doc Merge/Test Data")
    data_file = getParamDefault(params, "data_file", None)
    data_root = getParamDefault(params, "data_root", None)
    branding_folder = getParamDefault(params, "branding_folder", "/Doc Merge/Branding")
    branding_file = getParamDefault(params, "branding_file", None)
    templateName = getParamDefault(params, "template", "AddParty.md")
    email = getParamDefault(params, "email", "andrew.elliott+epub@revolutionarysystems.co.uk")
    subs = getData(test_case=test_case, payload=payload, payload_type=payload_type, data_folder = data_folder, data_file=data_file)
    if data_root:
        subs = subs[data_root]
    if branding_file:
        branding_subs = getData(data_folder = branding_folder, data_file=branding_file)
        subs["branding"]= branding_subs
        subs["AgreementDate"]=datetime.now()
        
    return mergeDocument(flowFolder, flow, remoteTemplateFolder, templateName, id, subs, remoteOutputFolder, email=email)    

def merge(request):
    return JsonResponse(merge_raw(request))
    
