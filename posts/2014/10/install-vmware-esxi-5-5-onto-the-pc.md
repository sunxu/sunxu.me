<!-- 
.. title: Install VMware ESXI 5.5 onto the PC
.. slug: install-vmware-esxi-5-5-onto-the-pc
.. date: 2014/10/24 12:35:02
.. tags: 
.. link: 
.. description: 
.. type: text
-->

如果想试用VMware的ESXi，而又无可用的服务器，那么可以考虑把它安装到普通PC上。

ESXi对硬件的要求比较严格，主要在这几点：

<!-- TEASER_END -->

* **CPU** 64位x86架构，至少两核，如果想使用64位虚拟机，必须能够支持硬件虚拟化
* **内存** 大于4G，单条4G内存是不够的
* **磁盘控制器** SCSI/RAID，PC上是没有SCSI支持的，还需要主板支持RAID，SATA磁盘会被认为是远程设备，只能用于暂存分区
* **网卡** 需要服务器网卡，主流的PC网卡没有驱动支持，不过可以使用ESXi-Customizer工具把驱动重新打包进安装镜像中，参照
[这里](http://www.tinkertry.com/install-esxi-5-5-with-realtek-8111-or-8168-nic/ "Install ESXi 5.5 with Realtek 8111/8168 NIC") 和
[这里](http://www.v-front.de/p/esxi-customizer.html "ESXi Customizer")。

提供一套硬件配置：

* CPU: Intel Xeon E3 1230 v3
* Memory: KHX1600C9D3/4GX * 2
* Motherboard: ASRock H97M Pro4 
* Harddisk: WD1003FZEX
* NIC: Broadcom 5721 1Gbps 1000Mbps RJ45 PCI-E X1

需要注意，ESXI 5.5默认使用GPT引导而不是MBR，如果你的BIOS对UEFI支持不好，会导致安装ESXI完成后无法启动，提示`No bootable device`。

如果使用MBR引导方式，要在系统初始化安装的界面，同时按下`Shift + O`进入命令行，命令行中会出现`>runweasel`，原样保留并按下空格，之后输入`formatwithmbr`，回车以MBR引导方式安装。
