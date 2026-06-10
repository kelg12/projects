# Findings

## Problems Identified

- One screw securing the HDD to the bracket was stripped already (somehow), so the bracket had to be removed along with the HDD itself.
- HFS+ file system is not readable by Windows, HFSExplorer was used to be able to mount/view HDD
- HFSExplorer was unable to view file system contents
- CrystalDiskInfo showed signs of drive degradation, with 200 Current Pending Sectors and 200 Uncorrectable Sectors
- Attempted to use DMDE to bypass bad sectors and view file system, but this returned more signs of damaged sectors
- Connected HDD to my Linux homelab machine to attempt to image the drive with `ddrescue` and prevent further degradation
- Could not mount drive successfully in Linux and drive showed more severely degraded compared to intial SMART info after `smartctl` scan

## Solution

- Used PhotoRec to extract specific file types (.jpg, .png, .mov, .pdf, etc.) from HDD since boot sector had degraded and prevented mounting
- Transferred files from homelab machine to USB drive with ```rsync -avh --progress /root/recup_dir.* /mnt/usb/```
- Happily surprised my father with his long lost photos and documents =)
