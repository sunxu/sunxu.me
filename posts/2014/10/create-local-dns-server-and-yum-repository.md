<!-- 
.. title: Create Local DNS Server and Yum Repository
.. slug: create-local-dns-server-and-yum-repository
.. date: 2014/10/24 14:37:03
.. tags: 
.. link: 
.. description: 
.. type: text
-->

多台CentOS机器，更新时需要重复的下载软件包，浪费带宽更浪费时间，因此建立一个本地的Yum镜像源很有必要。同时管理多台机器，使用域名要比记住IP方便多了，DNS服务也是必不可少的。

对于这两种服务，希望尽可能少的占用资源，并且保证稳定，当然FreeBSD是最好的选择，但是从维护的方便性上，还是选择了Ubuntu。

<!-- TEASER_END -->

Ubuntu安装过程很简单，安装后修改软件源，这里使用163和中科大的源，具体方法参照
[这里](http://mirrors.163.com/.help/ubuntu.html "网易开源镜像站") 和
[这里](https://lug.ustc.edu.cn/wiki/mirrors/help/ubuntu "USTC open source mirror")。

** 更新系统 **

    apt-get update
    apt-get upgrade

** 安装软件包 **
    
    apt-get install linux-headers-server
    apt-get install build-essential
    apt-get install openssh-server portmap
    apt-get install nfs-kernel-server
    apt-get install libpcre3 libpcre3-dev
    apt-get install openssl libssl-dev
    apt-get install bind9

** 配置静态IP **

编辑 `/etc/network/interfaces`

    auto eth0
    iface eth0 inet static

    address 192.168.1.254
    netmask 255.255.255.0
    gateway 192.168.1.1

    dns-nameservers 192.168.1.254 8.8.8.8
    dns-search x

重启

    reboot

** 安装VMware Tools **

    mkdir /mnt/cdrom
    mount /dev/cdrom /mnt/cdrom
    cp /mnt/cdrom/VMwareTools-*.tar.gz .
    tar xzvf VMVMwareTools-*.tar.gz
    cd vmware-tools-distrib/
    ./vmware-install.pl
    
一路默认，安装完成后重新启动系统。

** 安装Nginx **

下载后，解压缩，编译安装

    cd nginx-*
    ./configure --prefix=/opt/nginx --with-http_ssl_module
    make && make install
    
增加启动脚本
    
    vim /etc/init.d/nginx
    #! /bin/sh
 
    ### BEGIN INIT INFO
    # Provides:          nginx
    # Required-Start:    $all
    # Required-Stop:     $all
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: starts the nginx web server
    # Description:       starts nginx using start-stop-daemon
    ### END INIT INFO
     
    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
    DAEMON=/opt/nginx/sbin/nginx
    NGINX_HOME=/opt/nginx/
    NAME=nginx
    DESC=nginx
     
    test -x $DAEMON || exit 0
     
    # Include nginx defaults if available
    if [ -f /etc/default/nginx ] ; then
        . /etc/default/nginx
    fi
     
    set -e
     
    . /lib/lsb/init-functions
     
    case "$1" in
      start)
        echo -n "Starting $DESC: "
        start-stop-daemon --start --quiet --pidfile $NGINX_HOME/logs/$NAME.pid \
            --exec $DAEMON -- $DAEMON_OPTS || true
        echo "$NAME."
        ;;
      stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon --stop --quiet --pidfile $NGINX_HOME/logs/$NAME.pid \
            --exec $DAEMON || true
        echo "$NAME."
        ;;
      restart|force-reload)
        echo -n "Restarting $DESC: "
        start-stop-daemon --stop --quiet --pidfile \
            /usr/local/nginx/logs/$NAME.pid --exec $DAEMON || true
        sleep 1
        start-stop-daemon --start --quiet --pidfile \
            /usr/local/nginx/logs/$NAME.pid --exec $DAEMON -- $DAEMON_OPTS || true
        echo "$NAME."
        ;;
      reload)
          echo -n "Reloading $DESC configuration: "
          start-stop-daemon --stop --signal HUP --quiet --pidfile $NGINX_HOME/logs/$NAME.pid \
              --exec $DAEMON || true
          echo "$NAME."
          ;;
      status)
          status_of_proc -p $NGINX_HOME/logs/$NAME.pid "$DAEMON" nginx && exit 0 || exit $?
          ;;
      *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
        exit 1
        ;;
    esac
     
    exit 0

赋予执行权限，增加服务

    chmod +x /etc/init.d/nginx
    /usr/sbin/update-rc.d -f nginx defaults

启动，停止，重启等

    service nginx start
    service nginx restart
    service nginx reload
    service nginx status
    service nginx stop

    
** 同步Yum源 **

    mkdir -p /var/mirrors/CentOS/6.5/os/x86_64
    rsync -avSHP --delete --exclude "local*" --exclude "isos" \
           rsync://mirrors.ustc.edu.cn/centos/6.5/os/x86_64/ \
           /var/mirrors/CentOS/6.5/os/x86_64

