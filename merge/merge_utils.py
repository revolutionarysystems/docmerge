import httplib2
import os
from subprocess import check_output

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

#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    #print(credential_dir)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

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

def replaceParams(txt, subs):
    for key in subs.keys():
        old = "${"+key+"}"
        if (txt.find(old)>=0):
            txt = txt.replace(old, subs[key])
 #   print(txt)
    return txt

def removePara(para):
        p = para._element
        p.getparent().remove(p)
        p._p = p._element = None

def substituteVariablesPlain(fileNameIn, fileNameOut, subs):
    c = Context(subs)
    fileIn = open(fileNameIn, "r")
    fullText = fileIn.read()
    t = Template(fullText)
    xtxt = t.render(c)
    fileOut = open(fileNameOut, "w")
    fileOut.write(xtxt)
    


def substituteVariablesDocx(fileNameIn, fileNameOut, subs):
    c = Context(subs)
    doc = Document(docx=fileNameIn)
    #docOut = Document()
    fullText=""
    paras=doc.paragraphs
    control_paras = []  # starting and ending {%  %}
    i = 0
    for para in paras:
        paraText=""
        runs = para.runs
        j = 0
        for run in runs:
            txt = run.text
            paraText+= txt+"+"+str(j)+"+run+"
            j+=1
        #print(txt)
        if paraText.find("{%")>=0:
            control_paras.append(i)
        fullText+= paraText+str(i)+"+para+"
        i+=1

    t = Template(fullText)
    xtxt = t.render(c)
    xParaTxts = xtxt.split("+para+")

#    for para in doc.paragraphs:
#        p = para._element
#        p.getparent().remove(p)
#        p._p = p._element = None

    used = []
    unused = list(range(0,len(paras)))
    for xParaTxt in xParaTxts:
        #print(used, unused)
        runTxts = xParaTxt.split("+run+")
        if runTxts[-1]!='':
            para_n = int(runTxts[-1])
            reused = para_n in used
            if not(reused):
                p = paras[para_n]
                used.append(para_n)
                unused.remove(para_n)
                if para_n in control_paras:
                    removePara(p)
            else:   
                if not(para_n in control_paras):
                    p = paras[unused[0]].insert_paragraph_before(text=txt, style=paras[para_n].style)
                    p.clear()
                    p.paragraph_format.alignment = paras[para_n].paragraph_format.alignment
                    p.paragraph_format.first_line_indent = paras[para_n].paragraph_format.first_line_indent
                    p.paragraph_format.keep_together = paras[para_n].paragraph_format.keep_together
                    p.paragraph_format.keep_with_next = paras[para_n].paragraph_format.keep_with_next
                    p.paragraph_format.left_indent = paras[para_n].paragraph_format.left_indent
                    p.paragraph_format.line_spacing = paras[para_n].paragraph_format.line_spacing
                    p.paragraph_format.line_spacing_rule = paras[para_n].paragraph_format.line_spacing_rule
                    p.paragraph_format.page_break_before = paras[para_n].paragraph_format.page_break_before
                    p.paragraph_format.right_indent = paras[para_n].paragraph_format.right_indent
                    p.paragraph_format.space_after = paras[para_n].paragraph_format.space_after
                    p.paragraph_format.space_before = paras[para_n].paragraph_format.space_before
                    p.paragraph_format.widow_control = paras[para_n].paragraph_format.widow_control


            if reused or ('{' in p.text):   # replace para text
                for runTxt in runTxts[:-1]:
                    try:
                        txt = runTxt.split("+")[-2]
                    except:
                        txt=""
                    run_n = int(runTxt.split("+")[-1])
                    r = paras[para_n].runs[run_n]
                    if ('{' in r.text):
                        r.text = txt
                    elif reused:
                        p.add_run(text=txt, style=paras[para_n].runs[run_n].style)
            #print(p.text)

    doc.save(fileNameOut)



def uploadFile(fileName, folder, mimeType):
    body ={}
    body["name"]=fileName
    body["parents"]=[folder]
    media = MediaFileUpload(fileName, mimetype=mimeType, resumable=1)
    request = service.files().create(body=body, media_body=media)
    upload = request.execute()
    return upload

def getPdf(doc_id): #assuming a google docs file
    content_pdf = file_export(service, doc_id)
    outfile = open("writeTest.pdf","wb")
    outfile.write(content_pdf)
    outfile.close()


#def getContent(fileId):
#exportUrl = "https://docs.google.com/document/d/"+docId+"/export?format=doc"
#print(exportUrl)
#urllib.request.urlretrieve (exportUrl, "sample.docx")

def shellCommand(command):
    #print(check_output("dir C:", shell=True).decode())
    return check_output(command, shell=True).decode()


#doc_id_2 = uploadFile("amendTest.docx", 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')["id"]
#print(doc_id_2)

def convertToPdf(fileName, outdir = "."):
    return shellCommand("soffice --headless --convert-to pdf "+fileName+" --outdir "+outdir)


def initialiseService():
    #django templates   
#    settings.configure()
#    django.setup()

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    return service


def convert_markdown(fileNameIn, fileNameOut):
    fileIn = open(fileNameIn, "r")
    fileOut = open(fileNameOut, "w")
    fileOut.write(markdown(fileIn.read()))
    fileOut.close()

#### Navigate Drive folders

def folder_contents(parent, mimeType='application/vnd.google-apps.folder', ):
    if mimeType=="*":
        q = "'"+parent+"' in parents"
    else:
        q = "mimeType = '"+mimeType+"' and '"+parent+"' in parents" 

    results = service.files().list(
        fields="nextPageToken, files(id, name, mimeType, parents)", q=q).execute()
#        pageSize=50,fields="nextPageToken, files(id, name, mimeType)", q="'0B-R1VJ7CNz2ZYlI0M3ROR0YzS00' in parents").execute()
    items = results.get('files', [])
    return items

def folder_item(parent, name, mimeType='application/vnd.google-apps.folder', ):
    if mimeType=="*":
        q = "name = '"+name+"' and '"+parent+"' in parents"
    else:
        q = "mimeType = '"+mimeType+"' and name = '"+name+"' and '"+parent+"' in parents"
    results = service.files().list(
        fields="nextPageToken, files(id, name, mimeType, parents)", q=q).execute()
    items = results.get('files', [])
    return items[0]

def ls_list(pathlist, parent='root'):
    next_level = folder_item(parent, pathlist[0])
    if len(pathlist)==1:
        return next_level
    else:
        return ls_list(pathlist[1:], parent = next_level['id'])

def folder(path, parent='root'):
    path_parts = path.split("/")
    if parent == 'root':
        path_parts = path_parts[1:]
    return ls_list(path_parts, parent=parent)

def folder_files(path, parent='root', mimeType='*'):
    foldr = folder(path, parent)
    return folder_contents(foldr["id"], mimeType=mimeType)
    
def folder_file(path, name, parent='root', mimeType='*'):
    foldr = folder(path, parent)
    return folder_item(foldr["id"], name, mimeType=mimeType)
    




SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'RevSys DocMerge'

#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None


service = initialiseService()

#settings.configure(TEMPLATE_DIRS=("./templates",))
#django.setup()
