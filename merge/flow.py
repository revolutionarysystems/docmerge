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
    exportFile, getFile, file_content_as, local_textfile_content, push_local_txt, combine_docx, 
    substituteVariablesPlainString, merge_docx_footer)

from datetime import datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

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

# retrieve flow definition locally
def get_template_list_local(template_list_local_folder, template_list_file_name, subs=None):
    try:
#        print(template_list_local_folder+template_list_file_name)
        with open(template_list_local_folder+template_list_file_name, "r") as template_list_file:
            str_content = '{"template_list":'+template_list_file.read()+'}'
            if subs:
                str_content = substituteVariablesPlainString(str_content, subs)
        return json.loads(str_content)["template_list"]
    except FileNotFoundError:
        return None



# perform a download from Google drive, either as an export or getting content directly
def process_download(step, doc_id, doc_mimetype, localTemplateFileName, localMergedFileName, localMergedFileNameOnly, output_subfolder, subs):
#    print("downloading")
#    print(doc_id)
#    print(doc_mimetype)
    if step["folder"]=="templates":
         localFileName = localTemplateFileName
    else:
         localFileName = localMergedFileName
    if doc_mimetype == 'application/vnd.google-apps.document':         
        outcome = exportFile(doc_id, localFileName+step["local_ext"], step["mimetype"])
        outcome["link"] = subs["site"]+"file/?name="+localMergedFileNameOnly+step["local_ext"]
    else:
        outcome = getFile(doc_id, localFileName+step["local_ext"], step["mimetype"])
        outcome["link"] = subs["site"]+"file/?name="+localMergedFileNameOnly+step["local_ext"]

    return outcome

# Compound merge operation
def process_compound_merge(cwd, uniq, step, template_subfolder, template_list, output_subfolder, subs):
    template_local_folder = cwd+"/merge/templates/"
    if template_subfolder:
        template_local_folder+=template_subfolder+"/"
    else:
        template_subfolder = "/"+template_list[:template_list.rfind("/")+1]
        template_local_folder+=template_subfolder
        template_list =template_list[template_list.rfind("/")+1:]
    localTemplateListFileName = template_local_folder+template_list
    local_output_folder = "output"
    localCombinedFileNameOnly = (template_subfolder[1:]+"/"+template_list.split(".")[0]).replace("//", "/")
    localCombinedFileNameOnly = localCombinedFileNameOnly.replace(" ","_").replace("/","-")
    localCombinedFileName = cwd+"/merge/"+local_output_folder+"/"+localCombinedFileNameOnly+"_"+uniq+step["local_ext"]
    template_list = get_template_list_local(template_local_folder, template_list, subs=subs)
    files = template_list[0]["compound"]
    output_files = []
    for file_name in files:
        if file_name[0]=="-":
            output_files.append("pagebreak")
        else:
            localTemplateFileName, localMergedFileName, localMergedFileNameOnly = localNames(cwd, uniq, template_subfolder, file_name, output_subfolder)
            if step["local_ext"]==".docx":
                outcome = substituteVariablesDocx(localTemplateFileName+step["local_ext"], localMergedFileName+step["local_ext"], subs)
                output_files.append(outcome["file"])
    outcome = combine_docx(output_files, localCombinedFileName)
    outcome["link"] = subs["site"]+"/file/?name="+localCombinedFileNameOnly+"_"+uniq+step["local_ext"]

    try:
        if step["footer"]=="true":
            merge_docx_footer(localCombinedFileName, subs)
    except KeyError:
        pass

    return outcome

# perform a merge operation, either using more complex docx logic, or as plain text
def process_merge(cwd, uniq, step, localTemplateFileName, template_subfolder, localMergedFileName, localMergedFileNameOnly, output_subfolder, subs):
    try: #Allow "step to override template"
        localTemplateFileName, localMergedFileName, localMergedFileNameOnly = localNames(cwd, uniq, template_subfolder, step["template"], output_subfolder)
    except KeyError: #No rederivation of names if no step["template"]
        pass        
    if step["local_ext"]==".docx":
        outcome = substituteVariablesDocx(localTemplateFileName+step["local_ext"], localMergedFileName+step["local_ext"], subs)
        outcome["link"] = subs["site"]+"file/?name="+localMergedFileNameOnly+step["local_ext"]
    else:
        outcome = substituteVariablesPlain(localTemplateFileName+step["local_ext"], localMergedFileName+step["local_ext"], subs)
        outcome["link"] = subs["site"]+"file/?name="+localMergedFileNameOnly+step["local_ext"]
    try:
        if step["footer"]=="true":
            merge_docx_footer(localMergedFileName+step["local_ext"], subs)
    except KeyError:
        pass

    return outcome



# convert markdown format to html
def process_markdown(step, localMergedFileName):
    outcome = convert_markdown(localMergedFileName+step["local_ext"], localMergedFileName+".html")  
    return outcome

# upload to Google drive, optionally converting to Google Drive format
def process_upload(step, localFileName, subfolder, upload_id):
    if subfolder:
        upload_folder = folder(subfolder, upload_id, create_if_absent=True)
        upload_id=upload_folder["id"]

    if step["convert"]=="gdoc":
        print("converting")
        return uploadAsGoogleDoc(localFileName+step["local_ext"], upload_id, step["mimetype"])
    else:
        print("not converting")
        return uploadFile(localFileName+step["local_ext"], upload_id, step["mimetype"])

