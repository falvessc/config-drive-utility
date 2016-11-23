#!/usr/bin/env python

import builder_utils
import yaml

with open('device_params.yaml', 'r') as f:
    configuration = yaml.load(f)

    print configuration
    files = dict()

    junos_config = builder_utils.get_junos_default_config_template(configuration)
    if junos_config is not None:
        files["/juniper.conf"] = junos_config

    disk_instance_path = builder_utils.create_cloud_drive(configuration, files)
    if disk_instance_path is not None:
        print "Created %s successfully. Attach this image as a USB disk before power up" % disk_instance_path
