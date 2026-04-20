# Fiche Machine — student

## Identité
- Hostname: student
- OS: Debian GNU/Linux 12 (bookworm)
- Kernel: Linux student 6.1.0-43-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.162-1 (2026-02-08) x86_64 GNU/Linux
- CPU: 
- CPU details: CPU(s)= sockets= cores/socket=
- RAM: 7,6Gi       605Mi       6,4Gi       1,6Mi       907Mi       7,0Gi

## Réseau (LAN)
- Subnet: 192.168.0.0/24
- Interface: eno1
- IP: 192.168.0.142/24
- Gateway: 192.168.0.1
- DNS: 1.1.1.1, 8.8.8.8
- Ports en écoute (snapshot): 22, 631, 5353, 8020, 45095, 59623

Note 2026-04-20: `192.168.16.103/24` est une valeur de snapshot historique (ancien routeur).

## Stockage (extrait)
### df / volumes
```
Sys. de fichiers             Type     Taille Utilisé Dispo Uti% Monté sur
udev                         devtmpfs   3,8G       0  3,8G   0% /dev
tmpfs                        tmpfs      782M    1,4M  781M   1% /run
/dev/mapper/student--vg-root ext4        28G     14G   13G  52% /
tmpfs                        tmpfs      3,9G       0  3,9G   0% /dev/shm
tmpfs                        tmpfs      5,0M    8,0K  5,0M   1% /run/lock
/dev/nvme0n1p2               ext2       456M    165M  267M  39% /boot
/dev/mapper/student--vg-home ext4       200G    113M  190G   1% /home
/dev/nvme0n1p1               vfat       511M    5,9M  506M   2% /boot/efi
tmpfs                        tmpfs      782M     52K  782M   1% /run/user/1000
```

### lsblk
```
NAME                     FSTYPE      FSVER    LABEL   UUID                                   FSAVAIL FSUSE% MOUNTPOINTS
sda                      vfat        FAT16    TRADING 001B-9622                                             
nvme0n1                                                                                                     
├─nvme0n1p1              vfat        FAT32            95B2-C374                               505,1M     1% /boot/efi
├─nvme0n1p2              ext2        1.0              5d70706a-ab22-43bf-a0e5-0d045f79ab96    266,2M    36% /boot
└─nvme0n1p3              crypto_LUKS 2                b34b2289-b25c-4aaa-979f-4471116ce28e                  
  └─nvme0n1p3_crypt      LVM2_member LVM2 001         5fH2vq-LgSK-ZAOi-ZBCO-O5JI-dYUL-00ZkrE                
    ├─student--vg-root   ext4        1.0              f0b2f17c-bcee-4129-873d-bcec010b0464     12,6G    49% /
    ├─student--vg-swap_1 swap        1                ee1351fe-0e23-45f5-bed9-87f6a58e48af                  [SWAP]
    └─student--vg-home   ext4        1.0              fd092f0f-d54e-4b42-a847-611fb3497ec1    189,4G     0% /home
```

## Services (extrait)
```

```

## Docker (extrait)
```
docker not installed / not running
```

> Généré automatiquement depuis le snapshot le 2026-02-26T17:55:55.
