#!/bin/bash

cd build/html
python3 -m http.server

#sphinx-autobuild source/ build/html/
