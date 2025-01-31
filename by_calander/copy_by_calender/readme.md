<b><h1>copy_by_calender Scripts</b></h1>

This Python script is designed to copy files from a source directory to a destination directory with a specific folder structure based on the filenames. It also logs the copying process to a log file.

<h5>Prerequisites:</h5>
Python 3.x<br>
Configuration<br>
Create a config.json file with the following structure:<br>
json<br>

```
{
  "sourceDirectory": "SOURCE_DIRECTORY\\DealerStmt_Archives_${month}-2023",
  "destinationRoot": "DESTINATION_DIRECTORY\\qa",
  "monthYears": ["11-2023", "12-2023", "01-2024", "02-2024"]
}
```

Replace the sourceDirectory and destinationRoot values with your specific source and destination directory paths. DealerStmt_Archives_{month}-2023 and qa need to be appended as shown.

Install the required Python packages by running:
 
pip install json
<h4>copy_by_year.py</h4>
<h5>Usage</h5>
Run the script:python.exe copy_by_year.py.py
The script will copy files from the source directory to the destination directory with the specified folder structure. It will also log the copying process to a log file.

Check the log files in the "logs" folder for details on the copying process.

<h4>copy_by_month.py</h4>
<h5>Usage</h5>
Run the script:python.exe copy_by_month.py
The script will copy files from the source directory to the destination directory with the specified folder structure that match the month and year in the config. It will also log the copying process to a log file.

Check the log files in the "logs" folder for details on the copying process.

<h4>copy_by_month_year.py</h4>
<h5>Usage</h5>
Run the script:python.exe copy_by_month_year.py
The script will delete files from the destination directories specified in the config.json file. It will also log the deletion process to a log file.

Check the log files in the "logs" folder for details on the copying process.