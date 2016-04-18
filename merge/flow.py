# Author: Andrew Elliott
# Copyright Revolutionary Systems 2016
# Distributed under the terms of GNU GPL v3
#
# Doc Merge flow management
#
import os
import json
from .merge_utils import (substituteVariablesDocx, substituteVariablesPlain,
    convert_markdown, folder_file, folder, email_file, uploadAsGoogleDoc, uploadFile, 
    exportFile, getFile, file_content_as, local_textfile_content, push_local_txt)

# retrieve flow definition from library
def get_flow_resource(flow_folder, flow_file_name):
    flow_doc_id = folder_file(flow_folder, flow_file_name)["id"]
    doc_content = file_content_as(flow_doc_id)
    str_content = '{"flow":'+doc_content.decode("utf-8")+'}'
    return json.loads(str_content)["flow"]

# retrieve flow definition locally
def get_flow_local(cwd, flow_local_folder, flow_file_name):
    try:
        with open(cwd+"/merge/"+flow_local_folder+"/"+flow_file_name, "r") as flow_file:
            str_content = '{"flow":'+flow_file.read()+'}'
        return json.loads(str_content)["flow"]
    except FileNotFoundError:
        return None

def get_flow(cwd, flow_local_folder, flow_folder, flow_file_name):
    # potential pre-processing here
    flow = get_flow_local(cwd, flow_local_folder, flow_file_name)
    if flow == None:
        flow = get_flow_resource(flow_folder, flow_file_name)
    return flow



# perform a download from Google drive, either as an export or getting content directly
def process_download(step, doc_id, doc_mimetype, localTemplateFileName, localMergedFileName):
    if step["folder"]=="templates":
         localFileName = localTemplateFileName
    else:
         localFileName = localMergedFileName
    if doc_mimetype == 'application/vnd.google-apps.document':         
        return exportFile(doc_id, localFileName+step["local_ext"], step["mimetype"])
    else:
        return getFile(doc_id, localFileName+step["local_ext"], step["mimetype"])

# perform a merge operation, either using more complex docx logic, or as plain text
def process_merge(step, localTemplateFileName, localMergedFileName, localMergedFileNameOnly, subs):
    if step["local_ext"]==".docx":
        outcome = substituteVariablesDocx(localTemplateFileName+step["local_ext"], localMergedFileName+step["local_ext"], subs)
    else:
        outcome = substituteVariablesPlain(localTemplateFileName+step["local_ext"], localMergedFileName+step["local_ext"], subs)
        outcome["link"] = subs["site"]+"file/?name="+localMergedFileNameOnly+step["local_ext"]

    return outcome

# convert markdown format to html
def process_markdown(step, localMergedFileName):
    outcome = convert_markdown(localMergedFileName+step["local_ext"], localMergedFileName+".html")  
    return outcome

# upload to Google drive, optionally converting to Google Drive format
def process_upload(step, localFileName, output_id):
    localFileName = localFileName
    if step["convert"]=="gdoc":
        return uploadAsGoogleDoc(localFileName+step["local_ext"], output_id, step["mimetype"])
    else:
        return uploadFile(localFileName+step["local_ext"], output_id, step["mimetype"])

# send email
def process_email(step, localFileName, you, credentials):
    return email_file(localFileName, step["from"], you, step["subject"], credentials) 

# push file to server
def process_push(cwd, step, localFileName, template_local_folder, subs, payload=""):
    file_name = push_local_txt(cwd, step["folder"], localFileName+step["local_ext"], payload)  
    return {"file":file_name, "link":subs["site"]+"file/?name="+file_name.split("/")[-1]+"&path="+template_local_folder}
    #return {"file":file_name}

# Process all steps in the flow: grab the template document, construct local path names and then invoke steps in turn
def process_flow(cwd, flow, template_remote_folder, template_subfolder, template_name, uniq, subs, output_folder, output_subfolder, you, email_credentials, payload=None, require_template=True):
    output_id = folder(output_folder)["id"]
    template_id = folder(template_remote_folder)["id"]
    template_local_folder = cwd+"/merge/templates/"
    if template_subfolder:
        template_local_folder+=template_subfolder+"/"
        if not os.path.exists(template_local_folder):
            os.makedirs(template_local_folder)
    localTemplateFileName = template_local_folder+template_name.split(".")[0]
    localMergedFileNameOnly = template_name.split(".")[0]+'_'+uniq
    output_folder = "output"
    if output_subfolder:
        output_folder+=output_subfolder+"/"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    localMergedFileName = cwd+"/merge/"+output_folder+"/"+localMergedFileNameOnly.replace("/",";")
    outcomes = []
    overall_outcome = {}
    for step in flow:
        try:
            local_folder = step["folder"]
        except:
            local_folder = output_folder
        if local_folder=="templates":
            localFileName = localTemplateFileName
            upload_id = template_id
        else:
            localFileName = localMergedFileName
            upload_id = output_id
        if step["step"]=="download":
            if require_template:
                doc = folder_file(template_remote_folder, template_name)
                doc_id = doc["id"]
                doc_mimetype = doc["mimeType"]
            outcome = process_download(step, doc_id, doc_mimetype, localTemplateFileName, localMergedFileName)
        if step["step"]=="merge":
            outcome = process_merge(step, localTemplateFileName, localMergedFileName, localMergedFileNameOnly, subs)
        if step["step"]=="markdown":
            outcome = process_markdown(step, localMergedFileName)
        if step["step"]=="upload":
            outcome = process_upload(step, localFileName, upload_id)
            doc_id = outcome["id"]
        if step["step"]=="email":
            outcome = process_email(step, localMergedFileName, you, email_credentials)
        if step["step"]=="push":
            outcome = process_push(cwd, step, localTemplateFileName, "templates/"+template_subfolder+"/", subs, payload=payload)
        outcomes.append({"step":step["name"], "outcome":outcome})
        for key in outcome.keys():
            if key in ["link","id", "mimeType"]:
                overall_outcome[key]=outcome[key]
    overall_outcome["success"]=True
    overall_outcome["messages"]=[]
    overall_outcome["steps"]=outcomes

    return overall_outcome

