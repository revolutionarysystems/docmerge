import os
import zipfile
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .docMerge import mergeDocument
from .xml4doc import getData
from random import randint
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
#from .merge_utils import get_local_dir
from .resource_utils import get_working_dir, get_local_txt_content,get_local_dir, refresh_files, zip_local_dirs, remote_link
from traceback import format_exc
from dash.forms import UploadZipForm
from .config import remote_library, gdrive_root, local_root

def getParamDefault(params, key, default, preserve_plus=False):
    try:
        result = params.get(key)
        if result == None:
            return default
        elif result == "":
            return default
        else:
            if preserve_plus:
                return result
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
    flowFolder = getParamDefault(params, "flow_folder", "/"+gdrive_root+"/Flows")
    flow = getParamDefault(params, "flow", "md")
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/"+gdrive_root+"/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/"+gdrive_root+"/Output")
    template_subfolder = getParamDefault(params, "template_subfolder", None)
    output_subfolder = getParamDefault(params, "output_subfolder", None)
    payload = getParamDefault(params, "payload", None, preserve_plus=True)
    payload_type = getParamDefault(params, "payload_type", None)
    test_case = getParamDefault(params, "test_case", None)
    data_folder = getParamDefault(params, "data_folder", "/"+gdrive_root+"/Test Data")
    data_file = getParamDefault(params, "data_file", None)
    data_root = getParamDefault(params, "data_root", None)
    branding_folder = getParamDefault(params, "branding_folder", "/"+gdrive_root+"/Branding")
    branding_file = getParamDefault(params, "branding_file", None)
    xform_folder = getParamDefault(params, "xform_folder", "/"+gdrive_root+"/Transforms")
    xform_file = getParamDefault(params, "xform_file", None)
    templateName = getParamDefault(params, "template", "AddParty.md")
    email = getParamDefault(params, "email", "andrew.elliott+epub@revolutionarysystems.co.uk")
    templateName = templateName.replace("\\", "/")
    if template_subfolder:
        template_subfolder = template_subfolder.replace("\\", "/")
    subs = getData(test_case=test_case, payload=payload, payload_type=payload_type, params = params, local_data_folder="test_data", remote_data_folder = data_folder, data_file=data_file, xform_folder = xform_folder, xform_file=xform_file)
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
    #subs["roles"]=[
    #    {"called":"Landlord", "values":["PropertyOwner", "AdditionalLandlord"]},
    #    {"called":"Tenant", "values":["ManuallyInvitedTenant", "AdditionalTenant"]},
    #    {"called":"Guarantor", "values":["Guarantor"]},
    #]    
    subs["site"]= site
#    return mergeDocument(flowFolder, flow, remoteTemplateFolder, templateName, id, subs, remoteOutputFolder, email=email, payload=payload)    
    return mergeDocument(flowFolder, flow, remoteTemplateFolder, template_subfolder, templateName, id, subs, 
                        remoteOutputFolder, output_subfolder, email=email, payload=payload)    


def push_raw(request, method="POST"):
    if method=="GET":
        params = request.GET
    else:
        params = request.POST
    abs_uri = request.build_absolute_uri()            
    protocol, uri = abs_uri.split("://")
    site = protocol+"://"+uri.split("/")[0]+"/"
    id = getParamDefault(params, "identifier", str(randint(0,10000)))
    flowFolder = getParamDefault(params, "flow_folder", "/"+gdrive_root+"/Flows")
    flow = getParamDefault(params, "flow", "md")
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/"+gdrive_root+"/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/"+gdrive_root+"/Output")
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
    overall_outcome["traceback"]=format_exc(8)

    return overall_outcome

