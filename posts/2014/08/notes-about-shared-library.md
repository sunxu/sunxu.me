<!-- 
.. title: Notes about Shared Library
.. slug: notes-about-shared-library
.. date: 2014/08/21 16:42:54
.. tags: 
.. link: 
.. description: 
.. type: text
-->

当程序启动时，共享库自动加载，并映射到进程的内存空间。

可使用命令`ldd`查看指定程序依赖的共享库文件：

<!-- TEASER_END -->

    # ldd /bin/ls
    linux-vdso.so.1 =>  (0x00007fff709ff000)
    libselinux.so.1 => /lib64/libselinux.so.1 (0x0000003d44600000)
    librt.so.1 => /lib64/librt.so.1 (0x0000003d43a00000)
    libcap.so.2 => /lib64/libcap.so.2 (0x0000003d45600000)
    libacl.so.1 => /lib64/libacl.so.1 (0x0000003d47a00000)
    libc.so.6 => /lib64/libc.so.6 (0x0000003d43200000)
    libdl.so.2 => /lib64/libdl.so.2 (0x0000003d42e00000)
    /lib64/ld-linux-x86-64.so.2 (0x0000003d42a00000)
    libpthread.so.0 => /lib64/libpthread.so.0 (0x0000003d43600000)
    libattr.so.1 => /lib64/libattr.so.1 (0x0000003d46600000)
    
`ldd`命令是一段 shell 脚本，其核心是设置环境变量`LD_TRACE_LOADED_OBJECTS=1`。执行`LD_TRACE_LOADED_OBJECTS=1 /bin/ls`的输出结果与`ldd`相同，原因是装载器 ld-linux.so 会判断这个变量，若非空就输出程序所依赖的动态库。如果编写一个恶意的程序，并链接到改造过的装载器，就可以忽略这个环境变量，直接执行恶意程序，所以`ldd`命令是有安全隐患的，不建议使用。可使用下面更安全的命令查看未知程序的共享库依赖：

    # objdump -p /bin/ls | grep NEEDED
    NEEDED               libselinux.so.1
    NEEDED               librt.so.1
    NEEDED               libcap.so.2
    NEEDED               libacl.so.1
    NEEDED               libc.so.6

对于进程，可使用命令`pmap`输出它的内存映射，从而得到依赖的共享库。如下：

    # pmap 14641
    14641:   /bin/cat
    0000000000400000     44K r-x--  /bin/cat
    000000000060a000      4K rw---  /bin/cat
    000000000060b000      4K rw---    [ anon ]
    000000000080a000      4K rw---  /bin/cat
    0000000001103000    132K rw---    [ anon ]
    0000003d42a00000    128K r-x--  /lib64/ld-2.12.so
    0000003d42c1f000      4K r----  /lib64/ld-2.12.so
    0000003d42c20000      4K rw---  /lib64/ld-2.12.so
    0000003d42c21000      4K rw---    [ anon ]
    0000003d43200000   1580K r-x--  /lib64/libc-2.12.so
    0000003d4338b000   2044K -----  /lib64/libc-2.12.so
    0000003d4358a000     16K r----  /lib64/libc-2.12.so
    0000003d4358e000      4K rw---  /lib64/libc-2.12.so
    0000003d4358f000     20K rw---    [ anon ]
    00007fc65ac61000  96832K r----  /usr/lib/locale/locale-archive
    00007fc660af1000     12K rw---    [ anon ]
    00007fc660b00000      4K rw---    [ anon ]
    00007fff1e4b5000     84K rw---    [ stack ]
    00007fff1e502000      4K r-x--    [ anon ]
    ffffffffff600000      4K r-x--    [ anon ]
     total           100932K
