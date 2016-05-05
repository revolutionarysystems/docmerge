import json
from django.shortcuts import render
from .forms import MergeForm, SimpleMergeForm, RefreshForm
from .models import MergeJob, RefreshJob
from merge.gd_resource_utils import folder_files
from merge.views import merge_raw_wrapped,getParamDefault 
from merge.config import install_display_name

# Create your views here.


def dash(request):
    widgets = []
    widgets.append({"title":"Merge Requests", "glyph":"glyphicon glyphicon-hand-up"})
    widgets.append({"title":"Service Status", "glyph":"glyphicon glyphicon-info-sign"})
    #Todo protect against SSLError AND BrokenPipeError
    files = {"files":folder_files("/Doc Merge/Templates",fields="files(id, name, mimeType, trashed)")}
    quickTestJob=MergeJob(
        template_folder="/Doc Merge/Templates",
        template="Library.md",
        output_folder="/Doc Merge/Output",
        data_folder="/Doc Merge/Test Data",
        payload = json.dumps(files),
        payload_type = "json",
        branding_folder="/Doc Merge/Branding",
        flow = "md.txt",
        )
    mergeForm = MergeForm(instance=quickTestJob)
    return render(request, 'dash/home.html', {"widgets":widgets, "mergeForm": mergeForm, "install_display_name": install_display_name})

def test(request):
    params = request.GET
    template_subfolder = getParamDefault(params, "template_subfolder", "")
    if template_subfolder != "":
        template_subfolder = "/"+template_subfolder
    mergeJob=MergeJob(
    	template_folder="/Doc Merge/Templates/",
        template_subfolder = template_subfolder,
    	#template="AddParty_v3.md",
    	output_folder="/Doc Merge/Output",
    	data_folder="/Doc Merge/Test Data",
        branding_folder="/Doc Merge/Branding",
        xform_folder="/Doc Merge/Transforms",
    	flow = "md.txt",
        data_root = "docroot"
    	)

    mergeForm = SimpleMergeForm(instance=mergeJob)
    advMergeForm = MergeForm(instance=mergeJob)
    files = folder_files("/Doc Merge/Test Data")
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    mergeForm.fields['data_file'].choices=[(file["name"],file["name"]) for file in files]
    files = folder_files("/Doc Merge/Templates"+template_subfolder)
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    mergeForm.fields['template'].choices=[(file["name"],file["name"]) for file in files]
    files = folder_files("/Doc Merge/Flows")
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    mergeForm.fields['flow'].choices=[(file["name"],file["name"]) for file in files]
    return render(request, 'dash/test.html', {"mergeForm": mergeForm, "advMergeForm": advMergeForm, "install_display_name": install_display_name})

def test_result(mergeForm, request, method="POST"):
    mergeForm =  MergeForm(request.GET)
    params = request.GET
    print(params)
    template_subfolder = getParamDefault(params, "template_subfolder", "")
    mergeJob=MergeJob(
        template_folder="/Doc Merge/Templates/",
        template_subfolder = mergeForm["template_subfolder"].value(),
        template=mergeForm["template"].value(),
        output_folder="/Doc Merge/Output",
        data_folder="/Doc Merge/Test Data",
        data_file=mergeForm["data_file"].value(),
        branding_folder="/Doc Merge/Branding",
        branding_file=mergeForm["branding_file"].value(),
        xform_folder="/Doc Merge/Transforms",
        xform_file=mergeForm["xform_file"].value(),
        flow = mergeForm["flow"].value(),
        identifier = mergeForm["identifier"].value(),
        data_root = mergeForm["data_root"].value(),
    )
    mergeForm = SimpleMergeForm(instance=mergeJob)
    advMergeForm = MergeForm(instance=mergeJob)
    files = folder_files("/Doc Merge/Test Data")
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    mergeForm.fields['data_file'].choices=[(file["name"],file["name"]) for file in files]
    files = folder_files("/Doc Merge/Templates"+template_subfolder)
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    mergeForm.fields['template'].choices=[(file["name"],file["name"]) for file in files]
    files = folder_files("/Doc Merge/Flows")
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    mergeForm.fields['flow'].choices=[(file["name"],file["name"]) for file in files]
    json_response = merge_raw_wrapped(request, method=method)
    return render(request, 'dash/test.html', {"mergeForm": mergeForm, "advMergeForm": advMergeForm, 'merge_response': json_response, "install_display_name": install_display_name})

