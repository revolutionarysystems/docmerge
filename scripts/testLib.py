from merge.models import ClientConfig
from merge.resource_utils import refresh_files,process_local_files
from merge.gd_service import ensure_initialised
#from merge.flow import get_flow_local, get_flow
#from merge.xml4doc import getData
"""
def run1():
    files = folder_files("/Doc Merge/Flows",fields="files(id, name, mimeType, trashed)")
    for file in files:
        print(file["name"])
        print(file["id"])
        print(file)
"""
def run2():
    config = ClientConfig()
    config.tenant="ECV"
    ensure_initialised(config)

    files = refresh_files(config, "/Echo Publish Demo/Flows", "flows")
    #files = refresh_files("/Doc Merge/Flows", "flows/")
    for file in files:
        print(file)
"""
def run3():
    run2()
    cwd = get_working_dir()
    print(cwd)
    flow = get_flow(cwd, "flows/", "/Doc Merge/Flows", "docx2.txt")
    print(flow)


def run4():
    #content = get_xml_content("branding", "/Doc Merge/Branding", "superll.xml")
    content = getData(local_data_folder="branding", remote_data_folder = "/Doc Merge/Branding", data_file="superll.xml")
    print(content)
    
def run5():
    cwd = get_working_dir()
    file_name = push_local_txt(cwd, "branding", "text.xml", "<brand/>")
    print(file_name)

def run6():
    fldr = folder("/Doc Merge/Branding", create_if_absent = False)
    print(fldr)
#    files = folder_files("/Doc Merge/Dummy",fields="files(id, name, mimeType, trashed)", mimeType='application/vnd.google-apps.folder')
#    target = "Output"    
#    for file in files:
#        if file["name"] == target:
#            print(file) 
#    print("done")
#def folder_item(parent, name, mimeType='application/vnd.google-apps.folder', ):

"""    
def run():
    config = ClientConfig()
    files = process_local_files(config, "templates", days_ago=0, days_recent=999, action="report", recursive=True)
    print(files)
