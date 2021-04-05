import httplib2
import os
from apiclient import discovery
#from apiclient.http import MediaFileUpload
import oauth2client
from oauth2client import tools
from oauth2client import file
from oauth2client import client,clientsecrets
from apiclient.errors import HttpError
from .config import install_name, extend_path, remote_library
from time import sleep
import argparse
from docmerge.settings import MULTI_TENANTED

services = {}

class GDriveAccessException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

flags = tools.argparser.parse_args(args=[])

def get_credentials_ask(redirect):
    secrets = get_secrets()
    flow = client.OAuth2WebServerFlow(
#                            client_id="398120274769-frpov8mpo1a417a7k41rjapiaekr7fc5.apps.googleusercontent.com",  
#                            client_secret="Ht9esrVMvAqYWPygR0u0zXct",
                           client_id=secrets["client_id"],  
                           client_secret=secrets["client_secret"],
                           scope='https://www.googleapis.com/auth/drive',
                           prompt = 'consent',
                           redirect_uri=redirect)
    auth_uri = flow.step1_get_authorize_url()
    return auth_uri

def get_credential_dir(config):
    home_dir = os.path.expanduser('~')
    if MULTI_TENANTED:
        return os.path.join(home_dir, '.credentials', install_name, config.tenant)
    else:
        return os.path.join(home_dir, '.credentials', install_name)


def get_credentials_store(config, code, redirect):
    secrets = get_secrets()
    flow = client.OAuth2WebServerFlow(
#                            client_id="398120274769-frpov8mpo1a417a7k41rjapiaekr7fc5.apps.googleusercontent.com",  
#                            client_secret="Ht9esrVMvAqYWPygR0u0zXct",
                           client_id=secrets["client_id"],  
                           client_secret=secrets["client_secret"],
                           scope='https://www.googleapis.com/auth/drive',
                           redirect_uri=redirect)
    credentials = flow.step2_exchange(code)
    credential_dir = get_credential_dir(config)
#    home_dir = os.path.expanduser('~')
#    credential_dir = os.path.join(home_dir, '.credentials', install_name)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'drive-echopublish.json')
    print("Looking for credentials at:",credential_path)

    store = oauth2client.file.Storage(credential_path)
    store.put(credentials)

def get_secrets():
    client_type, client_info = clientsecrets.loadfile(CLIENT_SECRET_FILE)
    return client_info


def old_get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
#    home_dir = os.path.expanduser('~')
#    credential_dir = os.path.join(home_dir, '.credentials', install_name)
    credential_dir = get_credential_dir(config)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'drive-echopublish.json')
    print("Looking for credentials at:",credential_path)

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
#        except Exception as e:
#            print("No credentials at:", credential_path)
    return credentials

def get_credentials(config):
    global http
#    home_dir = os.path.expanduser('~')
#    credential_dir = os.path.join(home_dir, '.credentials', install_name, config.tenant)
    credential_dir = get_credential_dir(config)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'drive-echopublish.json')
    print("Looking for credentials at:",credential_path)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials:
        return None
    if credentials.invalid:
        print("+++> credentials invalid")
        return None
    return credentials


def get_service(config):
    if not remote_library:
        raise GDriveAccessException("This installation does not access Google Drive")
    global services
    try:
        service = services[config.tenant]
        if service == None:
            raise GDriveAccessException("Google Drive service is not yet initialised for", config.tenant)
        return service # service is not missing or None
    except NameError:
        raise GDriveAccessException("Google Drive service is not yet initialised", config.tenant)
    except KeyError:
        raise GDriveAccessException("Google Drive service is not yet initialised", config.tenant)


def protected_execute(config, query, max_tries=4, wait_time=0.2):
    results = []
    for i in range(max_tries):
        try:
            results = get_service(config).files().list(fields="nextPageToken, files(id, name, mimeType, parents)", q=query).execute()
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


def initialiseService(config):
    global http
    print("initialising Drive service")
    credentials = get_credentials(config)
    if credentials:
        print("credentials found")
        http = credentials.authorize(httplib2.Http())
        if credentials.invalid:
            credentials.refresh(http)
        service = discovery.build('drive', 'v3', http=http)
        return service
    else:
        return None


SCOPES = 'https://www.googleapis.com/auth/drive'
if (os.getcwd().find("scripts")>=0):  #from test script
    CLIENT_SECRET_FILE = '../client_secret.json'
else:
    CLIENT_SECRET_FILE = 'client_secret.json'
if (os.getcwd().find("home")>=0):  #pythonanywhere deployment
#    CLIENT_SECRET_FILE = '/home/docmerge/'+install_name+'/client_secret.json'
    if extend_path:
        CLIENT_SECRET_FILE = os.path.join(os.getcwd(),install_name,'client_secret.json')
    else:
        CLIENT_SECRET_FILE = os.path.join(os.getcwd(),'client_secret.json')
print("Looking for client secret at:",CLIENT_SECRET_FILE)
APPLICATION_NAME = 'Echo Publish'

def initialise(config):
    global services, http
    service = initialiseService(config)
    services[config.tenant]=service
    http = None

def ensure_initialised(config):
    try: 
        if services[config.tenant]==None:
            service = initialiseService(config)
            services[config.tenant]=service
            return service
        else:
            return services[config.tenant]
    except:
        service = initialiseService(config)
        services[config.tenant]=service
        return service

