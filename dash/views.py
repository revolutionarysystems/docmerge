import json
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django import forms
from .forms import MergeForm, SimpleMergeForm, RefreshForm, UploadZipForm, TestNavForm
from .models import MergeJob, RefreshJob
from merge.resource_utils import combined_folder_files as folder_files, local_folder_files, count_local_files, process_local_files, gd_populate_folders
from merge.views import merge_raw_wrapped,getParamDefault 
from merge.config import install_display, remote_library
from merge.config import install_display, remote_library, library_page
from merge.gd_service import GDriveAccessException, initialise as library_initialise, get_credentials_ask, get_credentials_store, ensure_initialised
from merge.gd_resource_utils import gd_build_folders
from docmerge.settings import MULTI_TENANTED
from merge.models import ClientConfig
from merge.flow import json_serial
from django.core.urlresolvers import reverse

def get_user_config(user):
    config = ClientConfig()
    if MULTI_TENANTED:
        tenant = user.profile.company
    else:
        tenant = "."
    config.tenant = tenant
    ensure_initialised(config)    
    return config

def get_library_uri(request):
    abs_uri= request.build_absolute_uri()
    protocol, uri = abs_uri.split("://")
    site = protocol+"://"+uri.split("/")[0]
    uri =  site+reverse('library')
    if uri.find("?")>=0:
        uri = uri[:uri.find("?")]
    return uri


