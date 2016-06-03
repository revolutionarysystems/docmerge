import json
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import MergeForm, SimpleMergeForm, RefreshForm, UploadZipForm
from .models import MergeJob, RefreshJob
from merge.resource_utils import combined_folder_files as folder_files, local_folder_files
from merge.views import merge_raw_wrapped,getParamDefault 
from merge.config import install_display_name, remote_library
from merge.gd_service import GDriveAccessException, initialise as library_initialise, get_credentials_ask, get_credentials_store
from merge.gd_resource_utils import gd_build_folders


@login_required 
def dash(request):
    print(request.user)
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    widgets = []
    widgets.append({"title":"Merge Requests", "glyph":"glyphicon glyphicon-hand-up"})
    widgets.append({"title":"Service Status", "glyph":"glyphicon glyphicon-info-sign"})
    #Todo protect against SSLError AND BrokenPipeError
    #files = {"files":local_folder_files("templates",fields="files(id, name, mimeType, trashed)")}
    quickTestJob=MergeJob(
        template_folder="templates",
        template="Library.md",
        output_folder="output",
        data_folder="test_data",
#        payload = json.dumps(files),
        payload = [{"test":"this"}],
        payload_type = "json",
        branding_folder="branding",
        flow = "md.txt",
        )
    mergeForm = MergeForm(instance=quickTestJob)
    return render(request, 'dash/home.html', {"widgets":widgets, "mergeForm": mergeForm, "install_display_name": install_display_name})

@login_required 
def test(request):
    warning = None
    try:
        params = request.GET
        template_subfolder = getParamDefault(params, "template_subfolder", "")
        if template_subfolder != "":
            template_subfolder = "/"+template_subfolder
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

        mergeForm = SimpleMergeForm(instance=mergeJob)
        advMergeForm = MergeForm(instance=mergeJob)
        files = folder_files("test_data")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        mergeForm.fields['data_file'].choices=[(file["name"],file["name"]) for file in files]
        files = folder_files("templates"+template_subfolder)
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        mergeForm.fields['template'].choices=[(file["name"],file["name"]) for file in files]
        files = folder_files("flows")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        mergeForm.fields['flow'].choices=[(file["name"],file["name"]) for file in files]
    except GDriveAccessException:
        warning = "Not yet connected to a library"
    return render(request, 'dash/test.html', {"mergeForm": mergeForm, "advMergeForm": advMergeForm, "install_display_name": install_display_name, "warning":warning})

def test_result(mergeForm, request, method="POST"):
    mergeForm =  MergeForm(request.GET)
    params = request.GET
    print(params)
    template_subfolder = getParamDefault(params, "template_subfolder", "")
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
    mergeForm = SimpleMergeForm(instance=mergeJob)
    advMergeForm = MergeForm(instance=mergeJob)
    files = folder_files("test_data")
    files = sorted(files, key=lambda k: k['ext']+k['name']) 
    mergeForm.fields['data_file'].choices=[(file["name"],file["name"]) for file in files]
    files = folder_files("templates"+template_subfolder)
    files = sorted(files, key=lambda k: k['ext']+k['name']) 
    mergeForm.fields['template'].choices=[(file["name"],file["name"]) for file in files]
    files = folder_files("flows")
    files = sorted(files, key=lambda k: k['ext']+k['name']) 
    mergeForm.fields['flow'].choices=[(file["name"],file["name"]) for file in files]
    json_response = merge_raw_wrapped(request, method=method)
    return render(request, 'dash/test.html', {"mergeForm": mergeForm, "advMergeForm": advMergeForm, 'merge_response': json_response, "install_display_name": install_display_name})

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
    params = request.GET
    lib_root = getParamDefault(params, "root", "")
    lib_folders = getParamDefault(params, "folders", "templates").split(",")
    widgets = []
    warning = None
    try:
        for folder in lib_folders:
            folder_name =(lib_root+"/"+folder).replace("Templates", "templates")
            subfolder = folder_name[folder_name.find("/")+1:]
            files = folder_files(folder_name, fields="files(id, name, mimeType)")
            print(files)
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
    return render(request, 'dash/library.html', {"widgets":widgets, "install_display_name": install_display_name, "warning":warning})

@login_required 
def library(request):
    widgets = []
    warning = None
    authuri = None
    params=request.GET
    redirect = request.build_absolute_uri()
    if redirect.find("?")>=0:
        redirect = redirect[:redirect.find("?")]
    if "code" in params: #Auth code
        get_credentials_store(params["code"], redirect)
        library_initialise()
        gd_build_folders()
    try:
        files = folder_files("templates",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: ('..' if k['isdir'] else k['ext'])+k['name']) 
        widgets.append({"title":"Templates", "path":"templates", "files":files, "glyph":"glyphicon glyphicon-file", "refreshForm": refresh_form("templates")})
        files = folder_files("flows",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        widgets.append({"title":"Flows",  "path":"flows", "files":files, "glyph":"glyphicon glyphicon-tasks", "refreshForm": refresh_form("flows")})
        files = folder_files("transforms",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        widgets.append({"title":"Transforms",  "path":"transforms", "files":files, "glyph":"glyphicon glyphicon-transfer", "refreshForm": refresh_form("transforms")})
        files = folder_files("test_data",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        widgets.append({"title":"Test Data",  "path":"test_data", "files":files, "glyph":"glyphicon glyphicon-tags", "refreshForm": refresh_form("test_data")})
        files = folder_files("branding",fields="files(id, name, mimeType)")
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        widgets.append({"title":"Branding",  "path":"branding", "files":files, "glyph":"glyphicon glyphicon-certificate", "refreshForm": refresh_form("branding")})
    except GDriveAccessException:
        warning = "Not yet connected to a library"
        authuri = get_credentials_ask(redirect)

    return render(request, 'dash/library.html', {"widgets":widgets, "install_display_name": install_display_name, "warning":warning, "authuri":authuri})

@login_required 
def library_link(request):
    library_initialise()
    return render(request, 'dash/library_link.html', {"install_display_name": install_display_name})

@login_required 
def archive(request):
    widgets = []
    widgets.append({"title":"Merge Requests", "glyph":"glyphicon glyphicon-hand-up"})
    files = local_folder_files("output",fields="files(id, name, mimeType, modifiedTime)")
    files = sorted(files, key=lambda k: k['mtime'], reverse=True) 
    widgets.append({"title":"Documents", "files":files, "glyph":"glyphicon glyphicon-file"})
    return render(request, 'dash/archive.html', {"widgets":widgets, "install_display_name": install_display_name})

@login_required 
def account(request):
    widgets = []
    widgets.append({"title":"Configuration", "glyph":"glyphicon glyphicon-cog"})
    widgets.append({"title":"Users", "glyph":"glyphicon glyphicon-user"})
    widgets.append({"title":"Reports", "glyph":"glyphicon glyphicon-list-alt"})
    widgets.append({"title":"Credit", "glyph":"glyphicon glyphicon-star"})
    widgets.append({"title":"Backup", "glyph":"glyphicon glyphicon-sort"})
    zipform = UploadZipForm()
    return render(request, 'dash/account.html', {"widgets":widgets, "install_display_name": install_display_name, "zipform":zipform})

@login_required 
def links(request):
    return render(request, 'dash/links.html', {})

def logout_view(request):
    logout(request)
    return render(request, 'registration/loggedout.html')