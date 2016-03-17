import json
from django.shortcuts import render
from .forms import MergeForm
from .models import MergeJob
from merge.merge_utils import folder_files
from merge.views import merge_raw

# Create your views here.


def dash(request):
    widgets = []
    widgets.append({"title":"Merge Requests"})
    widgets.append({"title":"Service Status"})
    files = {"files":folder_files("/Doc Merge/Templates",fields="files(id, name, mimeType, trashed)")}
    quickTestJob=MergeJob(
        template_folder="/Doc Merge/Templates",
        template="Library.md",
        ident = "123",
        output_folder="/Doc Merge/Output",
        data_folder="/Doc Merge/Test Data",
        payload = json.dumps(files),
        payload_type = "json",
        branding_folder="/Doc Merge/Branding",
        flow = "md",
        )
    mergeForm = MergeForm(instance=quickTestJob)
    return render(request, 'dash/home.html', {"widgets":widgets, "mergeForm": mergeForm})

def test(request):
    mergeJob=MergeJob(
    	template_folder="/Doc Merge/Templates",
    	#template="AddParty_v3.md",
    	output_folder="/Doc Merge/Output",
    	data_folder="/Doc Merge/Test Data",
    	branding_folder="/Doc Merge/Branding",
    	flow = "md",
    	)

    mergeForm = MergeForm(instance=mergeJob)
    mergeForm.fields['template'].choices=[(file["name"],file["name"]) for file in folder_files("/Doc Merge/Templates")]
    return render(request, 'dash/test.html', {"mergeForm": mergeForm})


def test_result(request):
    mergeForm =  MergeForm(request.GET)
    mergeJob=MergeJob(
        template_folder="/Doc Merge/Templates",
        template=mergeForm["template"].value(),
        output_folder="/Doc Merge/Output",
        data_folder="/Doc Merge/Test Data",
        data_file=mergeForm["data_file"].value(),
        branding_folder="/Doc Merge/Branding",
        branding_file=mergeForm["branding_file"].value(),
        flow = mergeForm["flow"].value(),

        )
    mergeForm = MergeForm(instance=mergeJob)
    json_response = merge_raw(request)
    return render(request, 'dash/test.html', {"mergeForm": mergeForm, 'merge_response': json_response})


def library(request):
    widgets = []
    files = folder_files("/Doc Merge/Templates",fields="files(id, name, mimeType)")
    widgets.append({"title":"Templates", "files":files})
    files = folder_files("/Doc Merge/Test Data",fields="files(id, name, mimeType)")
    widgets.append({"title":"Test Cases", "files":files})
    files = folder_files("/Doc Merge/Branding",fields="files(id, name, mimeType)")
    widgets.append({"title":"Branding", "files":files})
    files = folder_files("/Doc Merge/Flows",fields="files(id, name, mimeType)")
    widgets.append({"title":"Flows", "files":files})
    return render(request, 'dash/library.html', {"widgets":widgets})

def archive(request):
    widgets = []
    widgets.append({"title":"Merge Requests"})
    files = folder_files("/Doc Merge/Output",fields="files(id, name, mimeType, modifiedTime)")
    widgets.append({"title":"Documents", "files":files})
    return render(request, 'dash/archive.html', {"widgets":widgets})

def account(request):
    widgets = []
    widgets.append({"title":"Configuration"})
    widgets.append({"title":"Users"})
    widgets.append({"title":"Statistics"})
    widgets.append({"title":"Credit"})
    return render(request, 'dash/account.html', {"widgets":widgets})

def links(request):
    return render(request, 'dash/links.html', {})
