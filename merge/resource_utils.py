import os
import time
import pytz
import iso8601
import datetime
import zipfile
import stat
from .config import install_name, remote_library, gdrive_root, local_root, extend_path
from .gd_resource_utils import (folder, folder_contents, exportFile, getFile, folder_item, file_content_as, 
        gd_folder_files, gd_path_equivalent, gd_folder_files, gd_folder_item, uploadAsGoogleDoc, uploadFile, gd_mimetype_equivalent)

## Local Resource management

def get_working_dir():
    cwd = os.getcwd()
    if (cwd.find("home")>=0 and extend_path):  
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

def get_xml_dec(content):
    xml_dec_start = content.find("<?xml")
    if xml_dec_start>=0:
        return content[:content.find(">")+1]
    else:
        return content

def get_local_dir(local, config):
    cwd = get_working_dir()
    local_d = os.path.join(cwd, local_root, config.tenant, local)

#        local_d = "C:\\Users\\Andrew\\Documents\\GitHub\\"+install_name+"\\"+local_root+"\\"+local
    return local_d

def get_output_dir():
    return get_local_dir("output")

def get_local_txt_content(cwd, config, data_folder, data_file):
    try:
        full_file_path = os.path.join(get_local_dir(data_folder, config), data_file)
        with open(full_file_path, "r", encoding="UTF-8") as file:
            return  file.read()
    except FileNotFoundError:
        return None

def push_local_txt(cwd, config, data_folder, data_file, payload):
    full_file_path = os.path.join(get_local_dir(data_folder, config), data_file)
    return push_local_txt_fullname(full_file_path, payload)

def push_local_txt_fullname(full_file_path, payload):
#    full_file_path = data_file
    with open(full_file_path, "w", encoding="UTF-8") as file:
        file.write(payload)
        file.close()
    return full_file_path

def del_local(cwd, config, data_folder, data_file):
    full_file_path = os.path.join(get_local_dir(data_folder, config), data_file)
    os.remove(full_file_path)

