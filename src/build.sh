#!/usr/bin/env bash

DIR=$(dirname $0)

rm -f $DIR/ui_*.pyc

for filename in $DIR/qt/*.ui; do
    pyside-uic -x "$filename" -o "$DIR/ui_$(basename "$filename" .ui).py"
done
