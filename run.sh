#!/bin/bash

#Clone repository
git clone https://gitlab-ci-token:`cat token`@gitlab.sdu.dk/dath/FarmSustainaBl_Dashboard.git
cd FarmSustainaBl_Dashboard

#Install necessary packages
pip install dash
pip install dash_bootstrap_components
pip install pandas
pip install scipy
pip install seaborn
pip install numpy

########### OR Install packages in a virtual environment
#Prerequisite: venv module is installed
#python3 -m venv env
#source env/bin/activate
#pip install requirements.txt

python app.py