** 配置DNS服务 **

创建主区域

    cat >> /etc/bind/named.conf.local << EOF
    > zone "x" {
    >     type master;
    >     file "/var/lib/bind/x.hosts";
    >     };
    > EOF    

增加记录，创建文件 `/var/lib/bind/x.hosts`，输入以下内容

    $ttl 38400
    x.  IN  SOA x. ns.x. (
            1411160544
            10800
            3600
            604800
            38400 )
    x.  IN  NS  ns.x.
    ns.x.   IN  A   192.168.1.254
    jump.x. IN  A   192.168.1.254
    info.x. IN  A   192.168.1.254
    mirrors.x.   IN  A   192.168.1.254
    centos.mirrors.x.   IN  A   192.168.1.254
    vclient.x.  IN  A   192.168.1.21
    centos.x.  IN  A   192.168.1.51


配置转发，增加上游 DNS 服务。修改文件 `/etc/bind/named.conf.options`，增加配置

    forwarders {
        8.8.8.8;
        223.5.5.5;
        223.6.6.6;
        8.8.4.4;
        };
    forward first;
    transfer-format many-answers;

检查配置文件是否正确

    named-checkconf -z

重启

    service bind9 restart

** 安装Jailkit **

Jailkit是一个可以快速建立受限shell的工具。它将受限用户放到里面，并配置那些要在受限环境里运行的程序，可以用来制作跳板机。

    wget http://olivier.sessink.nl/jailkit/jailkit-2.17.tar.gz
    tar zxvf jailkit-2.17.tar.gz
    ./configure && make && make install
    
    mkdir /var/jail
    chown root:root  /var/jail/
    chmod 0755 /var/jail/

    jk_init -v -j /var/jail/ basicshell netutils ping
    jk_cp -v -f /var/jail/ /usr/bin/ssh-keygen
    jk_cp -v -f /var/jail/ /usr/bin/groups
    jk_cp -v -f /var/jail/ /usr/bin/vim
    
    jk_addjailuser /var/jail/ matrix
    usermod --root /var/jail/ --shell /bin/bash matrix
    
    mkdir -p /var/jail/home/matrix/.ssh/
    touch /var/jail/home/matrix/.ssh/authorized_keys
    chmod -v 0600 /var/jail/home/matrix/.ssh/authorized_keys
    chown matrix /var/jail/home/matrix/ --recursive
    chgrp users /var/jail/home/matrix/ --recursive
        
    cat > /var/jail/home/matrix/.ssh/authorized_keys << EOF
    > # RSA Public Key
    > EOF

如果配置正确，执行 `ssh matrix@localhost`，就会进入 chroot 环境，在这里只有少量命令可以使用，并且执行任何命令都不会影响主机。如果无法登录，请查看 `/var/log/daemon.log ` 和 `/var/log/auth.log` 里面的日志。

** 配置Yum源HTTP服务 **

在目录 `/opt/nginx/conf/` 下创建子目录 `conf.d/`。编辑 `/opt/nginx/conf/nginx.conf`，在 http 配置项里增加 `include conf.d/*.conf;`。

编辑 `/opt/nginx/conf/conf.d/mirrors.conf`

    server {
        charset         utf-8;
        index           index.html;

        listen          80;
        server_name     centos.mirrors.x;
        root            /var/mirrors/CentOS/;

        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
    }

**  配置Yum源NFS服务 **

编辑 `/etc/exports` 文件，增加配置

	/var/mirrors    192.168.0.0/8(ro,no_subtree_check)
	
导入配置

	exportfs -a
	
重启服务

	service nfs-kernel-server restart
	
** 配置CentOS的Yum源 **

** HTTP **

备份 `/etc/yum.repos.d/CentOS-Base.repo`，清空文件增加以下内容

	[base]
	name=CentOS-6.5 - Base
	baseurl=http://centos.mirrors.x/6.5/os/x86_64/
	gpgcheck=1
	gpgkey=http://centos.mirrors.x/6.5/os/x86_64/RPM-GPG-KEY-CentOS-6
	
** NFS **

安装 NFS 客户端，并挂载

	yum install nfs-utils
	mkdir /mnt/mirrors
	mount mirrors.x:/var/mirrors /mnt/mirrors

备份 `/etc/yum.repos.d/CentOS-Base.repo`，清空文件增加以下内容

	[base]
	name=CentOS-6.5 - Base
	baseurl=file:///mnt/mirrors/CentOS/6.5/os/x86_64
	gpgcheck=1
	gpgkey=file:///mnt/mirrors/CentOS/6.5/os/x86_64/RPM-GPG-KEY-CentOS-6

** 其他 **

可以使用 `dpkg --list | grep '^ii'` 命令列出安装的所有软件包，使用 `apt-get clean` 命令删除下载到 `/var/cache/apt/archives/` 的软件包，节省磁盘空间。
