import os

import InstanceManager


class Decoder:
    def __init__(self):
        self.instances = []

    def decode(self, small_only=False, mid_only=False, save=False):
        for type in []:
            for filename in os.scandir("DragonAge_encoded_instances/" + type):
                if filename.is_file():
                    decoded_instance = InstanceManager.to_inst(filename)
                    if len(decoded_instance.map) > 30 and small_only:
                        continue
                    if len(decoded_instance.map) < 30 or len(decoded_instance.map) > 100 and mid_only:
                        continue
                    self.instances.append(decoded_instance)
        for type in ['MT']:
            for filename in os.scandir("Generated_encoded_instances/" + type):
                if filename.is_file():
                    decoded_instance = InstanceManager.to_inst(filename)
                    if len(decoded_instance.map) > 30 and small_only:
                        continue
                    if len(decoded_instance.map) < 30 or len(decoded_instance.map) > 100 and mid_only:
                        continue
                    self.instances.append(decoded_instance)

        if save:
            for instance in self.instances:
                InstanceManager.filter_unconnected(instance)
                InstanceManager.map_reduce(instance)
            for instance in self.instances:
                InstanceManager.to_string(instance, "Reduced_maps")

    def decode_reduced(self, size_lower_bound=None, size_higher_bound = None, horizon_higher_bound = None,
                       types_allowed=('FR', 'MT', 'SC', 'AG001', 'AG05', 'AG01')):
        for filename in os.scandir("Reduced_maps"):
            if filename.is_file():
                decoded_instance = InstanceManager.to_inst(filename)
                if size_lower_bound is not None and len(decoded_instance.map) > size_lower_bound:
                    continue
                if size_higher_bound is not None and len(decoded_instance.map) < size_higher_bound:
                    continue
                if decoded_instance.type not in types_allowed:
                    continue
                if horizon_higher_bound is not None and horizon_higher_bound > decoded_instance.horizon:
                    continue
                self.instances.append(decoded_instance)
        return self.instances

