# falkor_misc_utilties
Miscellaneous scripts developed for use with R/V Falkor

These scripts were developed and tested on a 2017 MacBook running OS X 10.15 (Catalina) but should run on Linux/Windows systems that have python2.7 installed.

## geojson2csv.py

This utility will convert a geoJSON formatted file that contains coordTime (timestamp) data to a csv-formatted file.  The geoJSON trackline files created for Falkor and SuBastian should have the same internal format so this utility should work for all \*.trackline.json files found in the ./<CRUISE_ID>/OpenVDM/Trackines directory.

The usage statement for geojson2csv.py:
```
usage: geojson2csv.py [-h] [-d] [-n] [-L DELIMITER] [-F DATEFORMAT]
                      [-H DATEFORMATHEADER] [-O OUTPUTFILE]
                      geojsonFile

GeoJSON to CSV conversion utility

positional arguments:
  geojsonFile           input file.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           display debug messages
  -n, --no_header       do not include the header in the output
  -L DELIMITER, --delimiter DELIMITER
                        field delimiter used in the output. (default: ",").
  -F DATEFORMAT, --dateFormat DATEFORMAT
                        date format used in the output. Use standard datetime
                        strfdate syntax (default: "%Y,%m,%d,%H,%M,%S.%f").
  -H DATEFORMATHEADER, --dateFormatHeader DATEFORMATHEADER
                        header used for the date fields of the output.
                        (default: "Year,Month,Day,Hour,Minute,Second").
  -O OUTPUTFILE, --outputFile OUTPUTFILE
                        optional output file (default is stdout).
```

### Usage Examples:

1. Convert the file “FK200930_Tracklines.json” and output the reformatted data to stdout:
```
python ./geojson2csv.py ./FK200930_Tracklines.json
```

2. Convert the file “FK200930_Tracklines.json” and save the output to “outputFile.csv":
```
python ./geojson2csv.py -O ./outputFile.csv ./FK200930_Tracklines.json
```

3. Same conversion but omit the header:
```
python ./geojson2csv.py -n -O ./outputFile.csv ./FK200930_Tracklines.json
```

4. Same conversion but change the column delimiter from a comma (,) to a space ( ):
```
python ./geojson2csv.py -L “ " -O ./outputFile.csv ./FK200930_Tracklines.json
```

The utility’s default settings will create a csv-formatted output in the following format (this is the expected output from usage examples 1 & 2):
```
Year,Month,Day,Hour,Minute,Second,Latitude,Longitude
2020,09,29,19,47,00.000000,153.06832784,-27.44204976
2020,09,29,19,48,00.000000,153.06822365,-27.4421898
2020,09,29,19,49,00.000000,153.0681,-27.44229616
2020,09,29,19,50,00.000000,153.06848107,-27.44247444
```

The files created with this utility will not include vessel/vehicle heading/speed/depth columns as those datasets are not available in the source geoJSON files.

If you require additional vehicle attitude/sensor data from the SuBastian dives then it's best to look at the Sealog csv exports in the ./<CRUISE_ID>/SuBasitan/<DIVE_ID>/Sealog folders.  These files should contain all the automatic and manually entered events for each of the dives along with ancillary data such as vehicle position/attitude, sensor data and the image filenames associated with the events.  The timestamps in these files conform to the iso8601 format standard (yyyy-mm-ddTHH:MM:SS.fffZ).  With a little column culling/massaging in Excel it should be possible to get these files into a csv format that can be imported into ArcGIS and/or other GIS application.

There is also a loweringRecord.json file for each dive that includes potentially useful data such as the dive location, summary, max depth, geographic bounding box, start/stop times, etc.

## ovdmjson2csv.py

This utiliy converts the OpenVDM data dashboard files to csv.  This may be useful to users wanting to use the OpenVDM data dashboard files but require the data be in csv format.

The usage statement for ovdmjson2csv.py:
```
usage: ovdmjson2csv.py [-h] [-d] [-n] [-L DELIMITER] [-F DATEFORMAT]
                      [-H DATEFORMATHEADER] [-O OUTPUTFILE]
                      geojsonFile

GeoJSON to CSV conversion utility

positional arguments:
  geojsonFile           input file.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           display debug messages
  -n, --no_header       do not include the header in the output
  -L DELIMITER, --delimiter DELIMITER
                        field delimiter used in the output. (default: ",").
  -F DATEFORMAT, --dateFormat DATEFORMAT
                        date format used in the output. Use standard datetime
                        strfdate syntax (default: "%Y,%m,%d,%H,%M,%S.%f").
  -H DATEFORMATHEADER, --dateFormatHeader DATEFORMATHEADER
                        header used for the date fields of the output.
                        (default: "Year,Month,Day,Hour,Minute,Second").
  -O OUTPUTFILE, --outputFile OUTPUTFILE
                        optional output file (default is stdout).
```

