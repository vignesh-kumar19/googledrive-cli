#! /usr/bin/env python
from sys import exit, version_info, argv
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   ITALIC = '\033[3m'

# Checking version is 3
if not version_info.major == 3:
    print("{}Script needs python 3{}".format(color.RED, color.END))
    exit(1)

# credentials file path
filepath = '/home/'+os.environ.get("USER")+'/.googledriver-api/'

# Check credentials path exists
if not os.path.exists(filepath):
    os.makedirs(filepath)

# Set secret file and credentials file name
secretfilename = filepath + 'client_secret.json'
credentialsfilename = filepath + 'credentials.json'
scriptname = 'drivecli'

# importing required packages
from apiclient.discovery import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
from prettytable import PrettyTable
from optparse import OptionParser

from googledrivecli.googleoauth import GetAPIResourceObj

# Create credentials file
def generateCredentials():
    secretNotFound = True
    first_time = True
    while(secretNotFound):
        if os.path.isfile(secretfilename):
            print("{}client_secret.json is found !{}\n".format(color.GREEN, color.END))
            secretNotFound = False
        else:
            if first_time:
                print("""{}\n'client_secret.json' file not found !
Follow the steps in 'Step 1: Turn on the Drive API' : https://developers.google.com/drive/api/v3/quickstart/python{}
        """.format(color.BOLD, color.END))
                input("Click 'ENTER' once you download 'credentials.json' and save into '{}' directory\n".format(filepath))
                first_time = False
            else:
                input("'client_secret.json' file not found!, click enter once downloaded")


    if os.path.isfile(credentialsfilename):
        print("{}Credentials file is already available{}\n".format(color.GREEN, color.END))
        print("To upload, download, search file in Drive run '{} --help'".format(scriptname))
        exit(0)

    GetAPIResourceObj()
    exit(0)

# List File from drive
def listFile(**keyargs):
    page_token = None
    table = PrettyTable(["modifiedTime", "size", "name", "mimeType"])
    while True:
        service = GetAPIResourceObj()

        if keyargs.get('all'):
            search_response = service.files().list(fields="nextPageToken, files(size, modifiedTime, name, mimeType)", pageToken=page_token).execute()
        if keyargs.get('allimages'):
            search_response = service.files().list(pageSize=500, fields="nextPageToken, files(size, modifiedTime, name, mimeType)", pageToken=page_token, q="mimeType='image/jpeg'").execute()
        if keyargs.get('searchfile'):
            query="name contains '{}'".format(keyargs.get('searchfile'))
            search_response = service.files().list(fields="nextPageToken, files(size, modifiedTime, name, mimeType)", pageToken=page_token, q=query).execute()
        for file in search_response.get('files', []):
            # Process change
            table.add_row([file['modifiedTime'], file.get('size'), file['name'], file.get('mimeType')])

        if table.__dict__.get('_rows'):
            print (table)
        else:
            print("No files are found")

        # if not keyargs.get('searchfile'):
        #     input("Press ENTER to load next 500 files")
        page_token = search_response.get('nextPageToken', None)
        if page_token is None:
            break
        input("Press ENTER to load next 500 files")

# Upload File to drive
def uploadFile(filepath, filetype):
    if filetype == 'csv':
        filetype = 'text/csv'
    if filetype == 'image':
        filetype = 'image/jpeg'
    if filetype == 'pdf':
        filetype = 'application/pdf'
    if filetype == 'folder':
        filetype = 'application/vnd.google-apps.folder'
    if filetype == 'documents':
        filetype == 'application/vnd.google-apps.document'
    if filetype == 'iso':
        filetype = 'application/x-iso9660-image'
    if filetype == 'compressed':
        filetype = 'application/x-gzip'
    if filetype == 'plain':
        filetype = 'text/plain'

    file_metadata = {'name': filepath.split("/")[-1]}
    media  = MediaFileUpload(filepath, mimetype=filetype, resumable=True)
    file_response = GetAPIResourceObj().files().create(body=file_metadata, media_body=media,
                                fields='id').execute()
    if file_response:
        print("Upload Complete!")

