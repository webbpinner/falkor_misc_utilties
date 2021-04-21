#!/usr/bin/env python
# --------------------------------------------------------------------------- #
#
#         FILE:  ovdmjson2csv.py
#
#  DESCRIPTION:  Convert the OpenVDM data dashboard files for navigational
#                data to csv.
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
# Setup logging 
# -----------------------------------------------------------------------------

# Default logging level
LOG_LEVEL = logging.INFO

# create logger
logger = logging.getLogger(__file__)
logger.setLevel(LOG_LEVEL)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)

# create formatter
formatter = logging.Formatter('%(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


# -----------------------------------------------------------------------------
# Setup default arguments 
# -----------------------------------------------------------------------------

defaultDelimiter = ","
defaultOutputDateFormat = "%Y,%m,%d,%H,%M,%S.%f"
defaultOutputDateHeader = "Year,Month,Day,Hour,Minute,Second"
defaultGeoJSONHeader = ['Latitude (ddeg)', 'Longitude (ddeg)']


# -----------------------------------------------------------------------------
def buildHeaderArray(ovdm_jsonFile, delimiter):
  '''
  Builds csv header record
  '''

  global defaultGeoJSONHeader

  try:
    logger.info("Building Header record")
    with open(ovdm_jsonFile, 'r') as file:
      jsonFile = json.load(file)
  except Exception as e:
    logger.error("There was a problem reading the JSON file")
    raise e

  if 'type' in jsonFile['visualizerData'][0]:
    logger.info("JSON file contains position data")
    logger.debug("Header:", defaultGeoJSONHeader)
    return defaultGeoJSONHeader

  elif 'data' in jsonFile['visualizerData'][0]:
    headerArray = []
    for dataset in jsonFile['visualizerData']:
      headerArray.append("{} ({})".format(dataset['label'], dataset['unit']).replace(delimiter, ""))

    logger.debug("Header: {}".format(delimiter.join(headerArray)))
    return headerArray

  else:
    logger.error("JSON file does not appear to be an OpenVDM data dashboard file.")

  return False;


# -----------------------------------------------------------------------------
def main(ovdm_jsonFile, delimiter, dateFormat, header, outputFile):
  '''
  Main function of the script.  Loads the ovdm_jsonFile, processes it and
  returns csv to stdout
  '''

  try:
    logger.info("Ingesting input file")
    with open(ovdm_jsonFile, 'r') as file:
      jsonFile = json.load(file)
  except Exception as e:
    logger.error("There was a problem ingesting the JSON file")
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

  # input file contains geo-referenced data.
  if 'type' in jsonFile['visualizerData'][0]:
    if 'coordTimes' not in jsonFile['visualizerData'][0]['features'][0]['properties']:
      logger.error("The input file does not contain date/time date.")

    elif outputFile:
      try:
        logger.info("Writing output file")
        with open(outputFile, 'w') as file:
          
          if header:
            file.write(header + '\n')

          for idx, coord in enumerate(jsonFile['visualizerData'][0]['features'][0]['geometry']['coordinates']):
            file.write(delimiter.join([datetime.fromtimestamp(jsonFile['visualizerData'][0]['features'][0]['properties']['coordTimes'][idx]/ 1e3).strftime(dateFormat),str(coord[0]),str(coord[1])]) + '\n')

      except Exception as e:
        logger.error("There was a problem writing to the output file")
        raise e

    else:
      logger.info("Writing output to stdout")
      if header:
        print(header)

      for idx, coord in enumerate(jsonFile['visualizerData'][0]['features'][0]['geometry']['coordinates']):
        print(delimiter.join([datetime.fromtimestamp(jsonFile['visualizerData'][0]['features'][0]['properties']['coordTimes'][idx]/ 1e3).strftime(dateFormat),str(coord[0]),str(coord[1])]))

  # input file contains time-series data.
  elif 'data' in jsonFile['visualizerData'][0]:

    if outputFile:
      try:
        logger.info("Writing output file")
        with open(outputFile, 'w') as file:
          
          if header:
            file.write(header + '\n')

          for idx, timeRef in enumerate(jsonFile['visualizerData'][0]['data']):
            dataRow = []
            dataRow.append(datetime.fromtimestamp(timeRef[0]/ 1e3).strftime(dateFormat))

            for dataset in jsonFile['visualizerData']:

              dataRow.append(str(dataset['data'][idx][1]) if dataset['data'][idx][1] else "")

            file.write(delimiter.join(dataRow) + '\n')

      except Exception as e:
        logger.error("There was a problem writing to the output file")
        raise e

    else:
      logger.info("Writing output to stdout")
      if header:
        print(header)

        for idx, timeRef in enumerate(jsonFile['visualizerData'][0]['data']):
          dataRow = []
          dataRow.append(datetime.fromtimestamp(timeRef[0]/ 1e3).strftime(dateFormat))

          for dataset in jsonFile['visualizerData']:

            # print(dataset['data'][idx][1])

            dataRow.append(str(dataset['data'][idx][1]) if dataset['data'][idx][1] else "")

          print(delimiter.join(dataRow))

  # logger.debug(json.dumps(jsonFile, indent=2))

# -----------------------------------------------------------------------------
if __name__ == '__main__':

  import sys
  import argparse

  parser = argparse.ArgumentParser(description='OpenVDM JSON to CSV conversion utility')
  parser.add_argument('-d', '--debug', action='store_true', help=' display debug messages')
  parser.add_argument('-n', '--no_header', action='store_true', help=' do not include the header in the output')
  parser.add_argument('-L', '--delimiter', default=defaultDelimiter, help='field delimiter used in the output. (default: "' + defaultDelimiter + '").')
  parser.add_argument('-F', '--dateFormat', default=defaultOutputDateFormat, help='date format used in the output. Use standard datetime strfdate syntax (default: "' + defaultOutputDateFormat.replace("%", "%%") + '").')
  parser.add_argument('-H', '--dateFormatHeader', default=defaultOutputDateHeader, help='header used for the date fields of the output. (default: "' + defaultOutputDateHeader + '").')
  parser.add_argument('-O', '--outputFile', help='optional output file (default is stdout).')
  parser.add_argument('ovdm_jsonFile', help='input OpenVDM data dashboard file.')

  args = parser.parse_args()

  # Turn on debug mode
  if args.debug:
    logger.info("Setting log level to DEBUG")
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
      handler.setLevel(logging.DEBUG)
    logger.debug("Log level now set to DEBUG")

  # If the optional argument was added
  if len(args.dateFormat.split(args.delimiter)) != len(args.dateFormat.split(args.delimiter)):
    logger.error("The number of columns in datetime format must match number of columns in datetime header")

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  # If the optional argument was added
  if len(args.delimiter) == 0:
    logger.error("The delimiter must contain at least one character")

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  try:
    date = datetime.utcnow()
    datestr = date.strftime(args.dateFormat)
  except:
    logger.error("The specified dateFormat is invalid.")

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  # verify the input file is valid
  if not os.path.isfile(args.ovdm_jsonFile):
    logger.error("The specified input file does not exist.")

    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  if args.no_header:
    header = False
  else:
    header = args.dateFormatHeader.replace(defaultDelimiter, args.delimiter) + args.delimiter + args.delimiter.join(buildHeaderArray(args.ovdm_jsonFile, args.delimiter))

  # Run the main loop
  try:
    main(args.ovdm_jsonFile, args.delimiter, args.dateFormat.replace(defaultDelimiter, args.delimiter), header, args.outputFile)
  except KeyboardInterrupt:
    logger.info('Interrupted')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

  logger.info('Complete!')
