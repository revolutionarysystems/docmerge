from django.shortcuts import render
from .forms import MergeForm
from .models import MergeJob
from merge.merge_utils import folder_files

# Create your views here.


def dash(request):
    return render(request, 'dash/dash_home.html', {})

def test(request):
    mergeJob=MergeJob(
    	template_folder="/Doc Merge/Templates",
    	#template="AddParty_v3.md",
    	output_folder="/Doc Merge/Output",
    	data_folder="/Doc Merge/Test Data",
    	flow = "md",
    	)

    mergeForm = MergeForm(instance=mergeJob)
    mergeForm.fields['template'].choices=[(file["name"],file["name"]) for file in folder_files("/Doc Merge/Templates")]
    return render(request, 'dash/dash_test.html', {"mergeForm": mergeForm})
