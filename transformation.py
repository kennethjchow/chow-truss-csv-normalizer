import csv
from datetime import datetime
import pytz
from pytz import reference
import sys


def main(path='sample-with-broken-utf8.csv', output_filename='output.csv'):
    input_file = open(path,  errors='replace')
    reader = csv.DictReader(input_file)
    result = []
    for row in reader:
        try:
            formatted_data = format_data(row)
            result.append(formatted_data)
        except Exception as e:
            sys.stderr.write(
                f'Error occured for row <insert unique identifier here>: {str(e)} \n')
            continue
    write_to_csv(result, output_filename)
    input_file.close()
    # close file


def format_data(row):
    """
    Description
    -----------
        Formats the data in a per row basis
    """
    time_stamp = format_timestamp(row['Timestamp'])
    zip_code = format_zip(row['ZIP'])

    address = row['Address']
    full_name = row['FullName'].upper()

    foo_duration_seconds = calculate_duration(row['FooDuration'])
    bar_duration_seconds = calculate_duration(row['BarDuration'])

    total_duration = foo_duration_seconds+bar_duration_seconds
    notes = row['Notes']

    formatted_data = {
        'Timestamp': time_stamp,
        'Address': address,
        'ZIP': zip_code,
        'FullName': full_name,
        'FooDuration': foo_duration_seconds,
        'BarDuration': bar_duration_seconds,
        'TotalDuration': total_duration,
        'Notes': notes,
    }

    return formatted_data


def format_zip(zip):
    zip_text = str(zip)
    if len(zip_text) > 5 or not zip_text.isdigit():
        raise ValueError('Invalid ZIP input')
    return zip_text.zfill(5)


def write_to_csv(data, filename='output.csv'):
    """
    Description
    -----------
        Writes data to CSV with filename
    """
    try:
        if len(data) > 0:
            keys = data[0].keys()
            with open(filename, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
        else:
            sys.stderr.write('No data to write to csv')
    except:
        sys.stderr.write('Unable to save to the csv')
        raise


def format_timestamp(date_string):
    """
    Description
    -----------
        Formats the time stamp string. Changes timezone from US Pacific to Eastern. 
        Assumption is time is by default Pacific
    Input
    -----
        date_string (str): Time stamp string in format %m/%d/%y %I:%M:%S %p

    Output
    ------
        (str): Converted time in Eastern time and RFC3339 format
    """
    pacific = pytz.timezone("US/Pacific")
    eastern = pytz.timezone("US/Eastern")

    try:
        converted_datetime = datetime.strptime(
            date_string, "%m/%d/%y %I:%M:%S %p")
    except Exception as e:
        raise Exception(f'Unable to parse timestamp. Error message: {str(e)}')

    pacific_localized = pacific.localize(converted_datetime)
    converted_eastern = pacific_localized.astimezone(eastern)

    return converted_eastern.isoformat("T") + "Z"


def calculate_duration(time_string):
    """
    Description
    -----------
        Calcualtes duration in seconds from time.
    Input
    -----
        time_string (str): Time value in expected format HH:MM:SS.MS
    Output
    ------
        num - total time calculated from time_string
    """
    split_time = list(map(int, time_string.replace('.', ':').split(':')))

    if len(split_time) != 4: 
        raise ValueError('Time is missing values')
    if not all(isinstance(x, int) for x in split_time):
        raise ValueError('Invalid non-numeric characters in time values')

    hours, minutes, seconds, millisecs = split_time
    total_time = 3600*hours + 60*minutes + seconds + millisecs/1000
    return total_time


def is_input_valid():
    '''
    Checks if the user inputs are valid
    '''
    if len(sys.argv) != 3: # 3 is used here because it's expecting 3 arguments. Python filename, input file, output file
        return False
    if not sys.argv[1].endswith('.csv') or not sys.argv[2].endswith('.csv'):
        return False
    return True


if __name__ == '__main__':
    if is_input_valid():
        input_filename = sys.argv[1] # 1 is input file name
        output_filename = sys.argv[2]# 2 is output file name
        main(input_filename, output_filename)
    else:
        sys.stderr.write(
            'Input expecting two arguments: input_file.csv and output_file_name.csv')
