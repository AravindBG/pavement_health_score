import sys
import os

# Read from the input arguments
if len(sys.argv) == 2:
    # Path of the file
    print(len(sys.argv))
    path = sys.argv[1]
    # Validate the file name
    filename, file_extension = os.path.splitext(path)
    print(file_extension)

else:
    raise Exception('No valid arguments found')

    # Read from the CSV file

    # Calculate the health score

    # Write these value to a file and save in a separate folder