@login_required 
def dash(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    widgets = []
    warning = None
    authuri = None
    config = get_user_config(request.user)
    nrequests_1d = count_local_files(config, "requests", days_ago=0, days_recent=1)
    nrequests_7d = count_local_files(config, "requests", days_ago=0, days_recent=7)
    nrequests_30d = count_local_files(config, "requests", days_ago=0, days_recent=30)
    recent_requests = local_folder_files(config, "requests", days_recent=1)
    recent_requests = sorted(recent_requests, key=lambda k: k['mtime'])
    mergeForm=None
    redirect = get_library_uri(request)
    if recent_requests:
        latest_request = recent_requests[-1] 
    else:
        latest_request = None
    widgets.append({"title":"Merge Requests", 
        "data": {"nrequests_1d": nrequests_1d, "nrequests_7d": nrequests_7d, "nrequests_30d": nrequests_30d},
        "glyph":"glyphicon glyphicon-hand-up",
        "latest_request":latest_request})
    status = "BLACK" # No info
    reason = "No recent requests"
    if recent_requests:
        status = "GREEN"
        reason = "No recent failures"
        for ep_request in recent_requests[-10:]:
            if ep_request["name"].find(".fail.")>=0:
                status = "RED"
                reason = "All of the most recent requests have failed"
            else:
                if status != "GREEN":
                    status = "AMBER"
                    reason = "Some recent requests have failed"


    widgets.append({"title":"Service Status", "glyph":"glyphicon glyphicon-info-sign", "status":status, "reason":reason})
    files = {"files":local_folder_files(config, "templates/Demo Examples",fields="files(id, name, mimeType, trashed)")}
    template_subfolder = "/Demo Examples"
    quickTestJob=MergeJob(
        template_folder="templates",
        template_subfolder="Demo Examples",
        template="Library.md",
        output_folder="output",
        data_folder="test_data",
        data_root="",
        payload = json.dumps(files, default = json_serial),
#        payload = [{"test":"this"}],
        payload_type = "json",
        branding_folder="branding",
        flow = "md.json",
        )
    mergeForm = MergeForm(instance=quickTestJob)
    mergeForm.fields['template_subfolder'].choices=[(template_subfolder, template_subfolder)]
    mergeForm.fields['flow'].choices=[("md.json","md.json")]
    mergeForm.fields['data_root'].initial=""
    mergeForm.fields['template'].choices=[("Library.md","Library.md")]

    try:
        dummy = folder_files(config, "flows")
    except GDriveAccessException:
        warning = "Not yet connected to a library"
        authuri = get_credentials_ask(redirect)


    return render(request, 'dash/home.html', {"widgets":widgets, "mergeForm": mergeForm, "install_display": install_display, "warning":warning, "authuri":authuri})


def clean_subfolder(subfolder):
    if len(subfolder)>0 and subfolder[-1] =="/":
        subfolder=subfolder[:-1]
    elif subfolder != "" and subfolder.find("/")!=0:
        subfolder = "/"+subfolder
    return subfolder

def make_test_forms(config, mergeJob, template_subfolder):
        mergeForm = SimpleMergeForm(instance=mergeJob)
        advMergeForm = MergeForm(instance=mergeJob)
        navForm = TestNavForm(instance=mergeJob)
        files = folder_files(config, "test_data")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        mergeForm.fields['data_file'].choices=[("","---")]+[(file["name"],file["name"]) for file in files]
        files = folder_files(config, "transforms")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        mergeForm.fields['xform_file'].choices=[("","---")]+[(file["name"],file["name"]) for file in files]
        items = folder_files(config, "templates"+template_subfolder)
        files = []
        folders = []
        if template_subfolder:
            parent = template_subfolder[:template_subfolder.rfind("/")+1]
            folders.append({"name":parent, "ext":".."})
            folders.append({"name":template_subfolder, "ext":"."})
        else:
            folders.append({"name":"/", "ext":"."})
        for item in items:
            if item["isdir"]:
                item["name"]=template_subfolder+"/"+item["name"]
                folders.append(item)
            else:
                files.append(item)
        folders = sorted(folders, key=lambda k: k['ext']+k['name']) 
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        mergeForm.fields['template_subfolder'].choices=[(template_subfolder, template_subfolder)]
        navForm.fields['template_subfolder'].label = "Template folder"
        navForm.fields['template_subfolder'].choices=[(folder["name"],folder["name"]) for folder in folders]
        mergeForm.fields['template_subfolder'].widget = forms.HiddenInput()
        mergeForm.fields['data_root'].widget = forms.HiddenInput()
        mergeForm.fields['template'].choices=[("","---")]+[(file["name"],file["name"]) for file in files]
        files = folder_files(config, "flows")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        mergeForm.fields['flow'].choices=[("","---")]+[(file["name"],file["name"]) for file in files]
        return navForm, mergeForm, advMergeForm

@login_required 
def test(request):
    config = get_user_config(request.user)
    warning = None
    navForm = None
    mergeForm = None
    advMergeForm = None
    try:
        params = request.GET
        template_subfolder = clean_subfolder(getParamDefault(params, "template_subfolder", ""))
        mergeJob=MergeJob(
            template_folder="templates/",
            template_subfolder = template_subfolder,
            #template="AddParty_v3.md",
            output_folder="output",
            data_folder="test_data",
            branding_folder="branding",
            xform_folder="transforms",
            flow = "md.txt",
            data_root = "docroot"
            )
        navForm, mergeForm, advMergeForm = make_test_forms(config, mergeJob, template_subfolder)
    except GDriveAccessException:
        warning = "Not yet connected to a library"
    return render(request, 'dash/test.html', {"sub_title": template_subfolder, "navForm": navForm, "mergeForm": mergeForm, "advMergeForm": advMergeForm, "install_display": install_display, "warning":warning, "hideforms":"N"})

def test_result(mergeForm, request, method="POST"):
    config = get_user_config(request.user)
    warning = None
    navForm = None
    advMergeForm = None
    json_response = merge_raw_wrapped(request, method=method)
    try:
        params = request.GET
        hideforms = getParamDefault(params, "hide_forms", "N")
        template_subfolder = clean_subfolder(getParamDefault(params, "template_subfolder", ""))
        mergeJob=MergeJob(
            template_folder="templates/",
            template_subfolder = mergeForm["template_subfolder"].value(),
            template=mergeForm["template"].value(),
            output_folder="output",
            data_folder="test_data",
            data_file=mergeForm["data_file"].value(),
            branding_folder="branding",
            branding_file=mergeForm["branding_file"].value(),
            xform_folder="transforms",
            xform_file=mergeForm["xform_file"].value(),
            flow = mergeForm["flow"].value(),
            identifier = mergeForm["identifier"].value(),
            data_root = mergeForm["data_root"].value(),
        )
        navForm, mergeForm, advMergeForm = make_test_forms(config, mergeJob, template_subfolder)

    #    mergeForm = SimpleMergeForm(instance=mergeJob)
    #    advMergeForm = MergeForm(instance=mergeJob)
    #    navForm = TestNavForm(instance=mergeJob)
    #    files = folder_files(config, "test_data")
    #    files = sorted(files, key=lambda k: k['ext']+k['name']) 
    #    mergeForm.fields['data_file'].choices=[(file["name"],file["name"]) for file in files]
    #    files = folder_files(config, "templates"+template_subfolder)
    #    files = sorted(files, key=lambda k: k['ext']+k['name']) 
    #    mergeForm.fields['template'].choices=[(file["name"],file["name"]) for file in files]
    #    mergeForm.fields['template_subfolder'].choices=[(template_subfolder, template_subfolder)]
    #    mergeForm.fields['template_subfolder'].widget = forms.HiddenInput()
    #    navForm.fields['template_subfolder'].choices=[(folder["name"],folder["name"]) for folder in folders]
    #    files = folder_files(config, "flows")
    #    files = sorted(files, key=lambda k: k['ext']+k['name']) 
    #    mergeForm.fields['flow'].choices=[(file["name"],file["name"]) for file in files]
        json_response = merge_raw_wrapped(request, method=method)
    except GDriveAccessException:
        warning = "Not yet connected to a library"
    return render(request, 'dash/test.html', {"sub_title": template_subfolder, "navForm":navForm, "mergeForm": mergeForm, "advMergeForm": advMergeForm, 'merge_response': json_response, "install_display": install_display, "hideforms":hideforms})

@login_required 
def test_result_get(request):
    mergeForm =  MergeForm(request.GET)
    return test_result(mergeForm, request, method="GET")

@login_required 
def test_result_post(request):
    mergeForm =  MergeForm(request.POST)
    return test_result(mergeForm, request, method="POST")

def refresh_form(local):
    if remote_library:
        refreshJob=RefreshJob(local=local)
        refreshForm = RefreshForm(instance=refreshJob)
        return refreshForm
    else:
        return None





@login_required 
def library_folder(request):
    config = get_user_config(request.user)
    params = request.GET
    lib_root = getParamDefault(params, "root", "")
    lib_folders = getParamDefault(params, "folders", "templates").split(",")
    widgets = []
    warning = None
    if remote_library:
        remote = "Connected to Google Drive"
    else:
        remote = "Not connected to Google Drive"
    try:
        for folder in lib_folders:
            folder_name =(lib_root+"/"+folder).replace("Templates", "templates")
            subfolder = folder_name[folder_name.find("/")+1:]
            files = folder_files(config, folder_name, fields="files(id, name, mimeType)")
            if lib_root.find("/")>=0:
                parent_root = lib_root[:lib_root.rfind("/")]
                parent_folder = lib_root[lib_root.rfind("/")+1:]
            else:
                parent_root = lib_root
                parent_folder = ""
            files.append({"isdir":True,"name":"..", "parent":{"root":parent_root, "folder":parent_folder}})
            files = sorted(files, key=lambda k: ('..' if k['isdir'] else k['ext'])+k['name']) 
            widgets.append({"path":os.path.join("templates", subfolder), "subfolder": subfolder, "title": folder_name, "files":files, "glyph":"glyphicon glyphicon-file", "refreshForm": refresh_form(folder_name.replace("Templates", "templates"))})
    except GDriveAccessException:
        warning = "Not yet connected to a library"
        remote = "Not connected to Google Drive"
    return render(request, library_page, {"widgets":widgets, "install_display": install_display, "warning":warning, "remote":remote})


@login_required 
def library(request):
    config = get_user_config(request.user)
    widgets = []
    warning = None
    authuri = None
    params=request.GET
    redirect = get_library_uri(request)
    if remote_library:
        remote = "Connected to Google Drive"
    else:
        remote = "Not connected to Google Drive"
    if "code" in params: #Auth code
        get_credentials_store(config, params["code"], redirect)
        library_initialise(config)
        gd_build_folders(config)
        gd_populate_folders(config)
    try:
        files = folder_files(config, "templates",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: ('..' if k['isdir'] else k['ext'])+k['name']) 
        widgets.append({"title":"Templates", "path":"templates", "files":files, "glyph":"glyphicon glyphicon-file", "refreshForm": refresh_form("templates")})
        files = folder_files(config, "flows",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        widgets.append({"title":"Flows",  "path":"flows", "files":files, "glyph":"glyphicon glyphicon-tasks", "refreshForm": refresh_form("flows")})
        files = folder_files(config, "transforms",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        widgets.append({"title":"Transforms",  "path":"transforms", "files":files, "glyph":"glyphicon glyphicon-transfer", "refreshForm": refresh_form("transforms")})
        files = folder_files(config, "test_data",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        widgets.append({"title":"Test Data",  "path":"test_data", "files":files, "glyph":"glyphicon glyphicon-tags", "refreshForm": refresh_form("test_data")})
        files = folder_files(config, "branding",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        widgets.append({"title":"Branding",  "path":"branding", "files":files, "glyph":"glyphicon glyphicon-certificate", "refreshForm": refresh_form("branding")})
    except GDriveAccessException:
        warning = "Not yet connected to a library"
        authuri = get_credentials_ask(redirect)
        remote = "Not connected to Google Drive"

    return render(request, library_page, {"widgets":widgets, "install_display": install_display, "redirect": redirect, "warning":warning, "authuri":authuri, "remote":remote})

@login_required 
def library_link(request):
    config = get_user_config(request.user)
    library_initialise(config)
    return render(request, 'dash/library_link.html', {"install_display": install_display})

@login_required 
def archive(request):
    config = get_user_config(request.user)
    widgets = []
    files = local_folder_files(config, "requests",fields="files(id, name, mimeType, modifiedTime)")
    files = sorted(files, key=lambda k: k['mtime'], reverse=True) 
    widgets.append({"title":"Merge Requests", "files":files[:10], "path":"requests", "glyph":"glyphicon glyphicon-hand-up"})
    files = local_folder_files(config, "output",fields="files(id, name, mimeType, modifiedTime)")
    files = sorted(files, key=lambda k: k['mtime'], reverse=True) 
    widgets.append({"title":"Documents", "files":files[:500], "glyph":"glyphicon glyphicon-file"})
    return render(request, 'dash/archive.html', {"widgets":widgets, "install_display": install_display})

@login_required 
def account(request):
    config = get_user_config(request.user)
    widgets = []
    widgets.append({"title":"Configuration", "glyph":"glyphicon glyphicon-cog"})
    widgets.append({"title":"Users", "glyph":"glyphicon glyphicon-user"})
    widgets.append({"title":"Reports", "glyph":"glyphicon glyphicon-list-alt"})
    widgets.append({"title":"Credit", "glyph":"glyphicon glyphicon-star"})
    widgets.append({"title":"Backup", "glyph":"glyphicon glyphicon-sort"})
    zipform = UploadZipForm()
    return render(request, 'dash/account.html', {"widgets":widgets, "install_display": install_display, "zipform":zipform})

def guide(request):
    return render(request, 'dash/guide.html', {"install_display": install_display})

def api_guide(request):
    return render(request, 'dash/api_guide.html', {"install_display": install_display})

def flow_guide(request):
    return render(request, 'dash/flow_guide.html', {"install_display": install_display})

def template_guide(request):
    return render(request, 'dash/template_guide.html', {"install_display": install_display})

def links(request):
    return render(request, 'dash/links.html', {"install_display": install_display})

def logout_view(request):
    logout(request)
    return render(request, 'registration/loggedout.html', {"install_display": install_display})