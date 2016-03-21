import json
from django.shortcuts import render
from .forms import MergeForm, SimpleMergeForm, MinimalMergeForm
from .models import MergeJob
from merge.merge_utils import folder_files
from merge.views import merge_raw

# Create your views here.


def dash(request):
    widgets = []
    widgets.append({"title":"Merge Requests", "glyph":"glyphicon glyphicon-flash"})
    widgets.append({"title":"Service Status", "glyph":"glyphicon glyphicon-info-sign"})
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
    return render(request, 'dash/home.html', {"widgets":widgets, "mergeForm": mergeForm})

def test(request):
    mergeJob=MergeJob(
    	template_folder="/Doc Merge/Templates",
    	#template="AddParty_v3.md",
    	output_folder="/Doc Merge/Output",
    	data_folder="/Doc Merge/Test Data",
    	branding_folder="/Doc Merge/Branding",
    	flow = "md.txt",
        data_root = "ItpDocumentRequest"
    	)

    mergeForm = SimpleMergeForm(instance=mergeJob)
    advMergeForm = MergeForm(instance=mergeJob)
    mergeForm.fields['template'].choices=[(file["name"],file["name"]) for file in folder_files("/Doc Merge/Templates")]
    mergeForm.fields['flow'].choices=[(file["name"],file["name"]) for file in folder_files("/Doc Merge/Flows")]
    return render(request, 'dash/test.html', {"mergeForm": mergeForm, "advMergeForm": advMergeForm})


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
        identifier = mergeForm["identifier"].value(),
        data_root = mergeForm["data_root"].value(),
    )
    mergeForm = SimpleMergeForm(instance=mergeJob)
    advMergeForm = MergeForm(instance=mergeJob)
    json_response = merge_raw(request)
    return render(request, 'dash/test.html', {"mergeForm": mergeForm, "advMergeForm": advMergeForm, 'merge_response': json_response})


def library(request):
    widgets = []
    files = folder_files("/Doc Merge/Templates",fields="files(id, name, mimeType)")
    widgets.append({"title":"Templates", "files":files, "glyph":"glyphicon glyphicon-file"})
    files = folder_files("/Doc Merge/Test Data",fields="files(id, name, mimeType)")
    widgets.append({"title":"Test Cases", "files":files, "glyph":"glyphicon glyphicon-tags"})
    files = folder_files("/Doc Merge/Branding",fields="files(id, name, mimeType)")
    widgets.append({"title":"Branding", "files":files, "glyph":"glyphicon glyphicon-certificate"})
    files = folder_files("/Doc Merge/Flows",fields="files(id, name, mimeType)")
    widgets.append({"title":"Flows", "files":files, "glyph":"glyphicon glyphicon-tasks"})
    return render(request, 'dash/library.html', {"widgets":widgets})

def archive(request):
    widgets = []
    widgets.append({"title":"Merge Requests", "glyph":"glyphicon glyphicon-flash"})
    files = folder_files("/Doc Merge/Output",fields="files(id, name, mimeType, modifiedTime)")
    widgets.append({"title":"Documents", "files":files, "glyph":"glyphicon glyphicon-file"})
    return render(request, 'dash/archive.html', {"widgets":widgets})

def account(request):
    widgets = []
    widgets.append({"title":"Configuration", "glyph":"glyphicon glyphicon-cog"})
    widgets.append({"title":"Users", "glyph":"glyphicon glyphicon-user"})
    widgets.append({"title":"Reports", "glyph":"glyphicon glyphicon-list-alt"})
    widgets.append({"title":"Credit", "glyph":"glyphicon glyphicon-star"})
    return render(request, 'dash/account.html', {"widgets":widgets})

def links(request):
    return render(request, 'dash/links.html', {})
