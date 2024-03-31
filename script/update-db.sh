#!/bin/bash

base_dir=

echo "[$(date)] Script starts"

echo "[$(date)] Unzip."
cd ${base_dir}/data/daily
zip_file=$(ls *.zip | head -n 1)
unzip ${zip_file} -d ${base_dir}/data/daily

echo "[$(date)] Update DB with the XML file."
cd ${base_dir}/dgpa-job-site
pipenv run python job/update_db.py >> ${base_dir}/log/update_db.log 2>&1

echo "[$(date)] Remove the XML file."
cd ${base_dir}/data/daily
xml_file=$(ls *.xml | head -n 1)
rm ${xml_file}

echo "[$(date)] Move the zip file to archive."
mv ${zip_file} ${base_dir}/data/archive/

echo "[$(date)] Script ends"
