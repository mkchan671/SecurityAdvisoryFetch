Format - yyyy-mm-dd
echo Date format = %date%
echo dd = %date:~0,2%
echo mm = %date:~3,2%
echo yyyy = %date:~6,4%

Python -m openVulnQuery --all --conf .\credentials.json --first_published %date:~6,4%-%date:~3,2%-01:%date:~6,4%-%date:~3,2%-%date:~0,2% --csv .\cisco.csv
pause
