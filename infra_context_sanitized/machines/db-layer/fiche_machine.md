# Fiche Machine — db-layer

## Identité
- Hostname: ghost
- OS: Ubuntu 24.04.4 LTS
- Kernel: Linux ghost 6.17.0-14-generic #14~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Jan 15 15:52:10 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
- CPU: 
- CPU details: CPU(s)= sockets= cores/socket=
- RAM: 11Gi       5.7Gi       265Mi       1.5Gi       5.8Gi       5.9Gi

## Réseau (LAN)
- Subnet: 192.168.0.0/24
- Interface: enp4s0
- IP: 192.168.0.100/24
- Gateway: 192.168.0.1
- DNS: 
- Ports en écoute (snapshot): 22, 53, 631, 1901, 5353, 9100, 32400, 32401, 32410, 32412, 32413, 32414, 32600, 34211, 36397, 36708, 40225, 43128, 44539, 50803, 51821, 56112, 60399

Note 2026-04-20: `192.168.16.179/24` est une valeur de snapshot historique (ancien routeur).

## Stockage (extrait)
### df / volumes
```
Sys. de fichiers Type     Taille Utilisé Dispo Uti% Monté sur
tmpfs            tmpfs      1.2G    2.4M  1.2G   1% /run
/dev/sda2        ext4       915G     18G  851G   3% /
tmpfs            tmpfs      5.8G    8.0K  5.8G   1% /dev/shm
tmpfs            tmpfs      5.0M     12K  5.0M   1% /run/lock
efivarfs         efivarfs   128K     40K   84K  32% /sys/firmware/efi/efivars
/dev/sda1        vfat       1.1G    6.2M  1.1G   1% /boot/efi
tmpfs            tmpfs      1.2G    2.6M  1.2G   1% /run/user/1000
```

### lsblk
```
NAME   FSTYPE   FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
loop0  squashfs 4.0                                                    0   100% /snap/core20/2686
loop1  squashfs 4.0                                                    0   100% /snap/bare/5
loop2  squashfs 4.0                                                    0   100% /snap/core22/2045
loop3  squashfs 4.0                                                    0   100% /snap/core20/2717
loop4  squashfs 4.0                                                    0   100% /snap/core22/2292
loop5  squashfs 4.0                                                    0   100% /snap/thunderbird/995
loop6  squashfs 4.0                                                    0   100% /snap/firefox/7766
loop7  squashfs 4.0                                                    0   100% /snap/firmware-updater/210
loop8  squashfs 4.0                                                    0   100% /snap/firmware-updater/167
loop9  squashfs 4.0                                                    0   100% /snap/gnome-42-2204/202
loop10 squashfs 4.0                                                    0   100% /snap/gnome-3-38-2004/143
loop11 squashfs 4.0                                                    0   100% /snap/gnome-42-2204/247
loop12 squashfs 4.0                                                    0   100% /snap/mesa-core20/172
loop13 squashfs 4.0                                                    0   100% /snap/gtk-common-themes/1535
loop14 squashfs 4.0                                                    0   100% /snap/plex-desktop/87
loop15 squashfs 4.0                                                    0   100% /snap/slack/216
loop16 squashfs 4.0                                                    0   100% /snap/snap-store/1270
loop17 squashfs 4.0                                                    0   100% /snap/snapd/24792
loop18 squashfs 4.0                                                    0   100% /snap/snapd/25935
```

## Services (extrait)
```
algo-hf-api.service           loaded active running algo_hf API (FastAPI webhook)
gnome-remote-desktop.service  loaded active running GNOME Remote Desktop
```

## Docker (extrait)
```
docker not installed / not running
```

> Généré automatiquement depuis le snapshot le 2026-02-26T17:55:55.
