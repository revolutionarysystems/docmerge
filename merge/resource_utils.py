import os
import zipfile
from .config import install_name
from .gd_resource_utils import folder, folder_contents, exportFile, getFile, folder_item

## Local Resource management

def get_working_dir():
    cwd = os.getcwd()
    if (cwd.find("home")>=0):  
        cwd = os.path.join(cwd,install_name)
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



# Remote <-> Local methods

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

def zip_local_dirs(path, zip_file_name, selected_subdirs = ["templates", "flows", "transforms", "test_data", "branding"]):
    zip_name = os.path.join(path,zip_file_name+".zip")
    ziph = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            relpath = os.path.relpath(os.path.join(root, file), os.path.join(path, '..'))
            if selected_subdirs == None or relpath.split(os.path.sep)[1] in selected_subdirs:
                ziph.write(os.path.join(root, file), relpath)
    ziph.close()
    return zip_name