# Download File from drive
def downFile(**keyargs):
    #file_id = input("Enter file ID: ").strip()
    if keyargs.get('exactfilename'):
        query="name = '{}'".format(keyargs.get('exactfilename'))
    if keyargs.get('filenamecontains'):
        query="name contains '{}'".format(keyargs.get('filenamecontains'))
    search_response = GetAPIResourceObj().files().list(fields="nextPageToken, files(id, name)", q=query).execute()
    for file in search_response.get('files', []):
        request = GetAPIResourceObj().files().get_media(fileId=file.get('id'))
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        print("Downloading {}".format(file.get('name')))
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print("Download %d%%." % int(status.progress() * 100))
        path=keyargs.get('localpath') + '/' + file.get('name')
        with open(path, "wb") as fw:
            fh.seek(0)
            fw.write(fh.read())
        fh.close()


#if __name__ == "__main__":
def main():

    usage = "%prog (To generate credentials file, which allows to connect to google drive)\n \
 or : %prog search-file --searchfile=filename | --all-images |  --all  (To Search file(s) in drive)\n \
 or : %prog upload-file --filepath=filepath --filetype=filetype (To upload a file in drive)\n \
 or : %prog download-file --exactfilename=exactfilename | --filenamecontains=filenamecontains --localpath=path (To download a file in drive)\n \
 or : %prog --help (For help)"

    parser = OptionParser(usage=usage)
    parser.add_option("--searchfile", dest="searchfile", help="filename to search")
    parser.add_option("--exactfilename", dest="exactfilename", help="filename to download")
    parser.add_option("--filenamecontains", dest="filenamecontains", help="download files matches a string")
    parser.add_option("--localpath", dest="localpath", help="local path to save file")
    parser.add_option("--filepath", dest="filepath", help="filename with path, to upload a file")
    parser.add_option("--all", action="store_true", dest="all", default=False, help="list all files")
    parser.add_option("--all-images", action="store_true", dest="allimages", default=False, help="list all images")
    parser.add_option("--filetype", dest="filetype", help="valid file types are csv, image, pdf, plain, compressed, iso")
    (options, args) = parser.parse_args()
    #print(options)


    if len(args) == 0:
        generateCredentials()
        exit(0)
    if  args[0] not in ['search-file', 'upload-file', 'download-file']:
        print("Unknown argument: {}{}{}".format(color.BOLD, args[0], color.END))
        print("\n"+parser.get_usage())
        exit(1)

    # Checking credentials file is exist
    if not os.path.isfile(credentialsfilename):
        print("{}{} file not found {}".format(color.RED, credentialsfilename, color.END))
        print("Run '{}' to generate ".format(scriptname))
        exit(1)

    # Search-file checks
    if  args[0] == 'search-file':
        search_options = { 'searchfile':options.searchfile, 'allimages':options.allimages,
                            'all':options.all }
        search_option = { k: v for k, v in search_options.items()  if v }
        if  len(search_option) == 1:
            listFile(**search_option)
        elif len(search_option) < 1:
            print("{}Required argument is missing!{}".format(color.RED, color.END))
            print("\n"+parser.get_usage())
            exit(1)
        else:
            print("Only one option should be passed")
            print("\n"+parser.get_usage())
            exit(1)

    # Upload-file checks
    elif args[0] == 'upload-file':
        if not options.filepath or  not options.filetype:
            print("{}Required argument is missing!{}".format(color.RED, color.END))
            print("\n"+parser.get_usage())
            exit(1)
        if options.filetype not in [ 'csv', 'image', 'pdf', 'plain', 'compressed', 'iso' ]:
            print("Unknown file type.")
            print("\n"+parser.get_usage())
            exit(1)
        upload_option = { 'filepath':options.filepath, 'filetype':options.filetype }
        uploadFile(upload_option['filepath'], upload_option['filetype'])

    # Download file checks
    elif args[0] == 'download-file':
        if options.filenamecontains and options.exactfilename:
            print("Either give '--filenamecontains' or '--exactfilename' ")
            exit(1)
        if not (options.filenamecontains or options.exactfilename) and options.localpath:
            print("Required parameters is not given")
            print("\n"+parser.get_usage())
            exit(1)
        download_option = { 'filenamecontains':options.filenamecontains, 'exactfilename':options.exactfilename, 'localpath': options.localpath}
        download_option = { k: v for k, v in download_option.items()  if v }

        if len(download_option) == 2:
            downFile(**download_option)

        elif len(download_option) < 2:
            print("{}Required argument is missing!{}".format(color.RED, color.END))
            print("\n"+parser.get_usage())
            exit(1)
        else:
            print("\n"+parser.get_usage())
            exit(1)

    else:
        print("\n"+parser.get_usage())
