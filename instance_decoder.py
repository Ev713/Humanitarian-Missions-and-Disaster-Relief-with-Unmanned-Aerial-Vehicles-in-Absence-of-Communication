import os

import StringInstanceManager

instances = []
for type in ['FR', 'MT']:
    for filename in os.scandir("DragonAge_encoded_instances/"+type):
        if filename.is_file():
            decoded_instance = StringInstanceManager.to_inst(filename)
            #if len(decoded_instance.map) <= 30:
            instances.append(decoded_instance)
for type in ['FR', 'MT', 'SC', 'AG']:
    for filename in os.scandir("Generated_encoded_instances/"+type):
        if filename.is_file():
            decoded_instance = StringInstanceManager.to_inst(filename)
            # if len(decoded_instance.map) <= 30:
            instances.append(decoded_instance)
print(len(instances))
