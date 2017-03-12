import re
import os
import zipfile
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .docMerge import mergeDocument
from .xml4doc import getData
from random import randint
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
#from .merge_utils import get_local_dir
from .resource_utils import get_working_dir, get_local_txt_content,get_local_dir, refresh_files, zip_local_dirs, remote_link, process_local_files
from traceback import format_exc
from dash.forms import UploadZipForm
from .config import remote_library, gdrive_root, local_root
from tokenapi.decorators import token_required
from .gd_service import ensure_initialised
from .gd_resource_utils import gd_path_equivalent
from docmerge.settings import MULTI_TENANTED
from merge.models import ClientConfig


def get_user_config(user):
    print("user:")
    print(user)
    config = ClientConfig()
    if MULTI_TENANTED:
        tenant = user.profile.company
    else:
        tenant = "."
    config.tenant = tenant
    ensure_initialised(config)    
    return config

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
    config = get_user_config(request.user)
    if method=="GET":
        params = request.GET
    else:
        params = request.POST
    abs_uri = request.build_absolute_uri()            
    protocol, uri = abs_uri.split("://")
    site = protocol+"://"+uri.split("/")[0]+"/"
    id = getParamDefault(params, "identifier", str(randint(0,1000000)))
    if MULTI_TENANTED:
        tenant_extension = "/"+config.tenant
    else:
        tenant_extension = ""

    flowFolder = getParamDefault(params, "flow_folder", "/"+gdrive_root+tenant_extension+"/Flows")
    flow = getParamDefault(params, "flow", "md")
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/"+gdrive_root+tenant_extension+"/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/"+gdrive_root+tenant_extension+"/Output")
    template_subfolder = getParamDefault(params, "template_subfolder", None)
    output_subfolder = getParamDefault(params, "output_subfolder", None)
    payload = getParamDefault(params, "payload", None, preserve_plus=True)
    payload_type = getParamDefault(params, "payload_type", None)
    test_case = getParamDefault(params, "test_case", None)
    data_folder = getParamDefault(params, "data_folder", "/"+gdrive_root+tenant_extension+"/Test Data")
    data_file = getParamDefault(params, "data_file", None)
    data_root = getParamDefault(params, "data_root", "docroot")
    branding_folder = getParamDefault(params, "branding_folder", "/"+gdrive_root+tenant_extension+"/Branding")
    branding_file = getParamDefault(params, "branding_file", None)
    if branding_file == "None":
        branding_file = None
    xform_folder = getParamDefault(params, "xform_folder", "/"+gdrive_root+tenant_extension+"/Transforms")
    xform_file = getParamDefault(params, "xform_file", None)
    if xform_file == "None":
        xform_file = None
    templateName = getParamDefault(params, "template", "AddParty.md")
    email = getParamDefault(params, "email", "andrew.elliott+epub@revolutionarysystems.co.uk")
    templateName = templateName.replace("\\", "/")
    if template_subfolder:
        template_subfolder = template_subfolder.replace("\\", "/")
    subs = getData(config, test_case=test_case, payload=payload, payload_type=payload_type, params = params, local_data_folder="test_data", remote_data_folder = data_folder, data_file=data_file, xform_folder = xform_folder, xform_file=xform_file)
    if data_root:
        if data_root in subs:
            subs = subs[data_root]
