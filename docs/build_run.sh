#!/bin/bash
rm -rf build/
./autoapidoc.sh
make html

cd build/html
python3 -m http.server

#sphinx-autobuild source/ build/html/
