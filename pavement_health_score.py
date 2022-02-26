from email import header
import sys
import os
import csv


def validate_file_ext(exten):
    if exten.lowercase() == "csv":
        return True
    else:
        return False


def read_csv(path):
    try:
        # Open csv
        file = open(path, encoding='cp1252')
        # Read from the csv file
        csvreader = csv.reader(file)
        # Extract the field/header names
        headers = []
        header = next(csvreader)
        print(header)

        # Extract rows/records
        rows = []
        for row in csvreader:
            rows.append(row)
        print(rows)

    except:
        raise Exception(
            'Unable to open the file. Check the encoding of the csv file')
    finally:
        file.close()


    # Read from the input arguments
if len(sys.argv) == 2:
    # Path of the file
    path = sys.argv[1]
    # Validate the file name
    filename, file_extension = os.path.splitext(path)
    print(file_extension)
    if validate_file_ext:
        read_csv(filename+file_extension)
    else:
        raise Exception('Not a CSV file')

else:
    raise Exception('No valid arguments found')

    # Calculate the health score

    # Write these value to a file and save in a separate folder
