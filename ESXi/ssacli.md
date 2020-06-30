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
### OUTPUTS
```
[root@localhost:~] /opt/smartstorageadmin/ssacli/bin/ssacli ctrl slot=0 show status
Smart Array P410i in Slot 0 (Embedded)
   Controller Status: OK
   Cache Status: OK
   Battery/Capacitor Status: OK


[root@localhost:~] /opt/smartstorageadmin/ssacli/bin/ssacli ctrl slot=0 show
Smart Array P410i in Slot 0 (Embedded)
   Bus Interface: PCI
   Slot: 0
   Serial Number: 5001438009A185F0
   Cache Serial Number: PBCDF0DRH6V0VD
   Controller Status: OK
   Hardware Revision: C
   Firmware Version: 3.00-0
   Firmware Supports Online Firmware Activation: False
   Rebuild Priority: Medium
   Expand Priority: Medium
   Surface Scan Delay: 15 secs
   Surface Scan Mode: Idle
   Parallel Surface Scan Supported: No
   Queue Depth: Automatic
   Monitor and Performance Delay: 60  min
   Elevator Sort: Enabled
   Degraded Performance Optimization: Disabled
   Wait for Cache Room: Disabled
   Surface Analysis Inconsistency Notification: Disabled
   Post Prompt Timeout: 0 secs
   Cache Board Present: True
   Cache Status: OK
   Cache Ratio: 25% Read / 75% Write
   Drive Write Cache: Enabled
   Total Cache Size: 1.0
   Total Cache Memory Available: 0.9
   No-Battery Write Cache: Disabled
   Cache Backup Power Source: Capacitors
   Battery/Capacitor Count: 1
   Battery/Capacitor Status: OK
   SATA NCQ Supported: True
   Number of Ports: 2 Internal only
   Encryption: Not Set
   Driver Name: nhpsa
   Driver Version: 2.0.28-1OEM
   PCI Address (Domain:Bus:Device.Function): 0000:03:00.0
   Port Max Phy Rate Limiting Supported: False
   Host Serial Number: USE033N45T
   Sanitize Erase Supported: False
   Primary Boot Volume: None
   Secondary Boot Volume: None


[root@localhost:~] /opt/smartstorageadmin/ssacli/bin/ssacli ctrl slot=0 pd all show
Smart Array P410i in Slot 0 (Embedded)
   Array A
      physicaldrive 1I:1:1 (port 1I:box 1:bay 1, SAS HDD, 146 GB, OK)
   Array B
      physicaldrive 1I:1:2 (port 1I:box 1:bay 2, SAS HDD, 600 GB, OK)
   Array C
      physicaldrive 2I:1:5 (port 2I:box 1:bay 5, SATA HDD, 1 TB, OK)
   Unassigned
      physicaldrive 1I:1:4 (port 1I:box 1:bay 4, SATA HDD, 1 TB, OK)
      physicaldrive 2I:1:8 (port 2I:box 1:bay 8, SATA HDD, 1 TB, OK)


[root@localhost:~] /opt/smartstorageadmin/ssacli/bin/ssacli ctrl slot=0 pd 1I:1:1 show status
   physicaldrive 1I:1:1 (port 1I:box 1:bay 1, 146 GB): OK


[root@localhost:~] /opt/smartstorageadmin/ssacli/bin/ssacli ctrl slot=0 pd 1I:1:4 show detail
Smart Array P410i in Slot 0 (Embedded)
   Unassigned
      physicaldrive 1I:1:4
         Port: 1I
         Box: 1
         Bay: 4
         Status: OK
         Drive Type: Unassigned Drive
         Interface Type: SATA
         Size: 1 TB
         Drive exposed to OS: False
         Logical/Physical Block Size: 512/512
         Rotational Speed: 7200
         Firmware Revision: SDM1
         Serial Number: WN91SW93
         WWID: 3001438009A185F3
         Model: ATA     ST1000LM049-2GH1
         SATA NCQ Capable: True
         SATA NCQ Enabled: True
         Current Temperature (C): 23
         Maximum Temperature (C): 48
         PHY Count: 1
         PHY Transfer Rate: 3.0Gbps
         PHY Physical Link Rate: Unknown
         PHY Maximum Link Rate: Unknown
         Sanitize Erase Supported: False
         Shingled Magnetic Recording Support: None


[root@localhost:~] /opt/smartstorageadmin/ssacli/bin/ssacli ctrl slot=0 pd 1I:1:1 show
Smart Array P410i in Slot 0 (Embedded)
   Array A
      physicaldrive 1I:1:1
         Port: 1I
         Box: 1
         Bay: 1
         Status: OK
         Drive Type: Data Drive
         Interface Type: SAS
         Size: 146 GB
         Drive exposed to OS: False
         Logical/Physical Block Size: 512/512
         Rotational Speed: 10000
         Firmware Revision: HPD6
         Serial Number: PCXPT99E
         WWID: 5000CCA00A985815
         Model: HP      DG0146FARVU
         Current Temperature (C): 25
         Maximum Temperature (C): 46
         PHY Count: 2
         PHY Transfer Rate: 6.0Gbps, Unknown
         PHY Physical Link Rate: Unknown, Unknown
         PHY Maximum Link Rate: Unknown, Unknown
         Sanitize Erase Supported: False
         Shingled Magnetic Recording Support: None


[root@localhost:~] /opt/smartstorageadmin/ssacli/bin/ssacli ctrl slot=0 ld all show
Smart Array P410i in Slot 0 (Embedded)
   Array A
      logicaldrive 1 (136.70 GB, RAID 0, OK)
   Array B
      logicaldrive 2 (558.88 GB, RAID 0, OK)
   Array C
      logicaldrive 3 (931.48 GB, RAID 0, OK)
```
