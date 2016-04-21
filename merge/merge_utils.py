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

import smtplib

# Import the email modules we'll need
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
    return {"file":fileNameOut}
    
def preprocess(text):
    text = text.replace("{% #A %}", "{% cycle 'A' 'B' 'C' 'D' 'E' 'F' 'G' 'H' 'I' 'J' 'K' 'L' 'M' 'N' 'O' 'P' 'Q' 'R' 'S' 'T' 'U' 'V' 'W' 'X' 'Y' 'Z'%}")    
    text = text.replace("{% #9 %}", "{% cycle '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11' '12' '13' '14' '15' '16' '17' '18' '19' '20' as level1 %}")    
    text = text.replace("{% #9= %}", "{{ level1 }}")    
    return text


def docx_copy_run_style_from(run1, run2):
    run1.font.color.rgb = run2.font.color.rgb
    run1.font.all_caps = run2.font.all_caps
    run1.font.bold = run2.font.bold
    run1.font.italic = run2.font.italic
    run1.font.size = run2.font.size
    run1.font.underline = run2.font.underline
    #complex_script, cs_bold, cs_italic, double_strike, emboss, hidden, highlight_color,
    #imprint, math, name, no_proof, outline, rtl, shadow, small_caps, snap_to_grid, spec_vanish, 
    #strike, superscript, underline, web_hidden

def substituteVariablesDocx(fileNameIn, fileNameOut, subs):
    c = Context(subs)
    doc = Document(docx=fileNameIn)
    fullText=""
    paras=doc.paragraphs
    control_paras = []  # starting and ending {%  %}
    i = 0
    for para in paras:
        paraText=""
        runs = para.runs
        j = 0
        for run in runs:
            print(run.text, run.font)

            txt = run.text
            paraText+= txt+"+"+str(j)+"+run+"
            j+=1
#        print(paraText)
        if paraText.find("{%")>=0:
#            print(">>>",paraText[paraText.find("{%"):paraText.find("%}")+2])
            non_control_text=paraText[:paraText.find("{%")].strip()+paraText[paraText.find("%}")+2:].strip()
#            print(">>>",non_control_text)
            if non_control_text.find('+0+run+')==0: # pure control para should not show up in output
#                print("control para")
                control_paras.append(i)
        fullText+= paraText+str(i)+"+para+"
        i+=1
#   print(fullText)
    fullText = preprocess(fullText)
    t = Template(fullText)
    xtxt = t.render(c)
    print(xtxt)
    xParaTxts = xtxt.split("+para+")
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
#                else:
#                    print(">> using", para_n, txt)
#                    print(used)
#                    print(unused)
            else:   
                if not(para_n in control_paras):
 #                   print(">> inserting", para_n, unused[0], txt)
 #                   print(used)
 #                   print(unused)
 #                   print()
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
 #               print(p.text)
                for runTxt in runTxts[:-1]:
                    try:
                        txt = runTxt.split("+")[-2]
                    except:
                        txt=""
                    run_n = int(runTxt.split("+")[-1])
                    print(para_n, run_n, txt, paras[para_n].runs[run_n].font)
                    r = paras[para_n].runs[run_n]
                    if ('{' in r.text):
                        r.text = txt
                    elif reused:
                        run = p.add_run(text=txt, style=paras[para_n].runs[run_n].style)
                        docx_copy_run_style_from(run, paras[para_n].runs[run_n])

    for unused_p in unused:
        p = paras[unused_p]
        removePara(p)

    doc.save(fileNameOut)
    return {"file":fileNameOut}


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

def getPdf(doc_id, fileNameOut="writeTest.pdf"): #assuming a google docs file
    content_pdf = file_export(service, doc_id)
    outfile = open(fileNameOut,"wb")
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
    return {"file":fileNameOut}

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
            print(">>Try to create")
            next_level = create_folder(parent, pathlist[0])
        else:
            raise ex   
    if len(pathlist)==1:
        return next_level
    else:
        return ls_list(pathlist[1:], parent = next_level['id'], create_if_absent=create_if_absent)

def folder(path, parent='root', create_if_absent=False):
    print("path=",path)
    path_parts = path.split("/")
    if parent == 'root':
        path_parts = path_parts[1:]
    return ls_list(path_parts, parent=parent, create_if_absent=create_if_absent)