def disallowed_response(reason):
    overall_outcome = {}
    overall_outcome["success"]=False
    overall_outcome["messages"]=[{"level":"error", "message": reason}]
    overall_outcome["steps"]=[]

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
    download = getParamDefault(params, "download", "false")
    subfolder = getParamDefault(params, "path", "output")
    filepath = get_local_dir(subfolder)
    #file_content=""
    #with open(filepath+filename) as file:
    #    for line in file:
    #        file_content+=(line+"\n")
    if filename.find(".pdf")>=0: 
        file = open(filepath+"/"+filename, 'rb')
        response = HttpResponse(file, content_type='application/pdf')
        if download =="true":
            response['Content-Disposition'] = "attachment; filename={}".format(filename)
        else:
            response['Content-Disposition'] = "inline; filename={}".format(filename)
        return response
    elif filename.find(".zip")>=0:
        file = open(filepath+"/"+filename, 'rb')
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = "attachment; filename={}".format(filename)
        return response
    elif filename.find(".docx")>=0:
        file = open(filepath+"/"+filename, 'rb')
        response = HttpResponse(file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = "attachment; filename={}".format(filename)
        return response
    else:
        cwd = get_working_dir()
        return HttpResponse(get_local_txt_content(cwd, subfolder, filename))

def file(request):
    return file_raw(request)


def file_link(request):
    params = request.GET
    filename = getParamDefault(params, "name", None)
    subfolder = getParamDefault(params, "path", "output")
    response = {"remote":remote_link(filename, subfolder)}
    return JsonResponse(response)



def refresh(request):
    if remote_library:
        try:
            params = request.GET
            local = getParamDefault(params, "local", "templates")
            if local.find("templates")==0:
                remote_default = local.replace(local.split("/")[0],"/"+gdrive_root+"/Templates")
            elif local.find("flows")==0:
                remote_default = local.replace(local.split("/")[0],"/"+gdrive_root+"/Flows")
            elif local.find("branding")==0:
                remote_default = local.replace(local.split("/")[0],"/"+gdrive_root+"/Branding")
            elif local.find("test_data")==0:
                remote_default = local.replace(local.split("/")[0],"/"+gdrive_root+"/Test Data")
            elif local.find("transforms")==0:
                remote_default = local.replace(local.split("/")[0],"/"+gdrive_root+"/Transforms")
            else:
                remote_default = None    
            print("GDrive:", gdrive_root)
            print("refresh:", local, remote_default)
            remote = getParamDefault(params, "remote", remote_default)
            files = refresh_files(remote, local)
            response = {"refreshed_files":files}
        except Exception as ex:
            response = error_response(ex)
    else:
        response = disallowed_response("No connection to remote library")
    return JsonResponse(response)

def zip(request):
    try:
        params = request.GET
        abs_uri = request.build_absolute_uri()            
        protocol, uri = abs_uri.split("://")
        site = protocol+"://"+uri.split("/")[0]+"/"
        folders = getParamDefault(params, "folders", "templates,flows,transforms,test_data,branding")
        zip_file_name = getParamDefault(params, "name", "backup")
        target_dir = os.path.join(get_working_dir(),local_root)
        zip_file_name = zip_local_dirs(target_dir, zip_file_name, selected_subdirs = folders.split(","))
        link = site+"file/?name="+zip_file_name.split(os.path.sep)[-1]+"&path=."
        response = {"zip_files":zip_file_name, "link":link}
    except Exception as ex:
        response = error_response(ex)
    return JsonResponse(response)

def download_zip(request):
    try:
        params = request.GET
        abs_uri = request.build_absolute_uri()            
        protocol, uri = abs_uri.split("://")
        site = protocol+"://"+uri.split("/")[0]+"/"
        folders = getParamDefault(params, "folders", "templates,flows,transforms,test_data,branding")
        zip_file_name = getParamDefault(params, "name", "backup")
        target_dir = os.path.join(get_working_dir(),local_root)
        zip_file_full = zip_local_dirs(target_dir, zip_file_name, selected_subdirs = folders.split(","))
        zip_file_name = os.path.split(zip_file_full)[1]
        link = site+"file/?name="+zip_file_full.split(os.path.sep)[-1]+"&path=."
        response = {"zip_files":zip_file_full, "link":link}
    except Exception as ex:
        response = error_response(ex)
    file = open(zip_file_full, 'rb')
    response = HttpResponse(file, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename={}".format(zip_file_name)
    return response
#    return JsonResponse(response)

@csrf_exempt
def upload_zip(request):
    form = UploadZipForm(request.POST, request.FILES)
    target = os.path.join(get_working_dir(),local_root,request.FILES['file']._name)
    handle_uploaded_zip(request.FILES['file'], target)
    return JsonResponse({"file":target})

def handle_uploaded_zip(f, target):
    with open(target, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    zfile = zipfile.ZipFile(target)
    zfile.extractall(os.path.join(get_working_dir()))
