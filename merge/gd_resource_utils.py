import httplib2
import os
import ssl
from time import sleep
from apiclient.http import MediaFileUpload
from apiclient import errors
from apiclient.errors import HttpError
from .config import install_name, gdrive_root, remote_library
from .gd_service import get_service, protected_execute
from docmerge.settings import MULTI_TENANTED


def file_content(service, file_id):
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

def file_content_as(config, doc_id):
    content = file_get(get_service(config), doc_id)
    return content

def getFile(config, doc_id, fileName, mimetype):
    content_doc = file_get(get_service(config), doc_id)
    try:
        outfile = open(fileName,"wb")
        outfile.write(content_doc)
    except:
        outfile = open(fileName,"w")
        outfile.write(content_doc)
    outfile.close()
    return {"file":fileName}



def downloadFile(config, doc_id, fileName, mimetype):
    content_doc = file_export(get_service(config), doc_id, mimetype)
    try:
        outfile = open(fileName,"wb")
        outfile.write(content_doc)
    except:
        outfile = open(fileName,"w")
        outfile.write(content_doc)
    outfile.close()
    return {"file":fileName}

def exportFile(config, doc_id, fileName, mimetype):
    #print_file_metadata(service, doc_id)
    #content = file_content(service, docId)
    content_doc = file_export(get_service(config), doc_id, mimetype)
    try:
        outfile = open(fileName,"wb")
        outfile.write(content_doc)
    except:
        outfile = open(fileName,"w")
        outfile.write(content_doc)
    outfile.close()
    return {"file":fileName}

def uploadAsGoogleDoc(config, fileName, folder, mimeType, name=None):
    body ={}
    if name==None:
        body["name"]=fileName
    else:
        body["name"]=name
    body["parents"]=[folder]
    body["mimeType"]='application/vnd.google-apps.document'
    ##
    #'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    media = MediaFileUpload(fileName, mimetype=mimeType, resumable=True)
    request = get_service(config).files().create(body=body, media_body=media)
    upload = request.execute()
    return upload

def uploadFile(config, fileName, folder, mimeType, name=None):
    body ={}
    if name==None:
        body["name"]=fileName
    else:
        body["name"]=name
    body["parents"]=[folder]
    media = MediaFileUpload(fileName, mimetype=mimeType, resumable=True)
    request = get_service(config).files().create(body=body, media_body=media)
    upload = request.execute()
#    id =upload["id"]
#    body ={}
#    body["name"]=fileName.split("/")[-1]
#    update_request = get_service(config).files().update(fileId=id, body=body)
#    update = update_request.execute()
    return upload


#### Navigate Drive folders

def protected_execute_contents(config, query, fields, max_tries=4, wait_time=0.2):
    results = []
    for i in range(max_tries):
        try:
            results = get_service(config).files().list(fields=fields, q=query).execute()
            break
        except (HttpError, TypeError) as e  :
            if i+1<max_tries:
                sleep(wait_time)
                wait_time = 2* wait_time
            else:
                raise e
        except client.HttpAccessTokenRefreshError:
            initialise(config)            
    return results

def folder_contents(config, parent, mimeType='application/vnd.google-apps.folder', fields="nextPageToken, files(id, name, mimeType, parents, modifiedTime)"):
    if mimeType=="*":
        q = "trashed = false and '"+parent+"' in parents"
    else:
        q = "trashed = false and mimeType = '"+mimeType+"' and '"+parent+"' in parents" 
    ## Catch HttpError 403 - user rate limit - use protected method
    results = protected_execute_contents(config, q, fields)

    #results = get_service(config).files().list(fields=fields, q=q).execute()
    items = results.get('files', [])
    return items


def folder_item(config, parent, name, mimeType='application/vnd.google-apps.folder', ):
    if remote_library:
        if mimeType=="*":
            q = "name = '"+name+"' and '"+parent+"' in parents"
        else:
            q = "mimeType = '"+mimeType+"' and name = '"+name+"' and '"+parent+"' in parents"
        results = protected_execute(config, q)
        items = results.get('files', [])
        try:
            return items[0]
        except:
            raise FileNotFoundError("'"+name+"' was not found")
    else:
        raise FileNotFoundError("'"+name+"' was not found. No remote library")

