#!/bin/bash
rm -rf source/notebooks-usage/*.ipynb
cp ../examples/*U_*.ipynb source/notebooks-usage/

rm -rf source/notebooks-applications/*.ipynb
cp ../examples/*A_*.ipynb source/notebooks-applications/
