#!/usr/bin/env python
# --------------------------------------------------------------------------- #
#
#         FILE:  geojson2csv.py
#
#  DESCRIPTION:  Convert the geojson formatted data to csv
#
#         BUGS:
#        NOTES:
#       AUTHOR:  Webb Pinner
#      COMPANY:  Capable Solutions
#      VERSION:  0.1
#      CREATED:  2020-11-20
#     REVISION:  
#
# --------------------------------------------------------------------------- #
import os
import json
import logging
from datetime import datetime

# -----------------------------------------------------------------------------
# Setup default arguments 
# -----------------------------------------------------------------------------
defaultDelimiter = ","
defaultOutputDateFormat = "%Y,%m,%d,%H,%M,%S.%f"
defaultOutputDateHeader = "Year,Month,Day,Hour,Minute,Second"
defaultHeader = ['Longitude','Latitude']

# -----------------------------------------------------------------------------
def main(geojsonFile, delimiter, dateFormat, header, outputFile):
  '''
  Read the geojson file, convert the data to csv and return the data to stdout.
  '''

  try:
    logging.info("Ingesting input file")
    with open(geojsonFile, 'r') as file:
      geojson = json.load(file)
  except Exception as e:
    logging.error("There was a problem reading the geojson file")
    raise e

# -----------------------------------------------------------------------------
# Format of geoJSON for reference
# -----------------------------------------------------------------------------
#
#{
#  "type": "FeatureCollection", 
#  "features": [
#    {
#      "geometry": {
#        "type": "LineString", 
#        "coordinates": []
#      },
#      "type": "Feature", 
#      "properties": {
#        "coordTimes": [],
#        "name": ""
#      }
#    }
#  ]
#}

  if 'coordTimes' not in geojson['features'][0]['properties']:
    logging.error("The input file does not contain date/time date.")

  elif outputFile:
    try:
      logging.info("Writing output file")
      with open(outputFile, 'w') as file:
        
        if header:
          file.write(header + '\n')

        for idx, coord in enumerate(geojson['features'][0]['geometry']['coordinates']):
          file.write(delimiter.join([datetime.fromtimestamp(geojson['features'][0]['properties']['coordTimes'][idx]/ 1e3).strftime(dateFormat),str(coord[0]),str(coord[1])]) + '\n')

    except Exception as e:
      logging.error("There was a problem writing to the output file")
      raise e

  else:
    logging.info("Writing output to stdout")
    if header:
      print(header)

    for idx, coord in enumerate(geojson['features'][0]['geometry']['coordinates']):
      print(delimiter.join([datetime.fromtimestamp(geojson['features'][0]['properties']['coordTimes'][idx]/ 1e3).strftime(dateFormat),str(coord[0]),str(coord[1])]))


# -----------------------------------------------------------------------------
if __name__ == '__main__':

  import sys
  import argparse

  parser = argparse.ArgumentParser(description='GeoJSON to CSV conversion utility')
  parser.add_argument('-v', '--verbosity', dest='verbosity',
                      default=0, action='count',
                      help='Increase output verbosity')
  parser.add_argument('-n', '--no_header', action='store_true', help=' do not include the header in the output')
  parser.add_argument('-L', '--delimiter', default=defaultDelimiter, help='field delimiter used in the output. (default: "' + defaultDelimiter + '").')
  parser.add_argument('-F', '--dateFormat', default=defaultOutputDateFormat, help='date format used in the output. Use standard datetime strfdate syntax (default: "' + defaultOutputDateFormat.replace("%", "%%") + '").')
  parser.add_argument('-H', '--dateFormatHeader', default=defaultOutputDateHeader, help='header used for the date fields of the output. (default: "' + defaultOutputDateHeader + '").')
  parser.add_argument('-O', '--outputFile', help='optional output file (default is stdout).')
  parser.add_argument('geojsonFile', help='input file.')

  parsed_args = parser.parse_args()

  ############################
  # Set up logging before we do any other argument parsing (so that we
  # can log problems with argument parsing).
  
  LOGGING_FORMAT = '%(asctime)-15s %(levelname)s - %(message)s'
  logging.basicConfig(format=LOGGING_FORMAT)

  LOG_LEVELS = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
  parsed_args.verbosity = min(parsed_args.verbosity, max(LOG_LEVELS))
  logging.getLogger().setLevel(LOG_LEVELS[parsed_args.verbosity])

  # If the optional argument was added
  if len(parsed_args.dateFormat.split(parsed_args.delimiter)) != len(parsed_args.dateFormat.split(parsed_args.delimiter)):
    logging.error("The number of columns in datetime format must match number of columns in datetime header")

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  if parsed_args.no_header:
    header = False
  else:
    header = parsed_args.dateFormatHeader.replace(defaultDelimiter, parsed_args.delimiter) + parsed_args.delimiter + parsed_args.delimiter.join(defaultHeader)

  # If the optional argument was added
  if len(parsed_args.delimiter) == 0:
    logging.error("The delimiter must contain at least one character")

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  try:
    date = datetime.utcnow()
    datestr = date.strftime(parsed_args.dateFormat)
  except:
    logging.error("The specified dateFormat is invalid.")

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  # verify the input file is valid
  if not os.path.isfile(parsed_args.geojsonFile):
    logging.error("The specified input file does not exist.")

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)


  # Run the main loop
  try:
    main(parsed_args.geojsonFile, parsed_args.delimiter, parsed_args.dateFormat.replace(defaultDelimiter, parsed_args.delimiter), header, parsed_args.outputFile)
  except KeyboardInterrupt:
    logging.info('Interrupted')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  logging.info('Complete!')
