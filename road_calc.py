import pandas as pd
import sys
import os
import shutil

k_PCI = "PCI"
k_BBD = "BBD"
k_IRI = "IRI"
k_traffic_volume = "Traffic Volume"

result_directory = os.path.join(os.getcwd(), 'output/result')

if not os.path.isdir(result_directory):
    os.makedirs(result_directory)

intermediate_directory = os.path.join(os.getcwd(), 'output/intermediate')

if not os.path.isdir(intermediate_directory):
    os.makedirs(intermediate_directory)


def validate_file_ext(exten):
    if exten.lowercase() == "xlsx":
        return True
    else:
        return False


# Convert the xlsx to csv

def convert_to_csv(path, file_name):
    read_file = pd.read_excel(path)
    intermediate_file_path = os.path.join(
        intermediate_directory, file_name + ".csv")
    # print(intermediate_file_path)
    read_file.to_csv(intermediate_file_path,
                     index=None,
                     header=True)
    return intermediate_file_path


def update_csv_with_sum_values(result_file_path, row):
    # print(intermediate_file_path)
    df = pd.DataFrame(row).T
    try:
        with open(result_file_path, 'a') as f:
            df.to_csv(f, header=False, index=False)
            # print('Success')
    except:
        print('Unable to Write CSV')


k_PCI_N = "PCI_N"
k_BBD_N = "BBD_N"
k_IRI_N = "IRI_N"
k_traffic_volume_N = "Traffic Volume_N"
k_total = "Total"
k_pavement_condition = 0.379154447702835
k_bbd = 0.161107038123167
k_iri = 0.379154447702835
k_traffic_loading = 0.0805840664711632
k_PCI_W = "W_PCI"
k_BBD_W = "W_BBD"
k_IRI_W = "W_IRI"
k_traffic_volume_W = "W_Traffic Volume"
k_selection_priority_index = "Section Priority Index"


def update_csv_with_calculations(result_file_path, sum_values):
    df = pd.read_csv(result_file_path)

    for index, row in df.iterrows():
        if row[0] == k_total:
            break
        df.at[index, k_PCI_N] = row[1]/sum_values[1]
        df.at[index, k_BBD_N] = row[2]/sum_values[2]
        df.at[index, k_IRI_N] = row[3]/sum_values[3]
        df.at[index, k_traffic_volume_N] = row[4]/sum_values[4]

        pc = (row[1]/sum_values[1]) * k_pavement_condition
        df.at[index, k_PCI_W] = pc
        bbd = (row[2]/sum_values[2]) * k_bbd
        df.at[index, k_BBD_W] = bbd
        iri = (row[3]/sum_values[3]) * k_iri
        df.at[index, k_IRI_W] = iri
        tv = (row[4]/sum_values[4]) * k_traffic_loading
        df.at[index, k_traffic_volume_W] = tv
        df.at[index, k_selection_priority_index] = pc + bbd + iri + tv
        # print(index, row[0])

    try:
        with open(result_file_path, 'w') as f:
            df.to_csv(f, header=True, index=False)
            # print('Success')
    except:
        print('Unable to Write CSV')


def add_values(intermediate_file_path):
    # print("Processing file", intermediate_file_path)
    df = pd.read_csv(intermediate_file_path)

    totalPCI = 0
    saved_col_PCI = df[k_PCI]
    for val in saved_col_PCI.values:
        totalPCI += val
    # print(totalPCI)

    totalBBD = 0
    saved_col_BBD = df[k_BBD]
    for val in saved_col_BBD.values:
        totalBBD += val
    # print(totalBBD)

    totalIRI = 0
    saved_col_IRI = df[k_IRI]
    for val in saved_col_IRI.values:
        totalIRI += val
    # print(totalIRI)

    total_traffic_volume = 0
    saved_col_t_v = df[k_traffic_volume]
    for val in saved_col_t_v.values:
        total_traffic_volume += val
    # print(total_traffic_volume)

    return ["Total", round(totalPCI, 2), round(totalBBD, 2), round(totalIRI, 2), round(total_traffic_volume, 2)]


# Read from the input arguments
if len(sys.argv) == 2:
    # Path of the file
    path = sys.argv[1]
    # Validate the file name
    base_name, file_extension = os.path.splitext(path)
    # print(base_name, file_extension)
    if validate_file_ext:
        file_name = os.path.basename(path)
        # print(f"File name {file_name} file extension {file_extension}")
        exact_file_name = os.path.splitext(file_name)[0]
        # print(f"exact file name {exact_file_name}")

        # convert it to csv
        intermediate_csv_path = convert_to_csv(path, exact_file_name)
        sum_values = add_values(intermediate_csv_path)

        csv_file_name = os.path.basename(intermediate_csv_path)
        result_path = os.path.join(result_directory, "result_"+csv_file_name)

        # print(
        #     f"Intermediate file path --> {intermediate_csv_path}, Result file name --> {csv_file_name}")
        # move a copy to result folder
        shutil.copyfile(intermediate_csv_path, result_path)
        # Update with csv with sum values
        update_csv_with_sum_values(result_path, sum_values)
        # Update csv with calculations
        update_csv_with_calculations(result_path, sum_values)
    else:
        raise Exception('Input file is not a xlsx file')

else:
    raise Exception('No valid arguments found')
