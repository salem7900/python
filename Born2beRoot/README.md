*This project has been created as part of the 42 curriculum by sabdalla.*

# Born2beRoot

## Description

Born2beRoot is a system administration project whose goal is to learn the basics of setting up a secure, minimal Linux server from scratch using virtualization. Rather than using a graphical environment, the entire system is configured and administered through the command line, following strict security rules imposed by the subject.

The project consists of installing Debian inside a VirtualBox virtual machine, partitioning the disk with encrypted LVM, setting up a dedicated non-root user with controlled sudo privileges, securing remote access through SSH on a non-standard port, configuring a firewall that only allows the strictly necessary traffic, enforcing a strong password policy, and writing a bash monitoring script that reports the server's status at regular intervals.

The overall objective is not just to make the server "work", but to understand *why* each configuration choice is made from a security standpoint, since every decision is later discussed and justified during a peer-evaluation defense.

## Instructions

### Requirements
- VirtualBox installed on the host machine
- A Debian 13 (stable) `netinst` ISO image
- At least 8–10 GB of free disk space for the virtual machine

### Setting up the VM
1. Create a new VM in VirtualBox (Linux / Debian 64-bit), with the `.vdi` disk type, dynamically allocated.
2. Mount the Debian netinst ISO as the virtual CD/DVD drive and boot the VM.
3. During installation:
   - Set the hostname to `<login>42` (e.g. `sabdalla42`).
   - Create a standard user with the same username as your 42 login.
   - When prompted for partitioning, choose **"Guided – use entire disk and set up encrypted LVM"** and set a strong encryption passphrase.
   - At the software selection screen, **deselect every desktop environment** (GNOME, etc.) and keep only `SSH server` and `standard system utilities`. Installing a graphical server (X.org/Wayland) is forbidden by the subject and results in a grade of 0.
4. Finish the installation and reboot into the console (tty), with no graphical interface.

### Connecting to the VM
Once SSH is configured (see below), the VM can be reached from the host machine via port forwarding (NAT) on port 4242:

```
ssh -p 4242 <login>@127.0.0.1
```

### What has been configured
- **Partitioning**: LVM on top of a LUKS-encrypted partition, with at least two logical volumes (root, swap).
- **sudo**: limited to 3 password attempts, custom error message on failure, full input/output logging to `/var/log/sudo/`, TTY mode required, restricted `secure_path`.
- **User management**: in addition to `root`, a user named after the 42 login exists and belongs to both the `sudo` and `user42` groups.
- **SSH**: running on port 4242, root login disabled.
- **Firewall (UFW)**: active on every boot, only port 4242 is open (TCP, IPv4 and IPv6).
- **Password policy**: 30-day expiration, 2-day minimum between changes, 7-day warning before expiration, minimum 10 characters with uppercase, lowercase and digit, no more than 3 identical consecutive characters, username not allowed inside the password, at least 7 new characters compared to the previous password (not enforced for root).
- **AppArmor**: loaded and active at every boot.
- **monitoring.sh**: a bash script located at `/usr/local/bin/monitoring.sh`, scheduled through root's crontab (`@reboot` and every 10 minutes) and broadcast to every terminal using `wall`. It reports architecture/kernel, physical CPU count, vCPU count, RAM usage, disk usage, CPU load, last boot date, LVM status, active TCP connections, logged-in users, IPv4/MAC address, and the number of commands executed with sudo.

### Testing it yourself
- `sudo ufw status verbose` → check the firewall rules.
- `sudo systemctl status ssh` / `ss -tunlp | grep 4242` → check SSH is listening on the correct port.
- `groups <login>` → check the user belongs to `sudo` and `user42`.
- `sudo crontab -l` → check the monitoring script is scheduled.
- `sudo /usr/local/bin/monitoring.sh` → manually trigger the monitoring broadcast.

## Resources

