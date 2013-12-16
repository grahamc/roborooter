# Roborooter

A manifest-based root reconstruction device.

![roborooter](http://pool.theinfosphere.org/images/f/f2/Robo-Rooter.png)

## No Really

Roborooter uses a collection of manifest and source files to update chroot
jails, and bring them into conformity. Pointing roborooter at a new directory
will copy all the files, directories, place symlinks and device files, and
correct permissions. Pointing roborooter at an existing root will verify all the
files exist with the proper md5, re-set permissions and ownerships, and prune
files where they shouldn't exist.

## Components and Manifest

Components implement change to the filesystem, and are driven by manifests
on the filesystem.

### DeviceFile

The DeviceFile component will create device files in the chroot. Since device IDs
can change between systems, this is done by passing the source and target
device.

Roborooter will read the device ID from the source and create the node to the
target. There is support for both block and character devices.

Manifest Location: `manifests/devices`

Format:
```
/dev/source-device ./dev/target-device
...
...
```

### Content

The Content component will create files which are missing from a source. If the
directory in the root is missing, the directory will be created.

Roborooter will verify the file on disks' MD5 sum with the MD5 sum with the
manifest. If the file does not exist or the MD5 is different, it will replace
the file with the one located at `sources/<path>`.

Manifest Location: `manifests/md5`

Format:
```
a7f5b74980904c44b97ab43d5258c366 ./lib/i386-linux-gnu/example
34840fe8bbfe8d6005ff9d3be82a33ca ./lib/x86_64-linux-gnu/example
...
...
```

If the manifest is at `1/manifests/md5` it will expect the following files to
exist:

```
1/sources/lib/i386-linux-gnu/example
1/sources/lib/x68_64-linux-gnu/example
```

**Note:** If the files in sources/ does not have the same md5 as what is
represented in the `md5` manifest file, it will be written every time.

### Permission

The Permission component will update the last four bits of the file's mode. These
are the protection bits, i.e.: `0777` or `0640`. The manifest file utilized by the
Permission component is also shared with the Owner component.

**Note:** This component will not create any files or directories, but will only
update existing file and directory modes.

Manifest Location: `manifests/permissions`

Format:
```
root:staff 0555 ./lib
root:staff 0555 ./lib/i386-linux-gnu
root:staff 0555 ./lib/x86_64-linux-gnu
user:staff 0444 ./lib/i386-linux-gnu/example
root:staff 0555 ./dev
root:staff 0666 ./dev/random
```

### Owner

The Owner component will update the owner and group of a file or directory. The
manifest file utilized by the Owner component is also shared with the Permission
component.

**Note:** This component will not create any files or directories, but will only
update existing file and directory modes.

Manifest Location: `manifests/permissions`

Format:
```
root:staff 0555 ./lib
root:staff 0555 ./lib/i386-linux-gnu
root:staff 0555 ./lib/x86_64-linux-gnu
user:staff 0444 ./lib/i386-linux-gnu/example
root:staff 0555 ./dev
root:staff 0666 ./dev/random
```

### Whitelist

The Whitelist component enforces restrictions on which files should exist on the
disk. Any files which exist on the disk and are not permitted by the whitelist
will be removed. Note that the Whitelist component will not remove directories,
even if they are not listed in the whitelist. This behavior may change.

Manifest Location: `manifests/whitelist`

Format:
```
./htdocs/
./lib/i386-linux-gnu/example
./lib/x86_64-linux-gnu/example
./dev/random
```

In this manifest, by whitelisting the `./htdocs/` directory, Roborooter will not
remove any files within it. If a file were created in `./lib/` however, it would
be removed.

**Note:** Any file created in any manifest MUST be included in the whitelist,
else it will be removed by the whitelist component.

