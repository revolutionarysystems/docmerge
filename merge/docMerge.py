import os
#import django
#from django.conf import settings
from random import randint

from .merge_utils import initialiseService, downloadFile, substituteVariablesDocx, substituteVariablesPlain, convertToPdf,uploadFile,convert_markdown,folder_file,folder,email_file,uploadAsGoogleDoc,getPdf
from .resource_utils import  get_working_dir
from .flow import get_flow,process_flow

#credentials = {"username":"DOCMERGE\\andrew", "password":"mnemonic10", "server":"ssrs.reachmail.net:25"}
email_credentials = {"username":"andrewcaelliott@gmail.com", "password":"napier", "server":"smtp.gmail.com:587"}

#cwd = os.getcwd()
#if (cwd.find("home")>=0):  #fudge for windows/linux difference
#    cwd = cwd+"/docmerge"

cwd = get_working_dir()
cwd = cwd.replace("\\", "/")
def mergeDocument(flow_folder, flow, template_folder, template_subfolder, template_name, 
	                uniq, subs, output_folder, output_subfolder, email="andrew.elliott+epub@revolutionarysystems.co.uk", payload="", require_template=True):
    response = process_flow(cwd, get_flow(cwd, "flows", flow_folder, flow), template_folder, template_subfolder,
    			template_name, uniq, subs, output_folder, output_subfolder, email, email_credentials, payload=payload, require_template=require_template)
    return response



