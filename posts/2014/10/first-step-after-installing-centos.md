<!-- 
.. title: First Step after Installing CentOS
.. slug: first-step-after-installing-centos
.. date: 2014/10/24 16:11:24
.. tags: 
.. link: 
.. description: 
.. type: text
-->

CentOS release 6.5 (Final) x86_64

<!-- TEASER_END -->

** 网络配置 **

静态IP

	# vi /etc/sysconfig/network-scripts/ifcfg-eth0

	ONBOOT=yes
	BOOTPROTO=none
	IPADDR=192.168.1.100
	NETMASK=255.255.255.0
	NETWORK=192.168.1.0

	PEERDNS=yes
	DOMAIN=x
	DNS1=192.168.1.254
	DNS2=8.8.8.8
	
	# service network restart

动态IP

	# vi /etc/sysconfig/network-scripts/ifcfg-eth0
	ONBOOT=yes
	BOOTPROTO=dhcp

	PEERDNS=yes
	DOMAIN=x
	DNS1=192.168.1.254
	DNS2=8.8.8.8

	# service network restart


** Yum源配置 **

备份 `/etc/yum.repos.d/CentOS-Base.repo`，更新 `[base]` 配置

	[base]
	name=CentOS-6.5 - Base
	baseurl=http://centos.mirrors.x/6.5/os/x86_64/
	gpgcheck=1
	gpgkey=http://centos.mirrors.x/6.5/os/x86_64/RPM-GPG-KEY-CentOS-6

安装 NFS 客户端，挂载Yum源

	yum upgrade
	yum install nfs-utils
	mkdir /mnt/mirrors
	# mount mirrors.x:/var/mirrors /mnt/mirrors
	vi /etc/fstab
	mirrors.x:/var/mirrors /mnt/mirrors nfs ro 0 0
	mount -a

更新Yum源

	[base]
	name=CentOS-6.5 - Base
	baseurl=file:///mnt/mirrors/CentOS/6.5/os/x86_64
	gpgcheck=1
	gpgkey=file:///mnt/mirrors/CentOS/6.5/os/x86_64/RPM-GPG-KEY-CentOS-6
	
	[updates]
	name=CentOS-6.5 - Updates
	baseurl=file:///mnt/mirrors/CentOS/6.5/updates/x86_64
	gpgcheck=1
	gpgkey=file:///mnt/mirrors/CentOS/6.5/os/x86_64/RPM-GPG-KEY-CentOS-6


** 软件安装 **

	yum groupinstall "Development Tools"
	yum update

** VMware Tools **

    mkdir /mnt/cdrom
    mount /dev/cdrom /mnt/cdrom
    cp /mnt/cdrom/VMwareTools-*.tar.gz .
    tar xzvf VMVMwareTools-*.tar.gz
    cd vmware-tools-distrib/
    ./vmware-install.pl
    
一路默认，安装完成后重新启动系统。

** 导出VOF模板 **

导出前，删除文件 `/etc/udev/rules.d/70-persistent-net.rules`，编辑文件 `/etc/sysconfig/network-scripts/ifcfg-eth0`，删除 MACADDR 项。
	