# send email
def process_email(step, localFileName, you, credentials):
    return email_file(localFileName, step["from"], you, step["subject"], credentials) 

# push file to server
def process_push(cwd, step, localFileName, template_local_folder, subs, payload=""):
    file_name = push_local_txt(cwd, step["folder"], localFileName+step["local_ext"], payload)  
    return {"file":file_name, "link":subs["site"]+"file/?name="+file_name.split("/")[-1]+"&path="+template_local_folder}
    #return {"file":file_name}

# push file to local
def process_payload_dump(cwd, step, localFileName, subs, payload=""):
    if step["type"]=="json":
        payload = json.dumps(subs, default = json_serial, indent=4, sort_keys=True)
    file_name = push_local_txt(cwd, step["folder"], localFileName.replace("output", step["folder"])+step["local_ext"], payload)  
    return {"file":file_name, "link":subs["site"]+"file/?name="+file_name.split("/")[-1]+"&path="+step["folder"]}
    #return {"file":file_name}

def localNames(cwd, uniq, template_subfolder, template_name, output_subfolder):
    template_local_folder = cwd+"/merge/templates/"
    if template_subfolder:
        template_local_folder+=template_subfolder+"/"
        if not os.path.exists(template_local_folder):
            os.makedirs(template_local_folder)
    localTemplateFileName = (template_local_folder+template_name.split(".")[0]).replace("//", "/")
    localMergedFileNameOnly = (template_name.split(".")[0]+'_'+uniq)
    if template_subfolder:
        localMergedFileNameOnly = template_subfolder[1:]+"/"+localMergedFileNameOnly
    localMergedFileNameOnly = localMergedFileNameOnly.replace("//","/").replace(" ","_").replace("/","-")
    local_output_folder = "output"
    if output_subfolder:
        local_output_folder+=output_subfolder+"/"
        if not os.path.exists(local_output_folder):
            os.makedirs(local_output_folder)
    localMergedFileName = (cwd+"/merge/"+local_output_folder+"/"+localMergedFileNameOnly).replace("//", "/") #for now, avoid creating output folders
    return localTemplateFileName, localMergedFileName, localMergedFileNameOnly


# Process all steps in the flow: grab the template document, construct local path names and then invoke steps in turn
def process_flow(cwd, flow, template_remote_folder, template_subfolder, template_name, uniq, subs, output_folder, output_subfolder, you, email_credentials, payload=None, require_template=True):
    localTemplateFileName, localMergedFileName, localMergedFileNameOnly = localNames(cwd, uniq, template_subfolder, template_name, output_subfolder)
    outcomes = []
    overall_outcome = {}
    doc_id = None
    for step in flow:
        try:
            try:
                local_folder = step["folder"]
            except:
                local_folder = output_folder

            if step["step"]=="download":
                if doc_id ==None and require_template:
                    doc = folder_file(template_remote_folder, template_name)
                    doc_id = doc["id"]
                    doc_mimetype = doc["mimeType"]
                outcome = process_download(step, doc_id, doc_mimetype, localTemplateFileName, localMergedFileName, localMergedFileNameOnly, output_subfolder, subs)

            if step["step"]=="merge":
                outcome = process_merge(cwd, uniq, step, localTemplateFileName, template_subfolder, localMergedFileName, localMergedFileNameOnly, output_subfolder, subs)

            if step["step"]=="compound_merge": #template_name is a list of template names in a json file
                outcome = process_compound_merge(cwd, uniq, step, template_subfolder, template_name, output_subfolder, subs)

            if step["step"]=="markdown":
                outcome = process_markdown(step, localMergedFileName)

            if step["step"]=="upload":
                if local_folder=="templates":
                    localFileName = localTemplateFileName
                    upload_id = folder(template_remote_folder)["id"]
                    upload_subfolder = template_subfolder
                else:
                    localFileName = localMergedFileName
                    upload_id = folder(output_folder)["id"]
                    upload_subfolder = None
                outcome = process_upload(step, localFileName, upload_subfolder, upload_id)
                doc_id = outcome["id"]
                doc_mimetype = outcome["mimeType"]

            if step["step"]=="email":
                outcome = process_email(step, localMergedFileName, you, email_credentials)

            if step["step"]=="push":
                outcome = process_push(cwd, step, localTemplateFileName, "templates/"+template_subfolder+"/", subs, payload=payload)

            if step["step"]=="payload":
                outcome = process_payload_dump(cwd, step, localMergedFileName, subs, payload=payload)

            outcomes.append({"step":step["name"], "success": True, "outcome":outcome})
            for key in outcome.keys():
                if key in ["link", "id", "mimeType"]:
                    overall_outcome[key]=outcome[key]
                    overall_outcome[key+"_"+step["name"].replace(" ","_")]=outcome[key]
        except Exception as ex:
            outcomes.append({"step":step["name"], "success": False, "outcome": {"exception":str(ex)}})

    overall_outcome["success"]=True
    overall_outcome["messages"]=[]
    overall_outcome["steps"]=outcomes

    return overall_outcome

