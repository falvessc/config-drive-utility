Create Cloud Drive Utility

This is a simple utility to create a cloud-config drive for junos devices.

## Compatibility
Tested on the following;

1. Mac OSX Darwin 10.10.5
2. Ubuntu 16.04

Junos requires a USB disk be formatted with msdos that contains a default configuration.
This simply creates a templatized Junos configuration based on some entries in the
device_parms.yaml file and creates the image. OSX utilizes hdiutil for generating disk
images where linux utilizes qemu-img.

## Desired Filesystem Output
```
root@wistar:/mnt# tar --list -f vmm-config.tar 
./
./boot/
./boot/loader.conf
./juniper.conf
```

For KVM, use the following XML fragment to attach the USB image:

    <disk type='file' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native'/>
      <source file='/opt/wistar/seeds/t81_vsrx4/config-drive.img'/>
      <target dev='sda' bus='usb'/>
    </disk>

For VMWare Fusion, support for mounting USB RAW images in VMWare Fusion is unknown at this time. (ie. I can't
get this to work [RB])

## Expected Output

### OSX
```
barnesry-mbp:config-drive-utility barnesry$ ./make_config_drive.py
Creating cloud drive image
Seed File : /var/tmp/vsrx1/config-drive.dmg
OSX Volume : CLOUD-BOOT
...................................................................................................
{...}
some configuration output here
{...}
created: /var/tmp/vsrx1/config-drive.dmg
/dev/disk3          	FDisk_partition_scheme
/dev/disk3s1        	DOS_FAT_32                     	/Volumes/CLOUD-BOOT 1
mkdir -p /Volumes/CLOUD-BOOT/boot
writing file: /boot/loader.conf
mkdir -p /Volumes/CLOUD-BOOT/
writing file: /juniper.conf
a .
a ./boot
a ./.Trashes
a ./.fseventsd
a ./juniper.conf
a ./vmm-config.tar: Can't add archive to itself
a ./.TemporaryItems
a ./.TemporaryItems/folders.36036
a ./.TemporaryItems/folders.36036/Cleanup At Startup
a ./.fseventsd/fseventsd-uuid
a ./.Trashes/36036
a ./.Trashes/36036/vmm-config
a ./.Trashes/36036/vmm-config/boot
a ./.Trashes/36036/vmm-config/.Trashes
a ./.Trashes/36036/vmm-config/.fseventsd
a ./.Trashes/36036/vmm-config/juniper.conf
a ./.Trashes/36036/vmm-config/.fseventsd/fseventsd-uuid
a ./boot/loader.conf: Can't add archive to itself
"disk2" unmounted.
"disk2" ejected.
Created /var/tmp/vsrx1/config-drive.dmg successfully. Attach this image as a USB disk before power up
```


11-23-2016
nembery@juniper.net
