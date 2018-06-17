import re
import os
import zipfile
import json
import datetime, time
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .docMerge import mergeDocument
#from .xml4doc import getData
from merge.xml4doc import getData, fields_from_subs
from random import randint
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
#from .merge_utils import get_local_dir
from .resource_utils import (
    get_working_dir, get_local_txt_content,get_local_dir, refresh_files, zip_local_dirs, remote_link, 
    process_local_files, get_folders_and_files, combined_folder_files as folder_files, clean_subfolder, del_local)
from traceback import format_exc
from dash.forms import UploadZipForm
from .config import remote_library, gdrive_root, local_root
from tokenapi.decorators import token_required
from .gd_service import ensure_initialised
from .gd_resource_utils import gd_path_equivalent
from docmerge.settings import MULTI_TENANTED
from merge.models import ClientConfig
from merge.merge_utils import substituteVariablesPlainString,convert_markdown_string,preprocess
from pynliner import Pynliner


def get_user_config(user):
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
    action = getParamDefault(params, "action", None)
    print(action)
    filepath = get_local_dir(subfolder, config)
    #file_content=""
    #with open(filepath+filename) as file:
    #    for line in file:
    #        file_content+=(line+"\n")
    if (action=="delete"):
        cwd = get_working_dir()
        print(cwd, subfolder, filename)
        try:
            del_local(cwd, config, subfolder, filename)
        except FileNotFoundError:
            return JsonResponse({"success":False, "filename":filename, "message":"file not found"})    
        return JsonResponse({"success":True, "filename":filename, "message":"file deleted"})
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
            clear = getParamDefault(params, "clear", "false")
            local = getParamDefault(params, "local", "templates")
            remote_default = gd_path_equivalent(config, local.replace("\\","/"))
            remote = getParamDefault(params, "remote", remote_default)
            if (clear=="true"):
                process_local_files(config, local, days_ago=0, days_recent=999, action="delete", recursive=(recursive=="true"))
            files = refresh_files(config, remote, local, recursive=(recursive=="true"),clear=(clear=="true"))
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

@csrf_exempt
def download_zip(request):
    config = get_user_config(request.user)
    try:
        params = request.GET
        abs_uri = request.build_absolute_uri()            
        protocol, uri = abs_uri.split("://")
        site = protocol+"://"+uri.split("/")[0]+"/"
        folders = getParamDefault(params, "folders", "templates,flows,transforms,test_data,branding")
        ts = datetime.now()
        ziptimestamp = ts.strftime("%Y%m%d%H%M%S")
        zip_file_name = getParamDefault(params, "name", "backup-"+ziptimestamp)
        if MULTI_TENANTED:
            zip_file_name = config.tenant+"_"+zip_file_name
        target_dir = get_local_dir(".", config)
        print(target_dir)
        zip_file_full = zip_local_dirs(target_dir, zip_file_name, selected_subdirs = folders.split(","))
        zip_file_name = os.path.split(zip_file_full)[1]
        link = site+"file/?name="+zip_file_full.split(os.path.sep)[-1]+"&path=."
        response = {"zip_files":zip_file_full, "link":link}
    except Exception as ex:
        print(ex)
        response = error_response(ex)
    file = open(zip_file_full, 'rb')
    response = HttpResponse(file, content_type='application/zip')
    response['Content-Disposition'] = "attachment; filename={}".format(zip_file_name)
    return response
#    return JsonResponse(response)

@csrf_exempt
def patch_zip(request):
    return upload_zip(request, suppress_clear=True)

@csrf_exempt
def upload_zip(request, suppress_clear=False) :
    config = get_user_config(request.user)
    params = request.POST
    preserve = getParamDefault(params, "preserve", "false")
    form = UploadZipForm(params, request.FILES)
    folders = getParamDefault(params, "folders", "templates,flows,transforms,test_data,branding")
    target_dir = get_local_dir(".", config)
    target_parent = get_local_dir("..", config)
#    target = os.path.join(target_dir,request.FILES['file']._name)
    print("uploading", preserve, suppress_clear)
    if (preserve=="false") and not (suppress_clear):
        print("clearing")
        cleared_files = process_local_files(config, '.', days_ago=0, days_recent=999, action="delete", recursive=True, folders=folders)
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

def clear_resources(request):
    config = get_user_config(request.user)
    params = request.GET
    recursive = getParamDefault(params, "all", "false")
    local = getParamDefault(params, "local", None)
    if local != None:
        files = process_local_files(config, local, days_ago=0, days_recent=999, action="delete", recursive=(recursive=="true"))
    return JsonResponse({"files_cleared":len(files)})


def compose_preview(request):
    config = get_user_config(request.user)
    params = request.GET
    template_content= getParamDefault(params, "template_content", "")
    template_test_case= getParamDefault(params, "template_test_case", "")
    test_case_xform= getParamDefault(params, "test_case_xform", None)
    stylesheet_content = getParamDefault(params, "template_stylesheet_content", "")
    try:
        subs = getData(config, data_file=template_test_case, local_data_folder="test_data", xform_file=test_case_xform)
    except:
        subs={}
    try:
        subs=subs["docroot"]
    except:
        pass

    template_content  = preprocess(template_content)
    rendered = substituteVariablesPlainString(config, template_content, subs)
    rendered = convert_markdown_string(rendered)
    rendered = '<div class="echo-publish">'+rendered+"</div>"
    rendered = Pynliner().from_string(rendered).with_cssString(stylesheet_content).run()
    return JsonResponse({"preview":rendered})

