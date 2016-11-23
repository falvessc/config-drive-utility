Create Cloud Drive Utility

This is a simple utility to create a cloud-config drive for junos devices.

Junos requires a USB disk be formatted with msdos that contains a default configuration.
This simply creates a templatized Junos configuration based on some entries in the
device_parms.yaml file and creates the image.

For KVM, use the following XML fragment to attach the USB image:

    <disk type='file' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native'/>
      <source file='/opt/wistar/seeds/t81_vsrx4/config-drive.img'/>
      <target dev='sda' bus='usb'/>
    </disk>

11-23-2016
nembery@juniper.net
