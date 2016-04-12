import os
#import django
#from django.conf import settings
from random import randint

from .merge_utils import initialiseService, downloadFile, substituteVariablesDocx, substituteVariablesPlain, convertToPdf,uploadFile,convert_markdown,folder_file,folder,email_file,uploadAsGoogleDoc,getPdf, get_working_dir
from .flow import get_flow,process_flow

#credentials = {"username":"DOCMERGE\\andrew", "password":"mnemonic10", "server":"ssrs.reachmail.net:25"}
email_credentials = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}

#cwd = os.getcwd()
#if (cwd.find("home")>=0):  #fudge for windows/linux difference
#    cwd = cwd+"/docmerge"

cwd = get_working_dir()

def mergeDocument(flow_folder, flow, template_folder, template_name, uniq, subs, output_folder, email="andrew.elliott+epub@revolutionarysystems.co.uk"):
    response = process_flow(cwd, get_flow(flow_folder, flow), template_folder, template_name, uniq, subs, output_folder, email, email_credentials)
    return response



