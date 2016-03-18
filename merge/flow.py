import os
import json
from .merge_utils import initialiseService, downloadFile, substituteVariablesDocx, substituteVariablesPlain, convertToPdf,uploadFile,convert_markdown,folder_file,folder,email_file,uploadAsGoogleDoc,exportFile,getFile,file_content_as

cwd = os.getcwd()
if (cwd.find("home")>=0):  #fudge for windows/linux difference
    cwd = cwd+"/docmerge"
if (cwd.find("scripts")>=0):  
    cwd = cwd.replace("\scripts","")


docx_flow = [
		{
			"name": "Download to docx",
			"step": "download",
			"folder": "templates",
			"mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
			"local_ext":".docx"
		},
		{
			"name": "Merge docx",
			"step": "merge",
			"mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
			"local_ext":".docx"
		},
		{
			"name": "Upload to gdoc",
			"step": "upload",
			"convert":"gdoc",
			"folder": "output",
			"mimetype": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
			"local_ext":".docx"
		},
		{
			"name": "Generate pdf",
			"step": "download",
			"folder": "output",
			"mimetype": "application/pdf",
			"local_ext":".pdf"
		},
		{
			"name": "Upload pdf",
			"step": "upload",
			"convert":"none",
			"mimetype": "application/pdf",
			"local_ext":".pdf"
		},
	]

md_flow = [
		{
			"name": "Download to markdown",
			"step": "download",
			"folder": "templates",
			"mimetype": "text/plain",
			"local_ext":".md"
		},
		{
			"name": "Merge markdown",
			"step": "merge",
			"mimetype": "text/plain",
			"local_ext":".md"
		},
		{
			"name": "Convert to html",
			"step": "markdown",
			"local_ext":".md"
		},
		{
			"name": "Upload markdown",
			"step": "upload",
			"convert":"none",
			"mimetype": "text/plain",
			"local_ext":".md"
		},
		{
			"name": "Upload html",
			"step": "upload",
			"convert":"none",
			"mimetype": "text/html",
			"local_ext":".html"
		},
		{
			"name": "Send email",
			"step": "xemail",
			"subject": "Your Tenancy",
			"from": "fake@fake.con",
			"mimetypes": ["text/plain","text/html"],
			"local_exts":[".md",".html"]
		},
	]

html_flow = [
		{
			"name": "gdoc_dl_as_html",
			"step": "download",
			"folder": "templates",
			"mimetype": "text/html",
			"local_ext":".html"
		},
		{
			"name": "merge_html",
			"step": "merge",
			"mimetype": "text/html",
			"local_ext":".html"
		},
		{
			"name": "html_ul",
			"step": "upload",
			"convert":"none",
			"mimetype": "text/html",
			"local_ext":".html"
		},
	]


def get_flow_resource(flow_folder, flow_file_name):
    flow_doc_id = folder_file(flow_folder, flow_file_name)["id"]
    doc_content = file_content_as(flow_doc_id)
    #print(doc_content)
    str_content = '{"flow":'+doc_content.decode("utf-8")+'}'
    print(str_content)
    return json.loads(str_content)["flow"]

def get_flow(flow_folder, flowcode):
    if flowcode == "docx":
    	return docx_flow
    elif flowcode == "md":
    	return md_flow
    elif flowcode == "html":
    	return html_flow
    else:
    	return get_flow_resource(flow_folder, flowcode)

def process_download(step, doc_id, doc_mimetype, localTemplateFileName, localMergedFileName):
    if step["folder"]=="templates":
         localFileName = localTemplateFileName
    else:
         localFileName = localMergedFileName
    if doc_mimetype == 'application/vnd.google-apps.document':         
    	print("export")
    	return exportFile(doc_id, localFileName+step["local_ext"], step["mimetype"])
    else:
    	print("get")
    	return getFile(doc_id, localFileName+step["local_ext"], step["mimetype"])
             #downloadFile(doc_id, localTemplateFileName+localExt, "text/html")

def process_merge(step, doc_id, localTemplateFileName, localMergedFileName, subs):
    if step["local_ext"]==".docx":
        outcome = substituteVariablesDocx(localTemplateFileName+step["local_ext"], localMergedFileName+step["local_ext"], subs)
    else:
        outcome = substituteVariablesPlain(localTemplateFileName+step["local_ext"], localMergedFileName+step["local_ext"], subs)
    return outcome

def process_markdown(step, localMergedFileName):
    outcome = convert_markdown(localMergedFileName+step["local_ext"], localMergedFileName+".html")	
    return outcome


def process_upload(step, localFileName, output_id):
    localFileName = localFileName
    if step["convert"]=="gdoc":
        return uploadAsGoogleDoc(localFileName+step["local_ext"], output_id, step["mimetype"])
    else:
    	return uploadFile(localFileName+step["local_ext"], output_id, step["mimetype"])

def process_email(step, localFileName, you, credentials):
    return email_file(localFileName, step["from"], you, step["subject"], credentials) 

def process_flow(flow, template_folder, template_name, uniq, subs, output_folder, you, email_credentials):
    doc = folder_file(template_folder, template_name)
    doc_id = doc["id"]
    doc_mimetype = doc["mimeType"]
    output_id = folder(output_folder)["id"]
    localTemplateFileName = cwd+"/merge/templates/"+template_name.split(".")[0]
    localMergedFileName = cwd+"/merge/output/"+template_name.split(".")[0]+'_'+uniq
    outcomes = []
    for step in flow:
    	if step["step"]=="download":
    	    outcome = process_download(step, doc_id, doc_mimetype, localTemplateFileName, localMergedFileName)
    	if step["step"]=="merge":
    	    outcome = process_merge(step, doc_id, localTemplateFileName, localMergedFileName, subs)
    	if step["step"]=="markdown":
    	    outcome = process_markdown(step, localMergedFileName)
    	if step["step"]=="upload":
    	    outcome = process_upload(step, localMergedFileName, output_id)
    	    doc_id = outcome["id"]
    	if step["step"]=="email":
    	    outcome = process_email(step, localMergedFileName, you, email_credentials)
    	outcomes.append({"step":step["name"], "outcome":outcome})
    return outcomes

