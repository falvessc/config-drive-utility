import os
from jinja2 import Environment
import sys, traceback


# silly wrapper
def check_path(path):
    if os.path.exists(path):
        return True
    else:
        return False


def create_cloud_drive(configuration, files=[]):
    try:
        print "Creating cloud drive image"

        seed_dir = configuration["seeds_dir"] + configuration["name"]
        seed_img_name = seed_dir + "/config-drive.img"

        if not check_path(seed_dir):
            os.mkdir(seed_dir)

        if check_path(seed_img_name):
            print "seed.img already created!"
            return seed_img_name

        if not os.system("qemu-img create -f raw  %s 16M" % seed_img_name) == 0:
            raise Exception("Could not create config-drive image")

        if not os.system("mkdosfs %s" % seed_img_name) == 0:
            raise Exception("Could not create config-drive filesystem")

        if not os.system("mount %s /mnt" % seed_img_name) == 0:
            raise Exception("Could not mount config-drive filesystem")

        for name in files:

            if '/' in name:
                # we need to create a directory structure here!
                directory = os.path.dirname(name)
                if not os.system("mkdir -p /mnt%s" % directory) == 0:
                    raise Exception("Could not create confg-drive directory structure")
            else:
                # ensure a leading / just in case!
                name = "/" + name

            print "writing file: %s" % name
            with open("/mnt%s" % name, "w") as mdf:
                mdf.write(files[name])

        os.system("cd /mnt && tar -cvf vmm-config.tar .")

        return seed_img_name

    except Exception as e:
        print "Could not create_cloud_drive!!!"
        print str(e)
        traceback.print_exc(file=sys.stdout)
        return None

    finally:
        os.system("umount /mnt")


def get_junos_default_config_template(configuration):
    try:
        # read template
        this_path = os.path.abspath(os.path.dirname(__file__))
        template_path = os.path.abspath(os.path.join(this_path, "junos_config.j2"))

        template = open(template_path)
        template_string = template.read()
        template.close()

        env = Environment()
        template_data = env.from_string(template_string)

        config = dict()

        config["host_name"] = configuration["name"]
        config["mgmt_ip"] = configuration["management_ip"]
        config["mgmt_gateway"] = configuration["management_gateway"]
        config["ssh_key"] = configuration["ssh_key"]
        config["ssh_user"] = configuration["ssh_user"]
        config["password"] = configuration["root_password"]

        template_data_string = template_data.render(config=config)
        print template_data_string

        if not configuration["seeds_dir"].endswith('/'):
            configuration["seeds_dir"] += "/"

        seed_dir = configuration["seeds_dir"] + configuration["name"]

        if not check_path(seed_dir):
            os.mkdir(seed_dir)

        return template_data_string

    except Exception as e:
        print "Caught exception in get_junos_default_config_template " + str(e)
        return None


