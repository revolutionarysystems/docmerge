import os
#import django
#from django.conf import settings
from random import randint

from .merge_utils import initialiseService, downloadFile, substituteVariablesDocx, substituteVariablesPlain, convertToPdf,uploadFile,convert_markdown,folder_file,folder,email_file

credentials = {"username":"DOCMERGE\\andrew", "password":"mnemonic10", "server":"ssrs.reachmail.net:25"}

cwd = os.getcwd()
if (cwd.find("home")>=0):
    cwd = cwd+"/docmerge"
def mergeDocument(flow, template_folder, template_name, uniq, subs, output_folder, email=None):
    doc_id = folder_file(template_folder, template_name)["id"]
    output_id = folder(output_folder)["id"]
    localTemplateFileName = cwd+"/merge/templates/"+template_name.split(".")[0]
    localMergedFileName = cwd+"/merge/output/"+template_name.split(".")[0]
    outcomes = {}


    if flow == "docx":
        localExt=".docx"    
        outcomes["gdoc_dl_as_docx"]=downloadFile(doc_id, localTemplateFileName+localExt, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        outcomes["merge_docx"]=substituteVariablesDocx(localTemplateFileName+localExt, localMergedFileName+'_'+uniq+localExt, subs)
        outcomes["pdf_conversion"]=str(convertToPdf(localMergedFileName+'_'+uniq+localExt, outdir="./merge/output"))
        outcomes["pdf_upload"]=uploadFile(localMergedFileName+'_'+uniq+".pdf", output_id, "application/pdf")
        outcomes["pdf_link"]=''.join(["https://drive.google.com/a/revolutionarysystems.co.uk/file/d/",outcomes["pdf_upload"]["id"],"/view?usp=sharing"])
    if flow =="html":
        localExt=".html"    
        #downloadFile(doc_id, localTemplateFileName+localExt, "text/html")
        substituteVariablesPlain(localTemplateFileName+localExt, localMergedFileName+'_'+uniq+localExt, subs)
        uploadFile(localMergedFileName+localExt, output_id, "text/html")
    if flow =="md":
        localExt=".md"    
        outcomes["gdoc_dl_as_text"]=downloadFile(doc_id, localTemplateFileName+localExt, "text/plain")
        outcomes["merge_text"]=substituteVariablesPlain(localTemplateFileName+localExt, localMergedFileName+'_'+uniq+localExt, subs)
        outcomes["process_md"]=convert_markdown(localMergedFileName+'_'+uniq+localExt, localMergedFileName+'_'+uniq+".html")
        outcomes["md_upload"]=uploadFile(localMergedFileName+'_'+uniq+localExt, output_id, "text/plain")
        outcomes["md_link"]=''.join(["https://drive.google.com/a/revolutionarysystems.co.uk/file/d/",outcomes["md_upload"]["id"],"/view?usp=sharing"])
        outcomes["html_upload"]=uploadFile(localMergedFileName+'_'+uniq+".html", output_id, "text/html")
        outcomes["html_link"]=''.join(["https://drive.google.com/a/revolutionarysystems.co.uk/file/d/",outcomes["html_upload"]["id"],"/view?usp=sharing"])
        if email:
            outcomes["email"]=email_file(localMergedFileName+'_'+uniq, "fake@fake.com", email, "Your Tenancy", credentials)
#        https://drive.google.com/a/revolutionarysystems.co.uk/file/d/0B-R1VJ7CNz2ZOUh2ZHJORXM3M3c/view?usp=sharing

    return outcomes



