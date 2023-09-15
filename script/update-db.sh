#!/bin/bash

base_dir=

echo "Unzip."
cd ${base_dir}/data/daily
zip_file=$(ls *.zip | head -n 1)
unzip ${zip_file} -d ${base_dir}/data/daily

echo "Update DB with the XML file."
cd ${base_dir}/dgpa-job-site
pipenv run python job/update_db.py

echo "Remove the XML file."
cd ${base_dir}/data/daily
xml_file=$(ls *.xml | head -n 1)
rm ${xml_file}

echo "Move the zip file to archive."
mv ${zip_file} ${base_dir}/data/archive/