def test_result_get(request):
    mergeForm =  MergeForm(request.GET)
    return test_result(mergeForm, request, method="GET")

def test_result_post(request):
    mergeForm =  MergeForm(request.POST)
    return test_result(mergeForm, request, method="POST")

def refresh_form(local):
    refreshJob=RefreshJob(local=local)
    refreshForm = RefreshForm(instance=refreshJob)
    return refreshForm

def library_folder(request):
    params = request.GET
    lib_root = getParamDefault(params, "root", "")
    lib_folders = getParamDefault(params, "folders", "Templates").split(",")
    widgets = []
    for folder in lib_folders:
        folder_name =lib_root+"/"+folder
        subfolder = folder_name[folder_name.find("/")+1:]
        files = folder_files("/Doc Merge/"+folder_name, fields="files(id, name, mimeType)")
        if lib_root.find("/")>=0:
            parent_root = lib_root[:lib_root.rfind("/")]
            parent_folder = lib_root[lib_root.rfind("/")+1:]
        else:
            parent_root = lib_root
            parent_folder = ""
        files.append({"mimeType":'application/vnd.google-apps.folder',"name":"..", "parent":{"root":parent_root, "folder":parent_folder}})
        files = sorted(files, key=lambda k: ('aa' if k['mimeType']=='application/vnd.google-apps.folder' else k['mimeType'])+k['name']) 
        widgets.append({"subfolder": subfolder, "title": folder_name, "files":files, "glyph":"glyphicon glyphicon-file", "refreshForm": refresh_form(folder_name.replace("Templates", "templates"))})
    return render(request, 'dash/library.html', {"widgets":widgets, "install_display_name": install_display_name})

def library(request):
    widgets = []
    files = folder_files("/Doc Merge/Templates",fields="files(id, name, mimeType)")
    files = sorted(files, key=lambda k: ('aa' if k['mimeType']=='application/vnd.google-apps.folder' else k['mimeType'])+k['name']) 
    widgets.append({"title":"Templates", "files":files, "glyph":"glyphicon glyphicon-file", "refreshForm": refresh_form("templates")})
    files = folder_files("/Doc Merge/Test Data",fields="files(id, name, mimeType)")
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    widgets.append({"title":"Test Data", "files":files, "glyph":"glyphicon glyphicon-tags", "refreshForm": refresh_form("test_data")})
    files = folder_files("/Doc Merge/Branding",fields="files(id, name, mimeType)")
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    widgets.append({"title":"Branding", "files":files, "glyph":"glyphicon glyphicon-certificate", "refreshForm": refresh_form("branding")})
    files = folder_files("/Doc Merge/Flows",fields="files(id, name, mimeType)")
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    widgets.append({"title":"Flows", "files":files, "glyph":"glyphicon glyphicon-tasks", "refreshForm": refresh_form("flows")})
    files = folder_files("/Doc Merge/Transforms",fields="files(id, name, mimeType)")
    files = sorted(files, key=lambda k: k['mimeType']+k['name']) 
    widgets.append({"title":"Transforms", "files":files, "glyph":"glyphicon glyphicon-transfer", "refreshForm": refresh_form("transforms")})
    return render(request, 'dash/library.html', {"widgets":widgets, "install_display_name": install_display_name})

def archive(request):
    widgets = []
    widgets.append({"title":"Merge Requests", "glyph":"glyphicon glyphicon-hand-up"})
    files = folder_files("/Doc Merge/Output",fields="files(id, name, mimeType, modifiedTime)")
    widgets.append({"title":"Documents", "files":files, "glyph":"glyphicon glyphicon-file"})
    return render(request, 'dash/archive.html', {"widgets":widgets, "install_display_name": install_display_name})

def account(request):
    widgets = []
    widgets.append({"title":"Configuration", "glyph":"glyphicon glyphicon-cog"})
    widgets.append({"title":"Users", "glyph":"glyphicon glyphicon-user"})
    widgets.append({"title":"Reports", "glyph":"glyphicon glyphicon-list-alt"})
    widgets.append({"title":"Credit", "glyph":"glyphicon glyphicon-star"})
    return render(request, 'dash/account.html', {"widgets":widgets, "install_display_name": install_display_name})

def links(request):
    return render(request, 'dash/links.html', {})
