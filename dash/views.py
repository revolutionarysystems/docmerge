from django.shortcuts import render
from .forms import MergeForm
from .models import MergeJob

# Create your views here.


def dash(request):
    return render(request, 'dash/dash_home.html', {})

def test(request):
    mergeJob=MergeJob(
    	template_folder="/Doc Merge/Templates",
    	template="AddParty_v3.md",
    	output_folder="/Doc Merge/Output",
    	flow = "md",
    	)
    mergeForm = MergeForm(instance=mergeJob)
    return render(request, 'dash/dash_test.html', {"mergeForm": mergeForm})
