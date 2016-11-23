import os
import sys
import traceback
import platform, os
from jinja2 import Environment


# if we're OSX look for the homebrew qemu ENV variable
if platform.system() == 'Darwin':
    try:
        os.environ["QEMUPATH"]
        qemu_img_command = os.path.join(os.environ["QEMUPATH"], "qemu-img")
        print qemu_img_command
    except KeyError:
        print "Please set the environment variable QEMUPATH to point to OSX qemu executable"
        sys.exit(1)


# silly wrapper
def check_path(path):
    if os.path.exists(path):
        return True
    else:
        return False

def create_file_structure(files, os_type=None, volume_name='CLOUD-BOOT'):
    mount_point = None

    if os_type == 'Darwin':
        mount_point = "/Volumes/{}".format(volume_name)
    else:
        mount_point = '/mnt'

    for name in files:
        if '/' in name:
            # we need to create a directory structure here!
            directory = os.path.dirname(name)

            print "mkdir -p {0}{1}".format(mount_point, directory)
            if not os.system("mkdir -p {0}{1}".format(mount_point, directory)) == 0:
                raise Exception("Could not create confg-drive directory structure")
        else:
            # ensure a leading / just in case!
            name = "/" + name

        print "writing file: %s" % name
        with open("{0}{1}".format(mount_point, name), "w") as mdf:
            mdf.write(files[name])

    os.system("cd {0} && tar --exclude='.tar' -cvf vmm-config.tar .".format(mount_point))


def create_cloud_drive(configuration, files=[]):
    volume_name = None
    seed_image_name = None

    try:
        print "Creating cloud drive image"

        seed_dir = configuration["seeds_dir"] + configuration["name"]

        if platform.system() == 'Darwin':
            # hdiutil will append .dmg to the image name
            seed_img_name = seed_dir + "/config-drive.dmg"
            volume_name = 'CLOUD-BOOT'

            if not check_path(seed_dir):
                os.mkdir(seed_dir)

            if check_path(seed_img_name):
                print "seed.img already created!"
                return seed_img_name

            print seed_img_name
            print volume_name

            # OSX specific. Create image and format in one step
            if not os.system("hdiutil create -nospotlight -megabytes 16 -fs MS-DOS \
                              -volname {0} -o {1}".format(volume_name, seed_img_name)) == 0:
                raise Exception("Could not create config-drive image")

            # OSX specific. Will mount to /Volumes by default
            if not os.system("hdiutil attach %s" % seed_img_name) == 0:
                raise Exception("Could not mount config-drive filesystem")

            create_file_structure(files, os_type=platform.system())

        else:
            # assume linux for now
            seed_img_name = seed_dir + "/config-drive.img"

            if not check_path(seed_dir):
                os.mkdir(seed_dir)

            if check_path(seed_img_name):
                print "seed.img already created!"
                return seed_img_name

            if not os.system(qemu_img_command + " create -f raw  %s 16M" % seed_img_name) == 0:
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
        if platform.system() == 'Darwin':
            os.system("hdiutil detach /Volumes/%s" % volume_name)
        else:
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

        template_data_string = template_data.render(config=configuration)
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
