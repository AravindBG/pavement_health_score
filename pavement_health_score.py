import sys
import os
import csv

PCI_CONSTANT = 1
BBD_CONSTANT = 1
IRI_CONSTANT = 1

directory = os.path.join(os.getcwd(), 'Results')
if not os.path.isdir(directory):
    os.mkdir(directory)


def validate_file_ext(exten):
    if exten.lowercase() == "csv":
        return True
    else:
        return False

# Write these value to a file and save in a separate folder


def create_csv_file(file_name, headers, rows):
    dest_file_name = "Result_"+file_name

    filePath = os.path.join(directory, dest_file_name)
    print("Result file path ", filePath)
    fp = open(filePath, 'w')
    # create the csv writer
    writer = csv.writer(fp)
    # print("Type ", type(headers))
    # print("Headers ", headers)
    writer.writerow(headers)
    # write a row to the csv file
    # print("Rows ", rows)
    writer.writerows(rows)
    fp.close()

# Calculate the health score


def calculate_values(row_values):
    pci = float(row_values[1])
    bbd = float(row_values[2])
    iri = float(row_values[3])

    if((0 <= pci <= 100) and (0 <= bbd <= 10) and (0 <= iri <= 10)):
        result = (pci * PCI_CONSTANT) + \
            (bbd * BBD_CONSTANT) + (iri * IRI_CONSTANT)
        # Format the result to 3 decimal points
        formatted_result = round(result, 3)
        row_values.append(str(formatted_result))
        return row_values
    else:
        return None


def read_csv(file_name):
    print("Processing file", file_name)
    try:
        # Open csv
        file = open(file_name, encoding='cp1252')
        # Read from the csv file
        csvreader = csv.reader(file)
        # Extract the field/header names
        headers = []
        headers = next(csvreader)
        headers.append("Result")
        # print(headers)

        # Extract rows/records
        rows = []
        for row in csvreader:
            if calculate_values(row) == None:
                print("Invalid input values")
            else:
                updated_row = calculate_values(row)
                rows.append(updated_row)
        # print(rows)
        create_csv_file(path, headers, rows)
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
    # print(file_extension)
    if validate_file_ext:
        read_csv(filename+file_extension)
    else:
        raise Exception('Not a CSV file')

else:
    raise Exception('No valid arguments found')
