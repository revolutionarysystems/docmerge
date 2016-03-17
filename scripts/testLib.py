from merge.merge_utils import folder_files

def run():
    files = folder_files("/Doc Merge/Templates",fields="files(id, name, mimeType, trashed)")
    for file in files:
        print(file["name"])
        print(file["id"])
        print(file)
