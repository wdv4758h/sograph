========================================
sograph - shared objects' graph
========================================

Example
========================================

.. code-block:: sh

    # on Arch Linux
    $ ./sograph.py ls
    digraph graphname {
        "/usr/lib/libc.so.6" -> "/lib64/ld-linux-x86-64.so.2"
        "/usr/lib/libattr.so.1" -> "/usr/lib/libc.so.6"
        "/usr/lib/libcap.so.2" -> "/usr/lib/libc.so.6"
        "/usr/lib/libcap.so.2" -> "/usr/lib/libattr.so.1"
        "/usr/bin/ls" -> "/usr/lib/libc.so.6"
        "/usr/bin/ls" -> "/usr/lib/libattr.so.1"
        "/usr/bin/ls" -> "/usr/lib/libcap.so.2"
    }


Result :

.. image:: ./image/ls.png
