

#############################################################################
# This class provides message handling for read and writing JSON messages
# This class interfaces with google cloud for audio data
# This class interfaces with mqtt for message passing
#############################################################################

import paho.mqtt.client as paho
import base64
import json
from google.cloud import storage
import os
        
class CommsManager():
    
    def __init__(self) -> None:
        pass
    
    def initialise_communications(self):
        pass
    
    # This function uses the google bucket with audio files and
    # leverages the folder names as the official species names
    # Note: to run this you will need to first authenticate
    # See https://github.com/DataBytes-Organisation/Project-Echo/tree/main/src/Prototypes/data#readme
    def gcp_load_species_list(self):
 
        species_list = set()
 
        bucket_name = 'project_echo_bucket_3'
        os.environ["GCLOUD_PROJECT"] = "sit-23t1-project-echo-25288b9"

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()  # Get list of files
        for blob in blobs:
            folder_name = blob.name.split('/')[0]
       
            species_list.add(folder_name)
            #file_name = blob.name.split('/')[1]
            #path = os.path.join(dl_dir, folder_name)
            #if not os.path.exists(path):
            #    os.makedirs(path)
            #blob.download_to_filename(os.path.join(dl_dir, folder_name, file_name))
        return species_list
 
    def mqtt_send_audio_msg(self) -> None:
        def on_publish(client, userdata, mid):
            print("mid: "+str(mid))
        
        client = paho.Client()
        client.on_publish = on_publish
        client.connect('broker.mqttdashboard.com', 1883)
        client.loop_start()

        i = 0
        while True:
            MQTT_MSG = json.dumps(data[i])

            (rc, mid) = client.publish('projectecho/1', MQTT_MSG, qos=1)
            print(MQTT_MSG)
            time.sleep(5)
            i += 1
 
    # this method takes in binary audio data and encodes to string
    def string_to_audio(self, audio_string) -> bytes:
        base64_img_bytes = audio_string.encode('utf-8')
        decoded_data = base64.decodebytes(base64_img_bytes)
        return decoded_data
        
    # this method takes in binary audio data and encodes to string
    def audio_to_string(self, audio_binary) -> str:
        base64_encoded_data = base64.b64encode(audio_binary)
        base64_message = base64_encoded_data.decode('utf-8')
        return base64_message
    
    def test(self):
        print(f'testing MessageManager')
        
        print(f'Testing GCP endpoint')
        
        species_list = self.gcp_load_species_list()
        for species in species_list:
            print(f'Found species name: {species}')
        
        # load a test json file containing audio data
        with open('src\Prototypes\data\database\sample_data\events.json', 'r') as file:
            test_json = json.load(file)
            msg = test_json[0]
            print(f' Loaded message timestamp: {msg["timestamp"]}')
            
            audio_b1 = self.string_to_audio(msg['audioClip'])
            audio_s1 = self.audio_to_string(audio_b1)
            
            audio_b2 = self.string_to_audio(audio_s1)
            audio_s2 = self.audio_to_string(audio_b2)
            
            audio_b3 = self.string_to_audio(audio_s2)
            audio_s3 = self.audio_to_string(audio_b3)
            
            assert audio_s3 == audio_s1, "Strings are not matching!"
            
            print(f'test completed successfully')
    
        