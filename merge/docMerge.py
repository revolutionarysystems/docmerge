import os
#import django
#from django.conf import settings
from random import randint

from .gd_resource_utils import downloadFile,uploadFile, folder_file,folder
from .resource_utils import  get_working_dir
from .flow import get_flow,process_flow
from .config import email_credentials
from .config import email_default_recipient


#credentials = {"username":"DOCMERGE\\andrew", "password":"mnemonic10", "server":"ssrs.reachmail.net:25"}

#cwd = os.getcwd()
#if (cwd.find("home")>=0):  #fudge for windows/linux difference
#    cwd = cwd+"/docmerge"

cwd = get_working_dir()
cwd = cwd.replace("\\", "/")
def mergeDocument(flow_folder, flow, template_folder, template_subfolder, template_name, 
	                uniq, subs, output_folder, output_subfolder, email=email_default_recipient, payload="", require_template=True):
    response = process_flow(cwd, get_flow(cwd, "flows", flow_folder, flow), template_folder, template_subfolder,
    			template_name, uniq, subs, output_folder, output_subfolder, email, email_credentials, payload=payload, require_template=require_template)
    return response



