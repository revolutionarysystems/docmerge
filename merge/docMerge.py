import os
#import django
#from django.conf import settings
from random import randint

from .merge_utils import initialiseService, downloadFile, substituteVariablesDocx, substituteVariablesPlain, convertToPdf,uploadFile,convert_markdown,folder_file,folder,email_file,uploadAsGoogleDoc,getPdf
from .flow import get_flow,process_flow

#credentials = {"username":"DOCMERGE\\andrew", "password":"mnemonic10", "server":"ssrs.reachmail.net:25"}
email_credentials = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}

cwd = os.getcwd()
if (cwd.find("home")>=0):  #fudge for windows/linux difference
    cwd = cwd+"/docmerge"

def mergeDocument(flow_folder, flow, template_folder, template_name, uniq, subs, output_folder, email="andrew.elliott+epub@revolutionarysystems.co.uk"):
    outcomes = process_flow(get_flow(flow_folder, flow), template_folder, template_name, uniq, subs, output_folder, email, email_credentials)
    return {"outcomes":outcomes}



