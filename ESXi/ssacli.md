## HPE Storage Controller Management (ssacli) ([HP Smart Array P410 Controller](https://h20195.www2.hpe.com/v2/GetDocument.aspx?docname=c04111713&doctype=quickspecs&doclang=EN_US&searchquery=&cc=kz&lc=ru))
### Location VMware ESXi 5.1/5.5/6.0
```
/opt/hp/hpssacli/bin/hpssacli
```
### Location VMware ESXi 6.5/6.7
```
/opt/smartstorageadmin/ssacli/bin/ssacli
```

### Shortnames:
- chassisname = ch
- controller = ctrl 
- logicaldrive = ld
- physicaldrive = pd 
- drivewritecache = dwc
- licensekey = lk

### Specify drives:
- A range of drives (one to three): 1E:1:1-1E:1:3
- Drives that are unassigned: allunassigned

### Status
```
# Show - Controller Slot 1 Controller configuration basic
./ssacli ctrl slot=1 show config

# Show - Controller Slot 1 Controller configuration detailed
./ssacli ctrl slot=1 show detail

# Show - Controller Slot 1 full configuration
./ssacli ctrl slot=1 show config detail

# Show - Controller Slot 1 Status
./ssacli ctrl slot=1 show status

# Show - All Controllers Configuration
./ssacli ctrl all show config

# Show - Controller slot 1 logical drive 1 status
./ssacli ctrl slot=1 ld 1 show status

# Show - Physical Disks status basic
./ssacli ctrl slot=1 pd all show status

# Show - Physical Disk status detailed
./ssacli ctrl slot=1 pd all show status

# Show - Logical Disk status basic
./ssacli ctrl slot=1 ld all show status

# Show - Logical Disk status detailed
./ssacli ctrl slot=1 ld all show detail
```
### Create
```
# Create - New single disk volume
./ssacli ctrl slot=1 create type=ld drives=2I:0:8 raid=0 forced

# Create - New spare disk (two defined)
./ssacli ctrl slot=1 array all add spares=2I:1:6,2I:1:7

# Create - New RAID 1 volume
./ssacli ctrl slot=1 create type=ld drives=1I:0:1,1I:0:2 raid=1 forced

# Create - New RAID 5 volume
./ssacli ctrl slot=1 create type=ld drives=1I:0:1,1I:0:2,1I:0:3 raid=5 forced
```
### Adding drives to logical drive
```
# Add - All unassigned drives to logical drive 1
./ssacli ctrl slot=1 ld 1 add drives=allunassigned

# Modify - Extend logical drive 2 size to maximum (must be run with the "forced" flag)
./ssacli ctrl slot=1 ld 2 modify size=max forced
```
### Rescan controller
```
# Rescan all controllers
./ssacli rescan
```
### Drive Led Status
```
# Led - Activate LEDs on logical drive 2 disks
./ssacli ctrl slot=1 ld 2 modify led=on

# Led - Deactivate LEDs on logical drive 2 disks
./ssacli ctrl slot=1 ld 2 modify led=off

# Led - Activate LED on physical drive
ctrl slot=0 pd 1I:0:1 modify led=on

# Led - Deactivate LED on physical drive
ctrl slot=0 pd 1I:0:1 modify led=off
```
### Modify Cache Ratio
```
Modify the cache ratio on a running system can be interesting for troubleshooting and performance beanchmarking.

# Show - Cache Ratio Status
./ssacli ctrl slot=1 modify cacheratio=?

# Modify - Cache Ratio read: 25% / write: 75%
./ssacli ctrl slot=1 modify cacheratio=25/75

# Modify - Cache Ratio read: 50% / write: 50%
./ssacli ctrl slot=1 modify cacheratio=50/50

# Modify - Cache Ratio read: 0% / Write: 100%
./ssacli ctrl slot=1 modify cacheratio=0/100
```
### Modify Write Cache
```
Changing the write cache settings on the storage controller can be done with the following commands:

# Show - Write Cache Status
./ssacli ctrl slot=1 modify dwc=?

# Modify - Enable Write Cache on controller
./ssacli ctrl slot=1 modify dwc=enable forced

# Modify - Disable Write Cache on controller
./ssacli ctrl slot=1 modify dwc=disable forced

# Show - Write Cache Logicaldrive Status
./ssacli ctrl slot=1 logicaldrive 1 modify aa=?

# Modify - Enable Write Cache on Logicaldrive 1
./ssacli ctrl slot=1 logicaldrive 1 modify aa=enable

# Modify - Disable Write Cache on Logicaldrive 1
./ssacli ctrl slot=1 logicaldrive 1 modify aa=disable
```
### Delete Logical Drive
```
Deleting a logical drive on the HPE Smart Array controller can be done with the following commands.

# Delete - Logical Drive 1
./ssacli ctrl slot=1 ld 1 delete

# Delete - Logical Drive 2
./ssacli ctrl slot=1 ld 2 delete
```
### Erasing Physical Drives
In some cases, you need to erase a physical drive. This can be performed with multiple erasing options. Also, you can stop the process.

Erase patterns available:
- Default
- Zero
- Random_zero
- Random_random_zero
```
# Erase physical drive with default erasepattern
./ssacli ctrl slot=1 pd 2I:1:1 modify erase

# Erase physical drive with zero erasepattern
./ssacli ctrl slot=1 pd 2I:1:1 modify erase erasepattern=zero

# Erase physical drive with random zero erasepattern
./ssacli ctrl slot=1 pd 1E:1:1-1E:1:3 modify erase erasepattern=random_zero

# Erase physical drive with random random zero erasepattern
./ssacli ctrl slot=1 pd 1E:1:1-1E:1:3 modify erase erasepattern=random_random_zero

# Stop the erasing process on phsyical drive 1E:1:1
./ssacli ctrl slot=1 pd 1E:1:1 modify stoperase
```
### License key
```
In some cases a licence key needs to be installed on the SmartArray storage controller to enable the advanced features. 
This can be done with the following command:

# License key installation
./ssacli ctrl slot=1 licensekey XXXXX-XXXXX-XXXXX-XXXXX-XXXXX

# License key removal
./ssacli ctrl slot=5 lk XXXXXXXXXXXXXXXXXXXXXXXXX delete 
```
