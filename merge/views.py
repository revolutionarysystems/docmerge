from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .docMerge import mergeDocument
from .xml4doc import getData
from random import randint
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .merge_utils import get_local_dir, local_textfile_content, refresh_files
from traceback import format_exc

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

def merge_raw(request, method="POST"):
    if method=="GET":
        params = request.GET
    else:
        params = request.POST
    abs_uri = request.build_absolute_uri()            
    protocol, uri = abs_uri.split("://")
    site = protocol+"://"+uri.split("/")[0]+"/"
    id = getParamDefault(params, "identifier", str(randint(0,10000)))
    flowFolder = getParamDefault(params, "flow_folder", "/Doc Merge/Flows")
    flow = getParamDefault(params, "flow", "md")
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/Doc Merge/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/Doc Merge/Output")
    template_subfolder = getParamDefault(params, "template_subfolder", None)
    output_subfolder = getParamDefault(params, "output_subfolder", None)
    payload = getParamDefault(params, "payload", None)
    payload_type = getParamDefault(params, "payload_type", None)
    test_case = getParamDefault(params, "test_case", None)
    data_folder = getParamDefault(params, "data_folder", "/Doc Merge/Test Data")
    data_file = getParamDefault(params, "data_file", None)
    data_root = getParamDefault(params, "data_root", None)
    branding_folder = getParamDefault(params, "branding_folder", "/Doc Merge/Branding")
    branding_file = getParamDefault(params, "branding_file", None)
    xform_folder = getParamDefault(params, "xform_folder", "/Doc Merge/Transforms")
    xform_file = getParamDefault(params, "xform_file", None)
    templateName = getParamDefault(params, "template", "AddParty.md")
    email = getParamDefault(params, "email", "andrew.elliott+epub@revolutionarysystems.co.uk")
    templateName = templateName.replace("\\", "/")
    if template_subfolder:
        template_subfolder = template_subfolder.replace("\\", "/")
    subs = getData(test_case=test_case, payload=payload, payload_type=payload_type, local_data_folder="test_data", remote_data_folder = data_folder, data_file=data_file, xform_folder = xform_folder, xform_file=xform_file)
    if data_root:
        if data_root in subs:
            subs = subs[data_root]
        else:
            raise ValueError("Invalid data_root: " + data_root)
    if branding_file:
        branding_subs = getData(local_data_folder = "branding", remote_data_folder = branding_folder, data_file=branding_file)
        subs["branding"]= branding_subs
        subs["AgreementDate"]=datetime.now()
    subs["docs"]=[templateName]
    subs["roles"]=[
        {"called":"Landlord", "values":["PropertyOwner", "AdditionalLandlord"]},
        {"called":"Tenant", "values":["ManuallyInvitedTenant", "AdditionalTenant"]},
        {"called":"Guarantor", "values":["Guarantor"]},
    ]    
    subs["site"]= site
#    return mergeDocument(flowFolder, flow, remoteTemplateFolder, templateName, id, subs, remoteOutputFolder, email=email, payload=payload)    
    print("template name:", templateName)
    return mergeDocument(flowFolder, flow, remoteTemplateFolder, template_subfolder, templateName, id, subs, 
                        remoteOutputFolder, output_subfolder, email=email, payload=payload)    


def push_raw(request, method="POST"):
    print(">> push_raw")
    if method=="GET":
        params = request.GET
    else:
        params = request.POST
    abs_uri = request.build_absolute_uri()            
    protocol, uri = abs_uri.split("://")
    site = protocol+"://"+uri.split("/")[0]+"/"
    id = getParamDefault(params, "identifier", str(randint(0,10000)))
    flowFolder = getParamDefault(params, "flow_folder", "/Doc Merge/Flows")
    flow = getParamDefault(params, "flow", "md")
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/Doc Merge/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/Doc Merge/Output")
    payload = getParamDefault(params, "payload", None)
    templateName = getParamDefault(params, "template", "AddParty.md")
    template_subfolder = getParamDefault(params, "template_subfolder", None)
    output_subfolder = getParamDefault(params, "output_subfolder", None)
    email = getParamDefault(params, "email", "andrew.elliott+epub@revolutionarysystems.co.uk")
    templateName = templateName.replace("\\", "/")
    if template_subfolder:
        template_subfolder = template_subfolder.replace("\\", "/")
    sep = templateName.rfind("/")
    if sep >=0:
        path = templateName[:sep]
        templateName = templateName[sep+1:]
        if template_subfolder == None:
            template_subfolder = path
        else:
            template_subfolder+="/"+path
    subs={}
    subs["site"]= site
    return mergeDocument(flowFolder, flow, remoteTemplateFolder, template_subfolder, templateName, id, subs, 
                        remoteOutputFolder, output_subfolder, email=email, payload=payload, require_template=False)    


def error_response(ex):
    overall_outcome = {}
    overall_outcome["success"]=False
    overall_outcome["messages"]=[{"level":"error", "message": str(ex)}]
    overall_outcome["steps"]=[]
    overall_outcome["traceback"]=format_exc(5)

    return overall_outcome

def merge_raw_wrapped(request, method="POST"):
    try:
        return merge_raw(request, method=method)
    except Exception as ex:
        return error_response(ex)

@csrf_exempt
def merge(request):
    return JsonResponse(merge_raw_wrapped(request))
    
def push_raw_wrapped(request, method="POST"):
    try:
        return push_raw(request, method=method)
    except Exception as ex:
        return error_response(ex)

@csrf_exempt
def push(request):
    return JsonResponse(push_raw_wrapped(request))
    


def merge_get(request):
    return JsonResponse(merge_raw_wrapped(request, method="GET"))

def file_raw(request):
    params = request.GET
    filename = getParamDefault(params, "name", None)
    filepath = get_local_dir(getParamDefault(params, "path", "output"))
    #file_content=""
    #with open(filepath+filename) as file:
    #    for line in file:
    #        file_content+=(line+"\n")
    print(filepath,filename)
    return local_textfile_content(filename, filepath=filepath)

def file(request):
    return HttpResponse(file_raw(request))

def refresh(request):
    try:
        params = request.GET
        local = getParamDefault(params, "local", "templates")
        if local.find("templates")==0:
            remote_default = local.replace(local.split("/")[0],"/Doc Merge/Templates")
        elif local.find("flows")==0:
            remote_default = local.replace(local.split("/")[0],"/Doc Merge/Flows")
        elif local.find("branding")==0:
            remote_default = local.replace(local.split("/")[0],"/Doc Merge/Branding")
        elif local.find("test_data")==0:
            remote_default = local.replace(local.split("/")[0],"/Doc Merge/Test Data")
        elif local.find("transforms")==0:
            remote_default = local.replace(local.split("/")[0],"/Doc Merge/Transforms")
        else:
            remote_default = None    

        print("refresh:", local, remote_default)
        remote = getParamDefault(params, "remote", remote_default)
        files = refresh_files(remote, local)
        response = {"refreshed_files":files}
    except Exception as ex:
        response = error_response(ex)
    return JsonResponse(response)

