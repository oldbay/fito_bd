#!/bin/bash

cd ../../
/usr/bin/python2 setup.py extract_messages -o fito_bd.pot
mv fito_bd.pot fito_bd/translations/fito_bd.pot