- Official Debian documentation: [debian.org/releases/stable](https://www.debian.org/releases/stable/)
- `man` pages consulted directly on the system: `sudoers(5)`, `pam_pwquality(8)`, `ufw(8)`, `crontab(5)`, `sshd_config(5)`, `apparmor(7)`
- VirtualBox official documentation for NAT port forwarding and disk/VM management
- Various Born2beRoot walkthrough videos on YouTube, used only to understand general concepts (LVM/LUKS encryption, PAM password policies) — never to copy commands blindly, and always cross-checked against the official subject and `man` pages before applying them

### AI usage disclosure
An AI assistant (Claude, by Anthropic) was used throughout this project, consistently with the 42 AI policy described in the subject: as a guide, not as a source of direct answers. Concretely, it was used to:
- Get pointed toward the *concept* or the right command to research (e.g. being told to look into `pam_pwquality`, `chage`, `/etc/update-motd.d/`, `@reboot` in crontab, `find`/`wc -l` combinations) without being given a ready-made solution to copy;
- Debug specific, already-attempted configurations that failed (e.g. a `visudo` editor misconfiguration, an SSH port-forwarding "connection refused" caused by using the wrong SSH client environment, a `wall` message not reaching an SSH pseudo-terminal, a `sudo` call inside `monitoring.sh` that was inflating its own counter);
- Review the logic of commands that had already been written (e.g. checking `awk` field numbering in `free`/`df` parsing, confirming the difference between `used` and `available` memory);
- Get guidance on the overall order of the mandatory steps, and on how to interpret ambiguous parts of the subject (e.g. the `difok` rule not applying to root, which has no clean native solution in `pam_pwquality`);
- Draft and structure this README itself, based on the configuration choices actually made and tested during the project.

All commands were typed, executed, tested and debugged personally on the virtual machine; the AI was never asked to directly solve a requirement from the subject without the author first attempting it or understanding the reasoning behind it.

## Project description — Technical choices

### Why Debian
Debian was chosen over Rocky Linux mainly because it was explicitly recommended by the subject for students new to system administration, and because its tooling (`apt`, PAM, UFW) is generally considered more approachable than Rocky's enterprise-oriented stack (`dnf`, SELinux, firewalld).

### Debian vs Rocky Linux
| | Debian | Rocky Linux |
|---|---|---|
| Origin | Community-driven, one of the oldest Linux distributions | Community rebuild of Red Hat Enterprise Linux (RHEL) |
| Package manager | `apt` / `dpkg`, `.deb` packages | `dnf` / `yum`, `.rpm` packages |
| Release philosophy | Strong focus on stability and free software; slower, very predictable release cycle | Follows RHEL's enterprise release cycle, long-term support oriented |
| Typical use case | Servers, desktops, embedded systems, very flexible | Enterprise servers, environments requiring RHEL compatibility |
| Learning curve | Generally considered beginner-friendlier | Slightly steeper due to SELinux and enterprise conventions |

### AppArmor vs SELinux
Both are Linux Security Modules (LSM) used to enforce Mandatory Access Control, restricting what a process can do beyond standard Unix permissions.
- **AppArmor** (used on Debian) is path-based: security profiles are attached to file paths and are generally easier to read and write, which is why it was the simpler option for this project.
- **SELinux** (used on Rocky) is label-based: every file and process is tagged with a security context, allowing more fine-grained control, but at the cost of a steeper learning curve and more complex troubleshooting (e.g. `sestatus`, contexts, booleans).

### UFW vs firewalld
- **UFW** (Uncomplicated Firewall, used on Debian) provides a simple command-line syntax (`ufw allow 4242/tcp`) built on top of `iptables`/`nftables`, aimed at making firewall management approachable.
- **firewalld** (used on Rocky) is zone-based: rules are attached to "zones" representing different trust levels (public, internal, trusted, etc.), which is more flexible for complex network setups but requires understanding the zone concept first.

### VirtualBox vs UTM
- **VirtualBox** is a free, cross-platform (Windows/Linux/macOS Intel) type-2 hypervisor from Oracle, widely documented and was used for this project.
- **UTM** is a free virtualization/emulation tool for macOS, particularly relevant on Apple Silicon (M1/M2/M3) Macs where VirtualBox's support is limited; it is based on QEMU and leverages Apple's native Hypervisor framework for better performance on ARM-based Macs.

### Partitioning, security policy and user management summary
The disk is partitioned with a small unencrypted `/boot` partition and a LUKS-encrypted container holding an LVM volume group, itself split into at least a `root` and a `swap` logical volume (see **Instructions** above for the exact setup used). On top of the base installation, the following security layers were added, in this order: SSH hardening (custom port, no root login), a default-deny UFW firewall with a single opened port, a `sudo` configuration enforcing logging, limited retries and restricted paths, and a PAM-enforced password policy applied to every account, including root. A dedicated `monitoring.sh` script, scheduled through root's crontab, provides continuous visibility into the server's resource usage and sudo activity without requiring a graphical interface.
