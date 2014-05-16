<!-- 
.. title: Filesystem Hierarchy Standard
.. slug: filesystem-hierarchy-standard
.. date: 2014/05/16 12:35:36
.. tags: 
.. link: 
.. description: 
.. type: text
-->


* [Filesystem Hierarchy Standard](http://www.pathname.com/fhs/) (FHS)为Unix和Unix-like系统定义了目录结构和目录内容
* 该标准由[Linux Foundation](http://www.linuxfoundation.org)维护，目前版本是2.3，在2004/01/29发布
* FHS的前身是FSSTND (Filesystem Standard)
* FSSTND发起于1993/08，目的是重新规划Linux的文件和目录结构，首次发布在1994/02/14
* 1996年初，在BSD社区的帮助下，适配Unix-like系统成为下一代FSSTND的目标
* 1997/10/26，FSSTND的继任者发布，命名为FHS ([Release Announcement](http://www.pathname.com/fhs/announce-2.0.html))
* 大多数Linux发行版都遵从FHS，部分发行版在某些地方有区别
* [Linux Standard Base](http://refspecs.linuxfoundation.org/lsb.shtml) (LSB) 引用FHS作为文件系统层次结构的标准

<!-- TEASER_END -->

---

### The Root Filesystem

Directory       | Description
----------------|-----------------------------------------------
bin             | Essential command binaries
boot            | Static files of the boot loader
dev             | Device files
etc             | Host-specific system configuration
lib             | Essential shared libraries and kernel modules
media           | Mount point for removeable media
mnt             | Mount point for mounting a filesystem temporarily
opt             | Add-on application software packages
sbin            | Essential system binaries
srv             | Data for services provided by this system
tmp             | Temporary files
usr             | Secondary hierarchy
var             | Variable data
home            | User home directories (optional)
lib<qual>       | Alternate format essential shared libraries (optional)
root            | Home directory for the root user (optional)

---

### The /etc Hierarchy

File            | Description
----------------|-----------------------------------------------
csh.login       | Systemwide initialization file for C shell logins (optional)
exports         | NFS filesystem access control list (optional)
fstab           | Static information about filesystems (optional)
ftpusers        | FTP daemon user access control list (optional)
gateways        | File which lists gateways for routed (optional)
gettydefs       | Speed and terminal settings used by getty (optional)
group           | User group file (optional)
host.conf       | Resolver configuration file (optional)
hosts           | Static information about host names (optional)
hosts.allow     | Host access file for TCP wrappers (optional)
hosts.deny      | Host access file for TCP wrappers (optional)
hosts.equiv     | List of trusted hosts for rlogin, rsh, rcp (optional)
hosts.lpd       | List of trusted hosts for lpd (optional)
inetd.conf      | Configuration file for inetd (optional)
inittab         | Configuration file for init (optional)
issue           | Pre-login message and identification file (optional)
ld.so.conf      | List of extra directories to search for shared libraries (optional)
motd            | Post-login message of the day file (optional)
mtab            | Dynamic information about filesystems (optional)
mtools.conf     | Configuration file for mtools (optional)
networks        | Static information about network names (optional)
passwd          | The password file (optional)
printcap        | The lpd printer capability database (optional)
profile         | Systemwide initialization file for sh shell logins (optional)
protocols       | IP protocol listing (optional)
resolv.conf     | Resolver configuration file (optional)
rpc             | RPC protocol listing (optional)
securetty       | TTY access control for root login (optional)
services        | Port names for network services (optional)
shells          | Pathnames of valid login shells (optional)
syslog.conf     | Configuration file for syslogd (optional)

---

### The /usr Hierarchy

Directory       | Description
----------------|-----------------------------------------------
bin             | Most user commands
include         | Header files included by C programs
lib             | Libraries
local           | Local hierarchy (empty after main installation)
sbin            | Non-vital system binaries
share           | Architecture-independent data
X11R6           | XWindow System, version 11 release 6 (optional)
games           | Games and educational binaries (optional)
lib<qual>       | Alternate Format Libraries (optional)
src             | Source code (optional)

---

### /usr/local : Local hierarchy

Directory       | Description
----------------|-----------------------------------------------
bin             | Local binaries
etc             | Host-specific system configuration for local binaries
games           | Local game binaries
include         | Local C header files
lib             | Local libraries
man             | Local online manuals
sbin            | Local system binaries
share           | Local architecture-independent hierarchy
src             | Local source code

---

### /usr/share/man : Manual pages

Directory       | Description
----------------|-----------------------------------------------
man1            | User programs
man2            | System calls
man3            | Library calls
man4            | Special files
man5            | File formats
man6            | Games
man7            | Miscellaneous
man8            | System administration

---

### The /var Hierarchy

Directory       | Description
----------------|-----------------------------------------------
cache           | Application cache data
lib             | Variable state information
local           | Variable data for /usr/local
lock            | Lock files
log             | Log files and directories
opt             | Variable data for /opt
run             | Data relevant to running processes
spool           | Application spool data
tmp             | Temporary files preserved between system reboots
account         | Process accounting logs (optional)
crash           | System crash dumps (optional)
games           | Variable game data (optional)
mail            | User mailbox files (optional)
yp              | Network Information Service (NIS) database files (optional)

---

### The Annex for the Linux 

** / : Root directory. ** On Linux systems, if the kernel is located in /, we recommend using the names vmlinux or vmlinuz.

** /dev : Devices and special files. ** The following devices must exist under /dev.

* /dev/null
* /dev/zero
* /dev/tty

** /proc : Kernel and process information virtual filesystem. ** The *[proc](https://www.kernel.org/doc/Documentation/filesystems/proc.txt)* filesystem is the de-facto standard Linux method for handling process and system information, rather than */dev/kmem* and other similar methods. 

--EOF--

