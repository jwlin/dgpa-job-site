#!/bin/bash

username=
server=
remote_path=
url=https://web3.dgpa.gov.tw/WANT03FRONT/AP/WANTF00003.aspx?GETJOB=Y

echo "[$(date)] Script starts"

echo "Curl XML and rename it with the data date"
curl -o today.xml $url
data_date=$(sed -n 's:.*<ANNOUNCE_DATE>\(.*\)</ANNOUNCE_DATE>.*:\1:p' today.xml)
mv today.xml ${data_date}.xml

echo "Zip the downloaded XML file"
zip "${data_date}.zip" "${data_date}.xml"

echo "SCP the zip file to a remote server"
scp ${data_date}.zip $username@$server:$remote_path

echo "Delete the XML and zip files"
rm "${data_date}.xml"
rm "${data_date}.zip"

echo "[$(date)] Script ends"