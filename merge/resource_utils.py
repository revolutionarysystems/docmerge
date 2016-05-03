import httplib2
import os
import string
import ssl
from subprocess import check_output
import zipfile
import tempfile
import shutil

from apiclient import discovery
from apiclient.http import MediaFileUpload
import oauth2client
from oauth2client import tools
from oauth2client import client

from docx import Document
from docx.text.paragraph import Paragraph


import django
from django.template import Template, Context
from django.conf import settings

from apiclient import errors
from markdown import markdown

import smtplib

# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .config import install_name


#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

def get_working_dir():
    cwd = os.getcwd()
    if (cwd.find("home")>=0):  
        cwd = cwd+"/docmerge"
    if (cwd.find("scripts")>=0):  
        cwd = cwd.replace("\scripts","")
    return cwd

def strip_xml_dec(content):
    xml_dec_start = content.find("<?xml")
    if xml_dec_start>=0:
        return content[content.find(">")+1:]
    else:
        return content

def get_local_dir(local):
    cwd = os.getcwd()
    if (cwd.find("home")>=0):  
        local_d = "/home/docmerge/"+install_name+"/merge/"+local
    else:  
        local_d = "C:\\Users\\Andrew\\Documents\\GitHub\\docmerge\\merge\\"+local
    return local_d

def get_output_dir():
    return get_local_dir("output")

def get_local_txt_content(cwd, data_folder, data_file):
    try:
        full_file_path = os.path.join(cwd, "merge", data_folder, data_file)
        print(full_file_path)
        with open(cwd+"/merge/"+data_folder+"/"+data_file, "r") as file:
            return  file.read()
    except FileNotFoundError:
        return None

def push_local_txt(cwd, data_folder, data_file, payload):
    full_file_path = os.path.join(cwd, "merge", data_folder, data_file)
#    full_file_path = data_file
    with open(full_file_path, "w") as file:
        file.write(payload)
        file.close()
    return full_file_path

def del_local(cwd, data_folder, data_file):
    full_file_path = os.path.join(cwd, "merge", data_folder, data_file)
    os.remove(full_file_path)




def file_content(service, file_id):
  """Return a file's content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file.

  Returns:
    File's content if successful, None otherwise.
  """
  try:
    content = service.files().get_media(fileId=file_id).execute()
    return content
  except errors.HttpError as error:
    print('An error occurred: %s' % error)
    print(error.__dict__)
    return ""

def file_export(service, file_id, mimetype="application/pdf"):
  try:
    content = service.files().export_media(fileId=file_id, mimeType=mimetype).execute()
    return content
  except errors.HttpError as error:
    print('An error occurred: %s' % error)
    print(error.__dict__)
    return ""

def file_get(service, file_id):
  try:
    content = service.files().get_media(fileId=file_id).execute()
    return content
  except errors.HttpError as error:
    print('An error occurred: %s' % error)
    print(error.__dict__)
    return ""

def file_content_as(doc_id):
    content = file_get(service, doc_id)
#    content = '<ItpDocumentRequest xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><DocumentCode>AgreementTimerExtended</DocumentCode></ItpDocumentRequest>'
    return content

def getFile(doc_id, fileName, mimetype):
    #print_file_metadata(service, doc_id)
    #content = file_content(service, docId)
    content_doc = file_get(service, doc_id)
    try:
        outfile = open(fileName,"wb")
        outfile.write(content_doc)
    except:
        outfile = open(fileName,"w")
        outfile.write(content_doc)
    outfile.close()
    return {"file":fileName}



def downloadFile(doc_id, fileName, mimetype):
    #print_file_metadata(service, doc_id)
    #content = file_content(service, docId)
    content_doc = file_export(service, doc_id, mimetype)
    try:
        outfile = open(fileName,"wb")
        outfile.write(content_doc)
    except:
        outfile = open(fileName,"w")
        outfile.write(content_doc)
    outfile.close()
    return {"file":fileName}

def exportFile(doc_id, fileName, mimetype):
    #print_file_metadata(service, doc_id)
    #content = file_content(service, docId)
    content_doc = file_export(service, doc_id, mimetype)
    try:
        outfile = open(fileName,"wb")
        outfile.write(content_doc)
    except:
        outfile = open(fileName,"w")
        outfile.write(content_doc)
    outfile.close()
    return {"file":fileName}

def replaceParams(txt, subs):
    for key in subs.keys():
        old = "${"+key+"}"
        if (txt.find(old)>=0):
            txt = txt.replace(old, subs[key])
    return txt


def print_doc(doc):
    paras=doc.paragraphs
    print("...")
    for para in paras[14:20]:
        print(para.text)
    print("...")




def uploadAsGoogleDoc(fileName, folder, mimeType):
    body ={}
    body["name"]=fileName
    body["parents"]=[folder]
    body["mimeType"]='application/vnd.google-apps.document'
    ##
    #'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    media = MediaFileUpload(fileName, mimetype=mimeType, resumable=True)
    request = service.files().create(body=body, media_body=media)
    upload = request.execute()
    return upload