def ls_list(config, pathlist, parent='root', create_if_absent=False):
    try:
        next_level = folder_item(config, parent, pathlist[0])
    except FileNotFoundError as ex:
        if create_if_absent:
            next_level = create_folder(config, parent, pathlist[0])
        else:
            raise ex   
    if len(pathlist)==1:
        return next_level
    else:
        return ls_list(config, pathlist[1:], parent = next_level['id'], create_if_absent=create_if_absent)

def folder(config, path, parent='root', create_if_absent=False):
    path_parts = path.split("/")
    if parent == 'root':
        path_parts = path_parts[1:]
    return ls_list(config, path_parts, parent=parent, create_if_absent=create_if_absent)

def gd_folder_files(config, path, parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents)"):
        foldr = folder(config, path, parent)
        contents = folder_contents(config, foldr["id"], mimeType=mimeType, fields=fields)
        return contents

def gd_folder_item(config, path, filename, parent='root', mimeType='*'):
        foldr = folder(config, path, parent)
        contents = folder_item(config, foldr["id"], filename, mimeType=mimeType)
        return contents

def gd_path_equivalent(config, path):
    if MULTI_TENANTED:
        tenant_extension = "/"+config.tenant
    else:
        tenant_extension = ""
    if path.lower().find("templates")==0:
        remote_equiv = path.replace(path.split("/")[0],"/"+gdrive_root+tenant_extension+"/Templates")
    elif path.lower().find("flows")==0:
        remote_equiv = path.replace(path.split("/")[0],"/"+gdrive_root+tenant_extension+"/Flows")
    elif path.lower().find("branding")==0:
        remote_equiv = path.replace(path.split("/")[0],"/"+gdrive_root+tenant_extension+"/Branding")
    elif path.lower().find("test_data")==0:
        remote_equiv = path.replace(path.split("/")[0],"/"+gdrive_root+tenant_extension+"/Test Data")
    elif path.lower().find("transforms")==0:
        remote_equiv = path.replace(path.split("/")[0],"/"+gdrive_root+tenant_extension+"/Transforms")
    elif path.lower().find("output")==0:
        remote_equiv = path.replace(path.split("/")[0],"/"+gdrive_root+tenant_extension+"/Output")
    else:
        remote_equiv = None    
    return remote_equiv

def gd_mimetype_equivalent(ftype):
    if ftype == "gdoc":
        mimetype_equiv = 'application/vnd.google-apps.document'
    elif ftype == ".docx":
        mimetype_equiv = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif ftype == ".txt":
        mimetype_equiv = "text/plain"
    elif ftype == ".flo":
        mimetype_equiv = "application/json"
    elif ftype == ".xml":
        mimetype_equiv = "application/xml"
    elif ftype == ".json":
        mimetype_equiv = "application/json"
    elif ftype == ".pdf":
        mimetype_equiv = "application/pdf"
    elif ftype == ".zip":
        mimetype_equiv = "application/zip"
    else:
        mimetype_equiv = "application/octet-stream"
    return mimetype_equiv


def create_folder(config, parent_id, name):
    folder_metadata = {
      'name' : name,
      'parents' : [parent_id],
      'mimeType' : 'application/vnd.google-apps.folder'
    }
    folder = get_service(config).files().create(body=folder_metadata, fields='id').execute()
    return folder

def folder_file(config, path, name, parent='root', mimeType='*'):
    foldr = folder(config, path, parent)
    return folder_item(config, foldr["id"], name, mimeType=mimeType)
    
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

def gd_build_folders(config):
    folders = [
            "templates", 
            "templates/Sandbox", 
            "templates/Demo Examples", 
            "transforms",
            "flows",
            "branding",
            "test_data",
            "output",
            ]
    for subfolder in folders:
        path = gd_path_equivalent(config, subfolder) 
        folder(config, path, create_if_absent=True)  



