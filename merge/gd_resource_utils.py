import httplib2
import os
import ssl
from apiclient import discovery
from apiclient.http import MediaFileUpload
import oauth2client
from oauth2client import tools
from oauth2client import client
from apiclient import errors
from .config import install_name

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials', install_name)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'drive-echopublish.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



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


#### Navigate Drive folders

def folder_contents(parent, mimeType='application/vnd.google-apps.folder', fields="nextPageToken, files(id, name, mimeType, parents, modifiedTime)"):
    if mimeType=="*":
        q = "trashed = false and '"+parent+"' in parents"
    else:
        q = "trashed = false and mimeType = '"+mimeType+"' and '"+parent+"' in parents" 
#   try:
    if True:
        results = service.files().list(
            fields=fields, q=q).execute()
        items = results.get('files', [])
#    except:
#        return [{"name":"Google Drive Retrieval failed", "mimeType":"error"}]
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

def gd_folder_files(path, parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents)"):
        print(fields)
        foldr = folder(path, parent)
        contents = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
        return contents

#    try:
#        foldr = folder(path, parent)
#        contents = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
#    except (errors.HttpError, ssl.SSLError) as ex:
#        try:
#            foldr = folder(path, parent)
#            contents = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
#        except (errors.HttpError, ssl.SSLError) as ex:
#            contents = []
#    except IOError as e:
#        print("IO Error")
#        print(e)
##        if e.errno == errno.EPIPE:        
##            try:
##                foldr = folder(path, parent)
##                contents = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
##            except:
##                contents = []
#    return contents

def gd_path_equivalent(path):
    if path.lower().find("templates")==0:
        remote_equiv = path.replace(path.split("/")[0],"/Doc Merge/Templates")
    elif path.lower().find("flows")==0:
        remote_equiv = path.replace(path.split("/")[0],"/Doc Merge/Flows")
    elif path.lower().find("branding")==0:
        remote_equiv = path.replace(path.split("/")[0],"/Doc Merge/Branding")
    elif path.lower().find("test_data")==0:
        remote_equiv = path.replace(path.split("/")[0],"/Doc Merge/Test Data")
    elif path.lower().find("transforms")==0:
        remote_equiv = path.replace(path.split("/")[0],"/Doc Merge/Transforms")
    elif path.lower().find("output")==0:
        remote_equiv = path.replace(path.split("/")[0],"/Doc Merge/Output")
    else:
        remote_equiv = None    
    return remote_equiv


def create_folder(parent_id, name):
    folder_metadata = {
      'name' : name,
      'parents' : [parent_id],
      'mimeType' : 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder


    
def folder_file(path, name, parent='root', mimeType='*'):
    foldr = folder(path, parent)
    return folder_item(foldr["id"], name, mimeType=mimeType)
    
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


def initialiseService():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
if (os.getcwd().find("home")>=0):  #pythonanywhere deployment
    CLIENT_SECRET_FILE = '/home/docmerge/'+install_name+'/client_secret.json'
APPLICATION_NAME = 'Echo Publish'

service = initialiseService()
