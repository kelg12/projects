# iMac Data Recovery

## Overview

This project documents the recovery of user data from a non-bootable Apple iMac (model A1224) with a failing 1TB Western Digital hard drive.

The objective was to recover family photos, videos, and personal documents from an HFS+ formatted drive that could no longer be accessed through normal operating system tools.

## Environment

### Source Hardware

- Apple iMac A1224
- Western Digital Green 1TB HDD
- HFS+ filesystem

### Recovery Systems

- Windows 10 Workstation
- Proxmox VE Host (Debian-based Linux)

### Tools Used

- CrystalDiskInfo
- HFSExplorer
- DMDE
- SMARTCTL
- Linux Kernel Logs (dmesg)
- PhotoRec
- Python 3

## Recovery Procedure

1. Researched disassembly process for Apple iMac model A1224.
2. Removed the hard drive from the iMac.
3. Connected the drive to Windows 10 workstation using a USB-to-SATA adapter.
4. Attempted filesystem access through HFSExplorer.
5. Performed partition and filesystem analysis with DMDE, discovering degredation.
6. Investigated SMART health information.
7. Connected the drive to Linux host to perform deeper analysis and recovery.
8. Analyzed Linux kernel error logs.
9. Attempted read-only HFS+ mounting.
10. Performed file carving with PhotoRec.
11. Developed Python scripts to organize recovered files.
12. Removed duplicates and sorted files by type.

## Results

- Successfully recovered family photos and videos.
- Recovered over 100,000 files
- Identified and removed over 60,000 duplicate files
- Filtered out tens of thousands of cached web assets and temporary files
- Returned organized user data to the owner

## Key Skills Demonstrated

- Hardware troubleshooting
- Filesystem analysis
- Linux administration
- Data recovery methodology
- SMART diagnostics
- Bash CLI usage
- Python automation
- Documentation and reporting
