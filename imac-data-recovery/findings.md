# Findings

## Problems Identified

- One screw securing the HDD to the bracket was stripped already (somehow), so the bracket had to be removed along with the HDD itself.
- HFS+ file system is not readable by Windows, HFSExplorer was used to be able to mount/view HDD
- HFSExplorer was unable to view file system contents
- CrystalDiskInfo showed signs of drive degradation, with 200 Current Pending Sectors and 200 Uncorrectable Sectors
- Attempted to use DMDE to bypass bad sectors and view file system, but this returned more signs of damaged sectors
- Connected HDD to my Linux homelab machine to image drive with `ddrescue` and prevent further degradation