#        else:
#            raise ValueError("Invalid data_root: " + data_root)
    if branding_file:
        branding_subs = getData(config, local_data_folder = "branding", remote_data_folder = branding_folder, data_file=branding_file)
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
    return mergeDocument(config, flowFolder, flow, remoteTemplateFolder, template_subfolder, templateName, id, subs, 
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


def read_bulk_data(bulk_list, condition, test, testemail, config):
    lines = get_local_txt_content(get_working_dir(), config, "test_data", bulk_list).split("\n")
    selected = []
    headers = lines[0].split(",")
    print(headers)
    for line in lines[1:]:
        params ={}
        try:
            ziplist=list(zip(headers,line.split(",")))
            for item in ziplist:
                params[item[0].replace("\n","")]=item[1].replace("\n","")
        except Exception as e:
            print(e)
            print(line)
        if eval(condition):
            if test=="True":
                params["email"]=testemail.replace(" ","+").format(params["Name"].replace(" ",""))
            case = { "docroot": params }
            selected +=[ case ]
    return selected


def bulk_merge_raw(request, method="POST"):
    config = get_user_config(request.user)
    print("Config:", config)
    if method=="GET":
        params = request.GET
    else:
        params = request.POST
    abs_uri = request.build_absolute_uri()            
    protocol, uri = abs_uri.split("://")
    site = protocol+"://"+uri.split("/")[0]+"/"
    # todo better way of id. Dot plus serial?
    id = getParamDefault(params, "identifier", str(randint(0,10000)))
    if MULTI_TENANTED:
        tenant_extension = "/"+config.tenant
    else:
        tenant_extension = ""

    flowFolder = getParamDefault(params, "flow_folder", "/"+gdrive_root+tenant_extension+"/Flows")
    flow = getParamDefault(params, "flow", "md")
    remoteTemplateFolder = getParamDefault(params, "template_folder", "/"+gdrive_root+tenant_extension+"/Templates")
    remoteOutputFolder = getParamDefault(params, "output_folder", "/"+gdrive_root+tenant_extension+"/Output")
    template_subfolder = getParamDefault(params, "template_subfolder", None)
    output_subfolder = getParamDefault(params, "output_subfolder", None)

    data_folder = getParamDefault(params, "data_folder", "/"+gdrive_root+tenant_extension+"/Test Data")
    data_file = getParamDefault(params, "data_file", None)
    data_root = getParamDefault(params, "data_root", "docroot")

    branding_folder = getParamDefault(params, "branding_folder", "/"+gdrive_root+tenant_extension+"/Branding")
    branding_file = getParamDefault(params, "branding_file", None)
    if branding_file == "None":
        branding_file = None

    xform_folder = getParamDefault(params, "xform_folder", "/"+gdrive_root+tenant_extension+"/Transforms")
    xform_file = getParamDefault(params, "xform_file", None)
    if xform_file == "None":
        xform_file = None
    templateName = getParamDefault(params, "template", "AddParty.md")
    #Hmmm
    email = getParamDefault(params, "email", "andrew.elliott+epub@revolutionarysystems.co.uk")
    templateName = templateName.replace("\\", "/")
    if template_subfolder:
        template_subfolder = template_subfolder.replace("\\", "/")

    if branding_file:
        branding_subs = getData(config, local_data_folder = "branding", remote_data_folder = branding_folder, data_file=branding_file)

    condition = getParamDefault(params, "condition", "True")
    test = getParamDefault(params, "test", "True")
    testemail = getParamDefault(params, "testemail", "dummy@dummy.con")


    bulk_data = read_bulk_data(data_file, condition, test, testemail, config)
    results = []
    for subs in bulk_data:
    # This within a bulk loop
        if data_root:
            if data_root in subs:
                subs = subs[data_root]
        if branding_file:
            subs["branding"]= branding_subs
        subs["NowDate"]=datetime.now()
        subs["docs"]=[templateName]

        subs["site"]= site


        results+= [mergeDocument(config, flowFolder, flow, remoteTemplateFolder, template_subfolder, templateName, id, subs, 
                        remoteOutputFolder, output_subfolder, email=subs["email"], payload="")]
    return {"bulk_result":results}    



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

def bulk_merge_raw_wrapped(request, method="POST"):
    try:
        return bulk_merge_raw(request, method=method)
    except Exception as ex:
        return error_response(ex)

@csrf_exempt
#@token_required
def merge(request):
    return JsonResponse(merge_raw_wrapped(request))
    
@csrf_exempt
#@token_required
def bulk_merge(request):
    return JsonResponse(bulk_merge_raw_wrapped(request))
    
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
    config = get_user_config(request.user)
    params = request.GET
    filename = getParamDefault(params, "name", None)
    download = getParamDefault(params, "download", "false")
    subfolder = getParamDefault(params, "path", "output")
    filepath = get_local_dir(subfolder, config)
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
        return HttpResponse(get_local_txt_content(cwd, config, subfolder, filename))

def file(request):
    return file_raw(request)


def file_link(request):
    config = get_user_config(request.user)
    params = request.GET
    filename = getParamDefault(params, "name", None)
    subfolder = getParamDefault(params, "path", "output")
    response = {"remote":remote_link(config, filename, subfolder)}
    return JsonResponse(response)



def refresh(request):
    config = get_user_config(request.user)
    if remote_library:
        try:
            params = request.GET
            recursive = getParamDefault(params, "all", "false")
            local = getParamDefault(params, "local", "templates")
            remote_default = gd_path_equivalent(config, local)
            remote = getParamDefault(params, "remote", remote_default)
            files = refresh_files(config, remote, local, recursive=(recursive=="true"))
            response = {"refreshed_files":files}
        except Exception as ex:
            response = error_response(ex)
    else:
        response = disallowed_response("No connection to remote library")
    return JsonResponse(response)

def zip_files(request):
    config = get_user_config(request.user)
    try:
        params = request.GET
        abs_uri = request.build_absolute_uri()            
        protocol, uri = abs_uri.split("://")
        site = protocol+"://"+uri.split("/")[0]+"/"
        folders = getParamDefault(params, "folders", "templates,flows,transforms,test_data,branding")
        zip_file_name = getParamDefault(params, "name", "backup")
        if MULTI_TENANTED:
            zip_file_name = config.tenant+"_"+zip_file_name
#        target_dir = os.path.join(get_working_dir(),local_root)
        target_dir = get_local_dir(".", config)
        zip_file_name = zip_local_dirs(target_dir, zip_file_name, selected_subdirs = folders.split(","))
        link = site+"file/?name="+zip_file_name.split(os.path.sep)[-1]+"&path=."
        response = {"zip_files":zip_file_name, "link":link}
    except Exception as ex:
        response = error_response(ex)
    return JsonResponse(response)

def download_zip(request):
    config = get_user_config(request.user)
    try:
        params = request.GET
        abs_uri = request.build_absolute_uri()            
        protocol, uri = abs_uri.split("://")
        site = protocol+"://"+uri.split("/")[0]+"/"
        folders = getParamDefault(params, "folders", "templates,flows,transforms,test_data,branding")
        zip_file_name = getParamDefault(params, "name", "backup")
        if MULTI_TENANTED:
            zip_file_name = config.tenant+"_"+zip_file_name
        target_dir = get_local_dir(".", config)
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
def upload_zip(request) :
    config = get_user_config(request.user)
    form = UploadZipForm(request.POST, request.FILES)
    target_dir = get_local_dir(".", config)
    target_parent = get_local_dir("..", config)
    target = os.path.join(target_dir,request.FILES['file']._name)
    success, message = handle_uploaded_zip(request.FILES['file'], target, target_parent, config.tenant+"/")
    return JsonResponse({"file":target, "success":success, "message": message})

def handle_uploaded_zip(f, target, target_parent, account):
    with open(target, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    zfile = zipfile.ZipFile(target)
    if account =="." or account=="./":
        zfile.extractall(target_parent)
        return True, "uploaded"
    else:
        try:
            zfile.extractall(target_parent,[account])
            return True, "uploaded to "+account
        except:
            return False, "no content for "+account

def to_days(timeparam):
    p = re.compile("^(?P<magnitude>[0-9]+)(?P<unit>[dDhHmM])$")
    m=p.match(timeparam)
    try:
        magnitude = m.group('magnitude')
        unit = m.group('unit')
        magnum = int(magnitude)
        if unit.lower()=="d":
            return magnum
        elif unit.lower()=="h":
            return magnum / 24.0
        elif unit.lower()=="m":
            return magnum / 1440.0
    except:
        raise ValueError("Invalid time period: " + timeparam)


def cull_outputs(request):
    config = get_user_config(request.user)
    params = request.GET
    retain_dump = getParamDefault(params, "retain_dump", "1D")
    retain_output = getParamDefault(params, "retain_output", "1D")
    retain_requests = getParamDefault(params, "retain_requests", "62D")
    retain_dump_days = to_days(retain_dump)
    retain_output_days = to_days(retain_output)
    retain_requests_days = to_days(retain_requests)
    files = process_local_files(config, "dump", days_ago=retain_dump_days, days_recent=1000, action="delete")
    files += process_local_files(config, "output", days_ago=retain_output_days, days_recent=1000, action="delete")
    files += process_local_files(config, "requests", days_ago=retain_requests_days, days_recent=1000, action="delete")
    return JsonResponse({"files_culled":len(files)})

