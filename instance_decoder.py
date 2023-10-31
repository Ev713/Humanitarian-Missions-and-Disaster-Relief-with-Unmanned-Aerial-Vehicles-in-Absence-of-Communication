import os

import StringInstanceManager

instances = []
for filename in os.scandir("DragonAge_encoded_instances"):
    if filename.is_file():
        decoded_instance = StringInstanceManager.to_inst(filename)
        instances.append(decoded_instance)
print(len(instances))
