#### 2950
Release the Mode button after approximately 5 seconds when the Status (**STAT**) LED goes out. 
When you release the Mode button, the **SYST** LED blinks amber.

```
flash_init
load_helper
boot
switch:

switch: flash_init

switch: load_helper

switch: dir flash:
switch: rename flash:config.text flash:config.old
switch: boot
Switch#rename flash:config.old flash:config.text
Switch#copy flash:config.text system:running-config
```
Меняем пароль и т.п.
```
Sw1# wr
Sw1# reload
```
