#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from contextlib import redirect_stdout
import io


class GNU_ldd(object):
    '''
    This class depend on the output of GNU ldd with `-v` argument.

    Example of `ldd -v /usr/bin/ls` on Arch Linux (x86_64):

    ```
	linux-vdso.so.1 (0x00007ffc8a0cf000)
	libcap.so.2 => /usr/lib/libcap.so.2 (0x00007fa863581000)
	libc.so.6 => /usr/lib/libc.so.6 (0x00007fa8631dd000)
	libattr.so.1 => /usr/lib/libattr.so.1 (0x00007fa862fd8000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fa863785000)

	Version information:
	/usr/bin/ls:
		libc.so.6 (GLIBC_2.14) => /usr/lib/libc.so.6
		libc.so.6 (GLIBC_2.4) => /usr/lib/libc.so.6
		libc.so.6 (GLIBC_2.17) => /usr/lib/libc.so.6
		libc.so.6 (GLIBC_2.3.4) => /usr/lib/libc.so.6
		libc.so.6 (GLIBC_2.2.5) => /usr/lib/libc.so.6
		libc.so.6 (GLIBC_2.3) => /usr/lib/libc.so.6
	/usr/lib/libcap.so.2:
		libc.so.6 (GLIBC_2.3) => /usr/lib/libc.so.6
		libc.so.6 (GLIBC_2.14) => /usr/lib/libc.so.6
		libc.so.6 (GLIBC_2.2.5) => /usr/lib/libc.so.6
		libattr.so.1 (ATTR_1.0) => /usr/lib/libattr.so.1
	/usr/lib/libc.so.6:
		ld-linux-x86-64.so.2 (GLIBC_2.3) => /lib64/ld-linux-x86-64.so.2
		ld-linux-x86-64.so.2 (GLIBC_PRIVATE) => /lib64/ld-linux-x86-64.so.2
	/usr/lib/libattr.so.1:
		libc.so.6 (GLIBC_2.4) => /usr/lib/libc.so.6
		libc.so.6 (GLIBC_2.2.5) => /usr/lib/libc.so.6
    ```
    '''


    @staticmethod
    def _get_result(command: str) -> str:
        return subprocess.check_output(['ldd', '-v', command]).decode()


    @staticmethod
    def _parse_result(command: str, result: str) -> dict:

        start = False   # flag for parsing
        name = ''       # shared object's name as key
        depend = { command: set() }     # dict for result
                                        # dict: str -> set

        for line in result.split('\n'):

            if start:

                if '=>' in line:
                    lib = line.strip().split()[-1]  # e.g. "/usr/lib/libc.so.6"
                    if not depend.get(name):
                        depend[name] = { lib }
                    else:
                        depend[name].add(lib)
                elif line:
                    name = line.strip().strip(':')  # e.g. "/usr/bin/ls"
                    if name != command:
                        depend[command].add(name)

            elif 'Version information' in line:
                start = True

        return depend


    @staticmethod
    def _draw(command: str, depend: dict) -> str:
        '''
        Generate graph in DOT.
        '''

        dot = io.StringIO()

        with redirect_stdout(dot):
            print('digraph graphname {')
            for key, values in depend.items():
                for value in values:
                    print('    "{}" -> "{}"'.format(key, value))
            print('}')

        return dot.getvalue()


    @classmethod
    def draw(self, command: str) -> None:
        '''
        method for user
        '''

        result = self._get_result(command)
        depend = self._parse_result(command, result)
        print(self._draw(command, depend), end='')


if __name__ == '__main__':
    import sys
    from shutil import which

    backend = GNU_ldd
    backend.draw(which(sys.argv[1]))    # get command's absolute path