def local_folder_files(config, path, parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents", days_ago=0, days_recent=100000):
    cwd = get_working_dir()
#    full_path = os.path.join(cwd, local_root, path)
    full_path = get_local_dir(path, config)
    files = os.listdir(full_path)
    
#    with open("debug.txt", "a") as f:
#        print(full_path, file=f)
#        print(files, file=f)
    now = time.time()
    response = []
    for file in files:
        full = os.path.join(full_path, file)
        timestamp = os.stat(full).st_mtime
        if timestamp < now - days_ago * 86400 and timestamp >= now - days_recent * 86400:
            ext = os.path.splitext(file)[-1].lower()
            response.append({
                "name":file, 
                "ext":ext, 
                "isdir": os.path.isdir(os.path.join(full_path, file)),
                "mtime": pytz.utc.localize(datetime.datetime.utcfromtimestamp(os.path.getmtime(os.path.join(full_path, file))))})
    return response


def handleRemoveReadonly(func, path, exc):
  print("handling error")  
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def process_local_files(config, subfolder, days_ago=7, days_recent=365, action="report", recursive=False, folders="all"):
    path = get_local_dir(subfolder, config)
    #path = os.path.join(get_working_dir(), local_root, subfolder)
    now = time.time()
    to_process = []
    for f in os.listdir(path):
        full = os.path.join(path, f)
        if (not(os.path.isdir(full))): # Not a directory
            try:
                if os.stat(full).st_mtime < now - days_ago * 86400 and os.stat(full).st_mtime >= now - days_recent * 86400:
                    if os.path.isfile(full):
                        to_process.append(f)
                        if action == "delete":
                            os.remove(full)
            except FileNotFoundError:
                pass # temp files can exist, don't count if file no longer there
        elif recursive:
            if folders=="all" or f in folders.split(","):
                to_process += process_local_files(config, os.path.join(subfolder,f), days_ago=days_ago, days_recent=days_recent, action=action, recursive=recursive, folders="all")
            # If folder is now empty                
                subpath = get_local_dir(os.path.join(subfolder,f), config)
                subpathcontent = os.listdir(subpath)
                print("Cleared",full)
                if len(subpathcontent)==0:
                    to_process.append(f)
                    if action == "delete":
                        print("Deleting",full)
                        os.rmdir(full)
    return to_process

def count_local_files(config, subfolder, days_ago=7, days_recent=365):
    files = process_local_files(config, subfolder, days_ago=days_ago, days_recent=days_recent, action="report")
    return(len(files))

def gd_populate_folders(config):
    folders = [
            "templates", 
            "templates/Sandbox", 
            "templates/Demo Examples", 
            "templates/Partials", 
            "transforms",
            "flows",
            "branding",
            "test_data",
            "output",
            ]
    for subfolder in folders:
        if subfolder != "output":
            path = gd_path_equivalent(config, subfolder) 
            fldr = folder(config, path, create_if_absent=True)      
            files = process_local_files(config, subfolder, days_ago=0, days_recent=365, action="report")
            for file in files:
                if file.find("_.docx")<0: #No preprocess files
                    filepath = os.path.join(get_local_dir(subfolder, config), file)
                    ## touch local files so they are not immediately stale
                    os.utime(filepath, None)
                    barename, ext = os.path.splitext(file)
                    if ext == ".docx": 
                        upload_name = barename
                    else:
                        upload_name = file
                    try:
                        exists = folder_item(config, fldr["id"], upload_name, mimeType="*")
                    except FileNotFoundError:
                        exists = False
                    if not exists:
                        if ext == ".docx": 
                            uploadAsGoogleDoc(config, filepath, fldr["id"], gd_mimetype_equivalent(ext), name=upload_name)
                        else:
                            uploadFile(config, filepath, fldr["id"], gd_mimetype_equivalent(ext), name=upload_name)


# Remote <-> Local methods


def is_text(ext):
    if ext in [".pdf", ".doc", ".docx", ".png", ""]:
        return False
    else:
        return True

def combined_folder_files(config, path, parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents, modifiedTime)"):
    local_files = local_folder_files(config, path, parent='root', mimeType='*', fields=fields)
    combined_files = {}
    response = []
    for file in local_files:
        file["is_local"]="Y"
        if is_text(file["ext"]):
            file["edit_local"]="Y"
        if remote_library:
            file["is_remote"]="N"
        else:
            file["is_remote"]="X"
        combined_files[file["name"]]=file
        file["location"]="On server only"
        file["status_symbol"]="<"
    if remote_library:
        if path[-1] == "/":
            path = path[:-1]
        remote_files = gd_folder_files(config, gd_path_equivalent(config, path), parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents, modifiedTime)")
        for file in remote_files:
            if file["name"] in combined_files.keys():
                combined_files[file["name"]]["mimeType"]=file["mimeType"]
                combined_files[file["name"]]["location"]="In library and on server - up-to-date"
                combined_files[file["name"]]["status_symbol"]="="
            elif file["name"]+".docx" in combined_files.keys():
                file["name"]=file["name"]+".docx"
                combined_files[file["name"]]["mimeType"]=file["mimeType"]
                combined_files[file["name"]]["location"]="In library and on server - up-to-date"
                combined_files[file["name"]]["status_symbol"]="="
            else:
                combined_files[file["name"]]=file
                combined_files[file["name"]]["is_local"]="N"
                combined_files[file["name"]]["location"]="In library only"
                combined_files[file["name"]]["status_symbol"]=">"
            combined_files[file["name"]]["is_remote"]="Y"
            combined_files[file["name"]]["id"]=file["id"]
            combined_files[file["name"]]["modifiedTime"]=iso8601.parse_date(file["modifiedTime"])
            combined_files[file["name"]]["isdir"]=file["mimeType"]=="application/vnd.google-apps.folder"
            combined_files[file["name"]]["ext"] = os.path.splitext(file["name"])[-1].lower()
            if "mtime" in combined_files[file["name"]].keys():
                if combined_files[file["name"]]["modifiedTime"] > combined_files[file["name"]]["mtime"]: #remote time > local time:
                    combined_files[file["name"]]["is_local"]="S"
                    combined_files[file["name"]]["location"]="In library and on server - but out-of-date on server"
                    if combined_files[file["name"]]["isdir"]:
                        combined_files[file["name"]]["status_symbol"]="="
                    else:
                        combined_files[file["name"]]["status_symbol"]=">"
    for file in combined_files.values():
        if file["name"].find("_.docx")<0: # No "hidden" files
            response.append(file)
    return response


def refresh_files(config, path, local_dir, recursive = False, clear = False, parent='root', mimeType='*', fields="nextPageToken, files(id, name, mimeType, parents)"):
    #print("refreshing:", path, local_dir)
    foldr = folder(config, path, parent)
    files = folder_contents(config, foldr["id"], mimeType=mimeType, fields=fields)
    files_info=[]
    
    if clear: #delete local files
        process_local_files(config, local_dir, days_ago=0, days_recent=9999999, action="delete", recursive=True)

    for file in files:
        doc_id =file["id"]
        cwd = get_working_dir()
        localFileName = os.path.join(get_local_dir(local_dir, config), file["name"]).replace("\\", "/").replace("/./", "/")
#        localFileName = os.path.join(cwd, local_root, local_dir, file["name"])
        if file["mimeType"] == 'application/vnd.google-apps.folder':
            # create local 
            if not os.path.exists(localFileName):
                os.makedirs(localFileName) #actually a directory
            #print("subfolder")
            #print("remote", "/".join([path,file["name"]]))
            #print("local", localFileName)
            files_info.append({"folder": localFileName})
            if recursive:
                deep_files = refresh_files(config, "/".join([path,file["name"]]), localFileName, recursive=recursive, clear=clear)
                files_info = files_info+deep_files
        elif file["mimeType"] == 'application/vnd.google-apps.document':
            if localFileName.find(".") < 0: # no extension
                files_info.append(exportFile(config, doc_id, localFileName+".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
            elif localFileName.find(".docx") >= 0: # extension docx
                files_info.append(exportFile(config, doc_id, localFileName, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
            else:
                files_info.append(exportFile(config, doc_id, localFileName, "text/plain"))
        elif file["mimeType"] == 'application/vnd.google-apps.spreadsheet':
            if localFileName.find(".") < 0: # no extension
                files_info.append(exportFile(config, doc_id, localFileName+".docx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
            elif localFileName.find(".csv") >= 0: # extension csv
                files_info.append(exportFile(config, doc_id, localFileName, "text/csv"))
        else:
            files_info.append(getFile(config, doc_id, localFileName, file["mimeType"]))
    return files_info


    
def folder_file(config, path, name, parent='root', mimeType='*'):
    foldr = folder(config, path, parent)
    return folder_item(config, foldr["id"], name, mimeType=mimeType)

def get_remote_txt_content(config, data_folder, data_file):
    data_doc_id = folder_file(config, data_folder, data_file)["id"]
    doc_txt = file_content_as(config, data_doc_id)
    return doc_txt

def get_txt_content(config, local_data_folder, remote_data_folder, data_file):
    content = get_local_txt_content(get_working_dir(), config, local_data_folder, data_file)
    if content == None:
        if remote_library:
            content = get_remote_txt_content(config, remote_data_folder, data_file)
        else:
            raise FileNotFoundError("'"+data_file+"' was not found locally. No remote library")
    return content

def get_xml_content(config, local_data_folder, remote_data_folder, data_file):
    content = get_txt_content(config, local_data_folder, remote_data_folder, data_file)
    if type(content) is bytes:
        content = content.decode("UTF-8")
    return strip_xml_dec(content)

def get_json_content(config, local_data_folder, remote_data_folder, data_file):
    content = get_txt_content(config, local_data_folder, remote_data_folder, data_file)
    if type(content) is bytes:
        content = content.decode("UTF-8")
    return content

def zip_local_dirs(path, zip_file_name, selected_subdirs = ["templates", "flows", "transforms", "test_data", "branding"]):
    zip_name = os.path.join(path,zip_file_name+".zip")
    ziph = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    excludepattern = "_.docx" # exclude preprocessed docx
    for root, dirs, files in os.walk(path):
        for file in files:
            if not(file.find(excludepattern)>0):
                relpath = os.path.relpath(os.path.join(root, file), os.path.join(path, '..'))
                if selected_subdirs == None or relpath.split(os.path.sep)[1] in selected_subdirs:
                    ziph.write(os.path.join(root, file), relpath)
            else:
                print("skipping file", file)
    ziph.close()
    return zip_name

def remote_link(config, filename, subfolder):
    filepath = get_local_dir(subfolder, config)
    remote = gd_path_equivalent(config, subfolder)
    remote_folder = folder(config, remote)
    file_details = gd_folder_item(config, remote, filename)
    "https://docs.google.com/document/d/1S8gJeCD_vDjbM2JKk8Ojkt-6Uj_fdn_NQPdzHeQnn0Y/edit?usp=sharing"
#    return "https://drive.google.com/open?id={}".format(file_details["id"])
    return "https://drive.google.com/file/d/{}/view?usp=sharing".format(file_details["id"])
#    return "https://docs.google.com/document/d/{}/edit?usp=sharing".format(file_details["id"])


def get_folders_and_files(template_subfolder, items):
        files = []
        folders = []
        if template_subfolder:
            parent = template_subfolder[:template_subfolder.rfind("/")+1]
            if not(parent =="/"):
                    folders.append({"name":parent, "ext":".."})
            folders.append({"name":template_subfolder, "ext":"."})
#        else:
#            folders.append({"name":"/", "ext":"."})
        for item in items:
            if item["isdir"]:
                item["name"]=(template_subfolder+"/"+item["name"]).replace("//","/")
                folders.append(item)
            else:
                files.append(item)
        folders = sorted(folders, key=lambda k: k['ext']+k['name']) 
        folders=[{"name":"/", "ext":"/"}]+folders
        files = sorted(files, key=lambda k: k['ext']+k['name']) 
        return folders, files

def clean_subfolder(subfolder):
    if len(subfolder)>0 and subfolder[-1] =="/":
        subfolder=subfolder[:-1]
    elif subfolder != "" and subfolder.find("/")!=0:
        subfolder = "/"+subfolder
    return subfolder

