from power_of_10 import search_athletes
from power_of_10 import get_athlete
import json
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
from flask import Flask
from flask import render_template
app = Flask(__name__)

athleteId = search_athletes(firstname="jake", surname="bowles")
atheleteDetails = get_athlete(athleteId[0]["athlete_id"])

pbs = []

for x in atheleteDetails["pb"]:
    pbs.append(x)

performances = []

for x in atheleteDetails["performances"]:
    performances.append(x)

performances_json = json.dumps(performances)
pbs_json = json.dumps(pbs)

if not os.path.exists('/tmp/out/'):
    os.makedirs('/tmp/out/')

file = open("/tmp/out/performances.json","w")
file.write(performances_json)

file = open("/tmp/out/pbs.json","w")
file.write(pbs_json)

MY_CONNECTION_STRING = "BlobEndpoint=https://jbconttest.blob.core.windows.net/;QueueEndpoint=https://jbconttest.queue.core.windows.net/;FileEndpoint=https://jbconttest.file.core.windows.net/;TableEndpoint=https://jbconttest.table.core.windows.net/;SharedAccessSignature=sv=2020-08-04&ss=bfqt&srt=co&sp=rwdlacupitfx&se=2022-02-23T01:28:40Z&st=2022-02-22T17:28:40Z&spr=https&sig=t4y5sYntDjayfb4NQ4B5rz%2FtW5TWEmCMPpVoYb4M1i8%3D"
MY_CONTAINER = "container"
LOCAL_PATH = "/tmp/out"

class AzureBlobFileUploader:
  def __init__(self):
    print("Intializing AzureBlobFileUploader")
 
    # Initialize the connection to Azure storage account
    self.blob_service_client =  BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)
 
  def upload_all_images_in_folder(self):
    # Get all files with jpg extension and exclude directories
    all_file_names = [f for f in os.listdir(LOCAL_PATH)
                    if os.path.isfile(os.path.join(LOCAL_PATH, f)) and ".json" in f]
 
    # Upload each file
    for file_name in all_file_names:
      self.upload_image(file_name)
 
  def upload_image(self,file_name):
    # Create blob with same name as local file name
    blob_client = self.blob_service_client.get_blob_client(container=MY_CONTAINER,
                                                          blob=file_name)
    # Get full path to the file
    upload_file_path = os.path.join(LOCAL_PATH, file_name)
 
    # Create blob on storage
    # Overwrite if it already exists!
    print(f"uploading file - {file_name}")
    with open(upload_file_path, "rb") as data:
      blob_client.upload_blob(data,overwrite=True)
 
 

#print("Hello World!")

@app.route('/')
@app.route('/index')
def hello_world():
  # Initialize class and upload files
    azure_blob_file_uploader = AzureBlobFileUploader()
    azure_blob_file_uploader.upload_all_images_in_folder()
    return render_template('index.html', title='Welcome', username='jake')