def clean_field(field):
    if field.find("_item")>=0:
            fld1=field[:field.rfind("_item")+5]
            fld1=fld1[fld1.rfind(".")+1:]
            fld2=field[field.rfind("_item")+5:]
            fld=fld1+fld2
    else:
            fld = field
    return fld.replace("docroot.","")

def sample_data(request):
    config = get_user_config(request.user)
    params = request.GET
    template_test_case= getParamDefault(params, "template_test_case", "")
    test_case_xform= getParamDefault(params, "test_case_xform", None)
    filter_param= getParamDefault(params, "filter", None)
    parent_param= getParamDefault(params, "parent", None)
    if filter_param=="docroot":
        filter_param = None
    if filter_param:
        filter_string1=filter_param+"."
    else:
        filter_string1 = None
    if filter_param:
        filter_string2=filter_param+"_item."
    else:
        filter_string2 = None
    if parent_param and not (parent_param =="docroot"):
        filter_string1=parent_param+"."+filter_string1
        filter_string3=parent_param+"_item."+filter_param+"."
        filter_string4=parent_param+"_item."+filter_param+"_item."
    else:
        filter_string3 = "#"
        filter_string4 = "#"
    try:
        subs = getData(config, data_file=template_test_case, local_data_folder="test_data", xform_file=test_case_xform)
    except:
        subs={}
    #try:
    #    subs=subs["docroot"]
    #except:
    #    pass

    fields, groups, tree = fields_from_subs(subs)
    field_string = "Fields"
    for field in sorted(fields.keys()):
        if ((not filter_param) or (clean_field(field)+".").find(filter_string1)>=0 or clean_field(field).find(filter_string2)>=0 
                                    or clean_field(field).find(filter_string3)>=0 or clean_field(field).find(filter_string4)>=0):
                field_string+="\n"
                field_string+='<pre onclick="clip(this);" class="field">'+"{{"+clean_field(field)+"}}"+"</pre>"
    logic_string = "Logic"
    for field in sorted(fields):
        if ((not filter_param) or (clean_field(field)+".").find(filter_string1)>=0 or clean_field(field).find(filter_string2)>=0 
                                    or clean_field(field).find(filter_string3)>=0 or clean_field(field).find(filter_string4)>=0):
                logic_string+="\n"
                logic_string+='<pre onclick="clip(this);" class="field">'+"{% if "+clean_field(field)+" == \""+str(fields[field])+"\" %}{% endif %}"+"</pre>"
    group_string = "Groups"
    for field in sorted(groups):
        if ((not filter_param) or (clean_field(field)+".").find(filter_string1)>=0 or clean_field(field).find(filter_string2)>=0
                                    or clean_field(field).find(filter_string3)>=0 or clean_field(field).find(filter_string4)>=0):
                group_string+="\n"
                itemname = field[1+field.rfind("."):]+"_item"
                group_string+='<pre onclick="clip(this);" class="field">'+"{% for "+itemname+" in "+field.replace("docroot.","")+" %}{% endfor %}"+"</pre>"
    template_sample = {
            "fields": field_string,
            "logic": logic_string, 
            "groups":group_string,
            "tree": tree,
            };
    return JsonResponse({"sample":template_sample})

def styling(request):
    cwd = get_working_dir()
    config = get_user_config(request.user)
    params = request.GET
    template_folder = "templates"
    template_subfolder= getParamDefault(params, "template_subfolder", "")
    template_stylesheet= getParamDefault(params, "template_stylesheet", "")
    stylesheet_content = get_local_txt_content(cwd, config, template_folder+template_subfolder, template_stylesheet)

    return JsonResponse({"styling":stylesheet_content})

def load_template(request):
    cwd = get_working_dir()
    config = get_user_config(request.user)
    params = request.GET
    template_folder = "templates"
    template_subfolder= getParamDefault(params, "template_subfolder", "")
    template= getParamDefault(params, "template_name", "")
    template_content = get_local_txt_content(cwd, config, template_folder+template_subfolder, template)
    template_content=template_content.replace("\n\n", "\n")

    return JsonResponse({"template":template_content})

def change_folder(request):
    cwd = get_working_dir()
    config = get_user_config(request.user)
    params = request.GET
    template_folder = "templates"
    template_subfolder = clean_subfolder(getParamDefault(params, "template_subfolder", ""))
    items = folder_files(config, "templates"+template_subfolder)
    folders, files = get_folders_and_files(template_subfolder, items)
    template_files = [(file["name"],file["name"]) for file in files if file["name"].find(".css")<0]
    style_files = [(file["name"],file["name"]) for file in files if file["name"].find(".css")>0]
    subfolders = [(folder["name"],folder["name"]) for folder in folders]

    return JsonResponse({"folders":subfolders, "styles":style_files, "templates":template_files})

def delete(request):
    cwd = get_working_dir()
    config = get_user_config(request.user)
    params = request.GET
    path = getParamDefault(params, "file_path", "")
    file_name= getParamDefault(params, "file_name", "")
    del_local(cwd, config, path,file_name)
    return JsonResponse({"file_deleted":file_name})
    
