from merge.merge_utils import folder_files, refresh_files, get_working_dir
from merge.flow import get_flow_local, get_flow

def run1():
    files = folder_files("/Doc Merge/Flows",fields="files(id, name, mimeType, trashed)")
    for file in files:
        print(file["name"])
        print(file["id"])
        print(file)

def run2():
    files = refresh_files("/Doc Merge/Flows", "flows")
    #files = refresh_files("/Doc Merge/Flows", "flows/")
    for file in files:
        print(file)

def run():
    run2()
    cwd = get_working_dir()
    print(cwd)
    flow = get_flow(cwd, "flows/", "/Doc Merge/Flows", "docx2.txt")
    print(flow)

