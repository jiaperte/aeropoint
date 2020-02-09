#!/usr/bin/env python3
import sys
import re
import datetime
import dateutil.parser
import os
import shutil
import urllib.request as request
import urllib.error as error
from contextlib import closing
import pprint

def download_file_from_ftp(url_list):
    base_url = "ftp://www.ngs.noaa.gov/cors/rinex/"
    index = 0
    download_files = []
    while index < len(url_list):
        url = url_list[index]
        filename = url[url.rfind('/')+1:]
        try:
            #download hour file
            with closing(request.urlopen(base_url+url)) as r:
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r, f)
                    download_files.append(filename)
        except error.URLError as e: 
            #if hour file download fail, download full day file
            url = url.replace(url[url.find('.')-1], '0')
            filename = url[url.rfind('/')+1:]
            try: 
                with closing(request.urlopen(base_url+url)) as r:
                    with open(filename, 'wb') as f:
                        shutil.copyfileobj(r, f)
                        download_files.append(filename)
            except error.URLError as e: 
                print(url + " doesn't not exist.")

            while index < len(url_list)-1:
                if int(url_list[index].split('/')[1]) != int(url_list[index+1].split('/')[1]):
                    break
                index += 1

        index += 1

    return download_files
    
def date_to_nth_day(date, format='%Y-%m-%d'):
    date = datetime.datetime.strptime(date, format)
    new_year_day = datetime.datetime(year=date.year, month=1, day=1)
    return (date - new_year_day).days + 1


def validate_iso8601(str_val):
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex).match
    try:
        if match_iso8601(str_val) is not None:
            return True
    except:
        pass
    return False


def validate_station_id(str_val):
    regex = r'^[a-z0-9]{4}$'
    match_iso8601 = re.compile(regex).match
    try:
        if match_iso8601(str_val) is not None:
            return True
    except:
        pass
    return False


def generate_url_by_date(startDate, endDate, stationId):
    url_list=[]

    while startDate <= endDate:
        dateTmp = startDate
        nthDay = date_to_nth_day(str(dateTmp.date()))
        nthDayStr = "%03d" % nthDay
        hourCh = convertHourToChar(dateTmp.hour)
        year = str(dateTmp.year)[-2:]
        url = f"{dateTmp.year}/{nthDayStr}/{stationId}/{stationId}{nthDayStr}{hourCh}.{year}o.gz"
        url_list.append(url)
        startDate += datetime.timedelta(hours=1)

    return url_list


def convertHourToChar(hour):
    li = list(map(chr, range(ord('a'), ord('y'))))
    return li[hour]


def parse_cmdline(argv):
    argCount = len(argv)

    if argCount > 4:
        return ()

    # check args
    stationId = argv[0]
    startDate = argv[1]
    endDate = argv[2]

    #check time format is right or not
    if (not validate_iso8601(startDate) or not validate_iso8601(endDate)):
        return ()

    startDateParsed = dateutil.parser.isoparse(startDate)
    endDateParsed = dateutil.parser.isoparse(endDate)

    if endDateParsed < startDateParsed:
        print("end date should not before than start date")
        return ()

    current = datetime.datetime.now().isoformat()
    currentStr = str(current)[:current.rfind('.')] + 'Z'
    if endDateParsed > dateutil.parser.isoparse(currentStr):
         print("end date should not behind current date")
         return ()

    if not validate_station_id(stationId):  
        print("station ID format not right")
        return ()

    return (startDateParsed, endDateParsed, stationId)

def main():
    res = parse_cmdline(sys.argv[1:])
    if len(res) == 0: 
        sys.exit(2)

    startDateParsed, endDateParsed, stationId = res

    url_list = generate_url_by_date(startDateParsed, endDateParsed, stationId)
    # pprint.pprint(url_list)

    downFile = download_file_from_ftp(url_list)

    unzipFiles = []
    for file in downFile:
        os.system(f"gunzip -f {file}")
        unzipFiles.append(file[:-3])

    teqc = "./teqc"
    for file in unzipFiles:
        teqc += " " + file
    os.system(teqc + " > example.obs")

if __name__== "__main__":
  main()