def folder_files(path, parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents)"):
    try:
        foldr = folder(path, parent)
        contents = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
    except (errors.HttpError, errors.SSLError, errors.BrokenPipeError) as ex:
        try: #1 f
            foldr = folder(path, parent)
            contents = folder_contents(foldr["id"], mimeType=mimeType, fields=fields)
        except (errors.HttpError, errors.SSLError, errors.BrokenPipeError) as ex:
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
    
def email_file(baseFileName, me, you, subject, credentials):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you.replace(" ","+")

    mimetypes = ["text/plain", "text/html"]
    file_exts = [".md", ".html"]

    for mime in zip(mimetypes, file_exts):
        file=baseFileName+mime[1]
        fp = open(file, 'r')
        content = fp.read()
        fp.close()
        print(mime[0].split("/"))
        msg.attach(MIMEText(content, mime[0].split("/")[1]))    
    
    username = credentials["username"]
    password = credentials["password"]
    server = smtplib.SMTP(credentials["server"])

    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password)
    print(me)
    print(you.replace(" ","+"))
    print(msg.as_string())
    response = server.sendmail(me, [you.replace(" ","+")], msg.as_string())
    server.quit()
    return {"email":you.replace(" ","+")}

def get_working_dir():
    cwd = os.getcwd()
    if (cwd.find("home")>=0):  
        cwd = cwd+"/docmerge"
    if (cwd.find("scripts")>=0):  
        cwd = cwd.replace("\scripts","")
    return cwd

def get_output_dir():
    cwd = os.getcwd()
    if (cwd.find("home")>=0):  
        opd = "/home/docmerge/docmerge/merge/output"
    else:  
        opd = "C:\\Users\\Andrew\\Documents\\GitHub\\docmerge\\merge\\output"
    return opd

def get_local_dir(local):
    cwd = os.getcwd()
    if (cwd.find("home")>=0):  
        opd = "/home/docmerge/docmerge/merge/"+local
    else:  
        opd = "C:\\Users\\Andrew\\Documents\\GitHub\\docmerge\\merge\\"+local
    return opd

def local_textfile_content(filename, filepath=get_output_dir()):
    file_content=""
    with open(filepath+"/"+filename) as file:
        for line in file:
            file_content+=(line+"\n")
    #return {"content":file_content}
    return file_content

def get_remote_txt_content(data_folder, data_file):
    data_doc_id = folder_file(data_folder, data_file)["id"]
    doc_txt = file_content_as(data_doc_id)
    return doc_txt

def get_local_txt_content(cwd, data_folder, data_file):
#def get_flow_local(cwd, flow_local_folder, flow_file_name):
    try:
        print(cwd+"/merge/"+data_folder+"/"+data_file)
        with open(cwd+"/merge/"+data_folder+"/"+data_file, "r") as file:
            return  file.read()
    except FileNotFoundError:
        return None

def get_txt_content(local_data_folder, remote_data_folder, data_file):
    print("looking locally")
    content = get_local_txt_content(get_working_dir(), local_data_folder, data_file)
    if content == None:
        print("looking remotely")
        content = get_remote_txt_content(remote_data_folder, data_file)
    return content

def strip_xml_dec(content):
    print(content[:20])
    xml_dec_start = content.find("<?xml")
    if xml_dec_start>=0:
        return content[content.find(">")+1:]
    else:
        return content



def get_xml_content(local_data_folder, remote_data_folder, data_file):
    content = get_txt_content(local_data_folder, remote_data_folder, data_file)
    if type(content) is bytes:
        content = content.decode("UTF-8")
    return strip_xml_dec(content)

def push_local_txt(cwd, data_folder, data_file, payload):
    full_file_path = data_file
    with open(full_file_path, "w") as file:
        file.write(payload)
        file.close()
    return full_file_path


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
if (os.getcwd().find("home")>=0):  #pythonanywhere deployment
    CLIENT_SECRET_FILE = '/home/docmerge/docmerge/client_secret.json'
APPLICATION_NAME = 'Echo Publish'


service = initialiseService()



#docs = folder_files("/Doc Merge/Templates")
#print([file["name"] for file in docs])
#print([(file["name"],file["name"]) for file in folder_files("/Doc Merge/Templates")])
