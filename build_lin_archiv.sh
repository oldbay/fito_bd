#!/bin/bash

/usr/bin/python2 setup_cx.py build
cp -r /usr/lib/python2.7/site-packages/camelot build/exe.linux-i686-2.7/
cp -r fito_bd build/exe.linux-i686-2.7/
/usr/bin/python2 setup_cx.py bdist
