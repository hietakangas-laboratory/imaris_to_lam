import os
import pandas

def csv_create(input_csv_folder, output_folder_path, spot):
    ''' This function takes a bulk IMARIS spot directory containing .csv files
    with the information for many samples within, and then makes individual
    directories for each of the samples with the same .csv files for each
    individual sample.'''

    # walks through the spot directory and finds the bulk .csv files
    for root, dirs, files in os.walk(input_csv_folder):
        for file in files:
            if file.endswith(".csv"):
                # This skips the Overall.csv which doesn't contain the
                # 'Original Image Name' column which is later used for grouping
                if not "Overall" in file:
                    csv_path = os.path.join(root, file)
                    # splits the filename for naming purposes
                    fil_split = file.split("_")
                    fil = '_'.join(fil_split[2:])
                    # reads each of the .csv files
                    df = pandas.read_csv(csv_path, header=[2])
                    # Creates groups of the data based on individual strings
                    # in the 'Original Image Name' column and puts them in
                    # respective newly created directories in the output folder
                    for id, data in df.groupby("Original Image Name"):
                        orig_dir_name = id.split("_")
                        orig_dir_name_pre = '_'.join(orig_dir_name[:-2])
                        id_dir = os.path.join(output_folder_path, orig_dir_name_pre)
                        #group = '_'.join(orig_dir_name[:-4])
                        spot_dir = orig_dir_name_pre + "_" + spot + "_statistics"
                        spot_dir_path = os.path.join(id_dir, spot_dir)
                        if not os.path.exists(id_dir):
                            os.mkdir(id_dir)
                        if not os.path.exists(spot_dir_path):
                            os.mkdir(spot_dir_path)
                        sav_loc = os.path.join(spot_dir_path, "{}".format(fil))
                        heady = "Made with\nISTL\n"
                        with open(sav_loc, 'w', encoding='utf-8') as file:
                            file.write(heady)
                            data.to_csv(file, index=False, line_terminator='\n', encoding='utf-8')
                            print(file)