def uploadFile(fileName, folder, mimeType):
    body ={}
    body["name"]=fileName
    body["parents"]=[folder]
    media = MediaFileUpload(fileName, mimetype=mimeType, resumable=True)
    request = service.files().create(body=body, media_body=media)
    upload = request.execute()
    id =upload["id"]
    body ={}
    body["name"]=fileName.split("/")[-1]
    update_request = service.files().update(fileId=id, body=body)
    update = update_request.execute()
    return update



def initialiseService():
    #django templates   
#    settings.configure()
#    django.setup()

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service



#### Navigate Drive folders

def folder_contents(parent, mimeType='application/vnd.google-apps.folder', fields="nextPageToken, files(id, name, mimeType, parents)"):
    if mimeType=="*":
        q = "trashed = false and '"+parent+"' in parents"
    else:
        q = "trashed = false and mimeType = '"+mimeType+"' and '"+parent+"' in parents" 

    try:
        results = service.files().list(
            fields=fields, q=q).execute()
#        pageSize=50,fields="nextPageToken, files(id, name, mimeType)", q="'0B-R1VJ7CNz2ZYlI0M3ROR0YzS00' in parents").execute()
        items = results.get('files', [])
    except:
        return []
    return items

def folder_item(parent, name, mimeType='application/vnd.google-apps.folder', ):
    if mimeType=="*":
        q = "name = '"+name+"' and '"+parent+"' in parents"
    else:
        q = "mimeType = '"+mimeType+"' and name = '"+name+"' and '"+parent+"' in parents"
    results = service.files().list(
        fields="nextPageToken, files(id, name, mimeType, parents)", q=q).execute()
    items = results.get('files', [])
    try:
        return items[0]
    except:
        raise FileNotFoundError("'"+name+"' was not found")

def ls_list(pathlist, parent='root', create_if_absent=False):
    try:
        next_level = folder_item(parent, pathlist[0])
    except FileNotFoundError as ex:
        if create_if_absent:
#            print(">>Try to create")
            next_level = create_folder(parent, pathlist[0])
        else:
            raise ex   
    if len(pathlist)==1:
        return next_level
    else:
        return ls_list(pathlist[1:], parent = next_level['id'], create_if_absent=create_if_absent)

def folder(path, parent='root', create_if_absent=False):
#    print("path=",path)
    path_parts = path.split("/")
    if parent == 'root':
        path_parts = path_parts[1:]
    return ls_list(path_parts, parent=parent, create_if_absent=create_if_absent)

def folder_files(path, parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents)"):
    try:
        foldr = folder(path, parent)
        contents = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
    except (errors.HttpError, ssl.SSLError) as ex:
        try:
            foldr = folder(path, parent)
            contents = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
        except (errors.HttpError, ssl.SSLError) as ex:
            contents = []
    return contents

def create_folder(parent_id, name):
    folder_metadata = {
      'name' : name,
      'parents' : [parent_id],
      'mimeType' : 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder

def refresh_files(path, local_dir, parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents)"):
    foldr = folder(path, parent)
    files = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
    files_info=[]
    for file in files:
        doc_id =file["id"]
        cwd = get_working_dir()
        localFileName = cwd+"/merge/"+local_dir+"/"+file["name"]
        if file["mimeType"] == 'application/vnd.google-apps.folder':
            pass
        elif file["mimeType"] == 'application/vnd.google-apps.document':
            if localFileName.find(".") < 0: # no extension
                files_info.append(exportFile(doc_id, localFileName+".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
            else:
                files_info.append(exportFile(doc_id, localFileName, "text/plain"))
        else:
            files_info.append(getFile(doc_id, localFileName, file["mimeType"]))
    return files_info


    
def folder_file(path, name, parent='root', mimeType='*'):
    foldr = folder(path, parent)
    return folder_item(foldr["id"], name, mimeType=mimeType)
    

#def local_textfile_content(filename, filepath=get_output_dir()):
#    file_content=""
#    with open(filepath+"/"+filename) as file:
#        for line in file:
#            file_content+=(line+"\n")
#    #return {"content":file_content}
#    return file_content

def get_remote_txt_content(data_folder, data_file):
    data_doc_id = folder_file(data_folder, data_file)["id"]
    doc_txt = file_content_as(data_doc_id)
    return doc_txt

def get_txt_content(local_data_folder, remote_data_folder, data_file):
#    print("looking locally")
    content = get_local_txt_content(get_working_dir(), local_data_folder, data_file)
    if content == None:
#        print("looking remotely")
        content = get_remote_txt_content(remote_data_folder, data_file)
    return content

def get_xml_content(local_data_folder, remote_data_folder, data_file):
    content = get_txt_content(local_data_folder, remote_data_folder, data_file)
    if type(content) is bytes:
        content = content.decode("UTF-8")
    return strip_xml_dec(content)

