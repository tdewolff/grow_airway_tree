#!/usr/bin/env bash

DIR=$(dirname $0)

rm -f $DIR/view/*.pyc

for filename in $DIR/qt/*.ui; do
    pyside-uic -x "$filename" -o "$DIR/view/ui_$(basename "$filename" .ui).py"
done
