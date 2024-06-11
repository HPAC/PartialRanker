#!/bin/bash
rm -rf source/api
sphinx-apidoc -o source/api/ ../partial_ranker
