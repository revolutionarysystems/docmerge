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
    exportFile, getFile, file_content_as, local_textfile_content)

# retrieve flow definition from library
def get_flow_resource(flow_folder, flow_file_name):
    flow_doc_id = folder_file(flow_folder, flow_file_name)["id"]
    doc_content = file_content_as(flow_doc_id)
    str_content = '{"flow":'+doc_content.decode("utf-8")+'}'
    return json.loads(str_content)["flow"]

def get_flow(flow_folder, flowcode):
    # potential pre-processing here
    return get_flow_resource(flow_folder, flowcode)

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
def process_merge(step, doc_id, localTemplateFileName, localMergedFileName, localMergedFileNameOnly, subs):
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

# Process all steps in the flow: grab the template document, construct local path names and then invoke steps in turn
def process_flow(cwd, flow, template_folder, template_name, uniq, subs, output_folder, you, email_credentials):
    #print(flow)
    doc = folder_file(template_folder, template_name)
    doc_id = doc["id"]
    doc_mimetype = doc["mimeType"]
    output_id = folder(output_folder)["id"]
    localTemplateFileName = cwd+"/merge/templates/"+template_name.split(".")[0]
    localMergedFileNameOnly = template_name.split(".")[0]+'_'+uniq
    localMergedFileName = cwd+"/merge/output/"+localMergedFileNameOnly
    outcomes = []
    for step in flow:
        if step["step"]=="download":
            outcome = process_download(step, doc_id, doc_mimetype, localTemplateFileName, localMergedFileName)
        if step["step"]=="merge":
            outcome = process_merge(step, doc_id, localTemplateFileName, localMergedFileName, localMergedFileNameOnly, subs)
        if step["step"]=="markdown":
            outcome = process_markdown(step, localMergedFileName)
        if step["step"]=="upload":
            outcome = process_upload(step, localMergedFileName, output_id)
            doc_id = outcome["id"]
        if step["step"]=="email":
            outcome = process_email(step, localMergedFileName, you, email_credentials)
        outcomes.append({"step":step["name"], "outcome":outcome})
    return outcomes

