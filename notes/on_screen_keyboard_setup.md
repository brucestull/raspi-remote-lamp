# On-Screen Keyboard Setup

```bash
flynntknapp@LAMP-SERVER:~ $ wvkbd
bash: wvkbd: command not found
flynntknapp@LAMP-SERVER:~ $ sudo apt-get install wvkbd
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
wvkbd is already the newest version (0.12-1).
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
flynntknapp@LAMP-SERVER:~ $ wvkbd
bash: wvkbd: command not found
flynntknapp@LAMP-SERVER:~ $ sudo apt list --installed | grep wvkbd

WARNING: apt does not have a stable CLI interface. Use with caution in scripts.

wvkbd/stable,now 0.12-1 arm64 [installed]
flynntknapp@LAMP-SERVER:~ $ dpkg -L wvkbd | grep bin
/usr/bin
/usr/bin/wvkbd-mobintl
flynntknapp@LAMP-SERVER:~ $ /usr/bin/wvkbd-mobintl 
Initializing keyboard
Found 50 layouts
Found 12 layers
Resize 1920x240 1, 51 layouts
Resize 1920x240 1, 51 layouts
Resize 1920x120 1, 51 layouts
```

## Notes

- Need to add a startup script to start teh keyboard.

