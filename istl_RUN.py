'''
    Author: Jack Morikka.

    This program is intended to take bulk collected data from an IMARIS batch
    run that outputs channels (or spots) and convert it into a format ready for
    LAM analysis. This bulk data consists of e.g. a Spots_1 directory which
    contains .csv files such as 'Area.csv' and 'positions.csv' etc. for every
    sample that was processed in the IMARIS batch. This program essentially
    separates out these samples creating the same excel files for single
    samples in their own unique folders with the spot name (e.g. DAPI, GFP,
    MP etc.) clearly indicated in a fashion readable by LAM.

    The user selects the bulk 'spot' folder e.g. Spots_1_Statistics, and
    chooses an empty output folder where the new folders with .csv files will
    be sent. The user then names this 'spot' e.g. DAPI, GFP or MP. The user
    then runs the program. For the same bulk data the user then reruns the
    program and picks another 'spot' folder e.g. Spots_2_Statistics and chooses
    the SAME output folder which they selected for the first 'spot' folder.
    '''


from tkinter import *
from tkinter import filedialog
import logging
import istl



class Imaris_to_lam:

    def __init__(self):

        # Creates the structure for the GUI with the title
        self.__window = Tk()
        self.__window.title('Imaris_to_LAM')

        # Creates label for select spot folder selection prompt
        self.__s_ij_prompt = Label(self.__window,
                                   text='Select spot folder:') \
            .grid(row=3, column=1, sticky=E)

        # Creates the browse button for getting the spot folder path
        Button(self.__window, text='Browse', command=self.retrieve_csv_folder) \
            .grid(row=3, column=2)

        # Creates the variable label for spot folder path text
        self.__csv_folder = StringVar()
        self.__selectij = Label(self.__window, text=self.__csv_folder.get(),
                                bg='white', bd=2,
                                textvariable=self.__csv_folder, relief='sunken')
        self.__selectij.grid(row=3, column=3, columnspan=3, sticky=W)

        # Creates label for select output folder prompt
        self.__r_dir_prompt = Label(self.__window,
                                    text='Select output folder:') \
            .grid(row=5, column=1, sticky=E)

        # Creates the browse button for getting the output folder
        Button(self.__window, text='Browse', command=self.retrieve_ofolder) \
            .grid(row=5, column=2)

        # Creates the variable label for output folder text
        self.__ofolder = StringVar()
        self.__selectDir = Label(self.__window, text=self.__ofolder.get(),
                                 bg='white', bd=2,
                                 textvariable=self.__ofolder, relief='sunken')
        self.__selectDir.grid(row=5, column=3, columnspan=3, sticky=W)

        # Creates the spot name entry input field
        self.__name_prompt = Label(self.__window,
                                    text='Enter spot name '
                                         '(e.g. DAPI, GFP, MP etc.:)') \
            .grid(row=9, column=1)

        self.__name_input = Entry(self.__window, width=5)
        self.__name_input.grid(row=9, column=2, padx=5, ipadx=5)

        # Creates the run button for running the simulator
        Button(self.__window, text='Run', command=self.go) \
            .grid(row=11, column=1, sticky=E)

        # Creates button for quitting the stitcher
        Button(self.__window, text='Quit', command=self.quit_func) \
            .grid(row=11, column=2, sticky=W)

    def retrieve_csv_folder(self):
        ''' Prompts the user to select the buld 'spot' folder'''

        selected_directory = filedialog.askdirectory()
        self.__csv_folder.set(selected_directory)

    def retrieve_ofolder(self):
        ''' Prompts the user to select an output folder'''

        selected_directory = filedialog.askdirectory()
        self.__ofolder.set(selected_directory)


    def go(self):
        ''' If an input folder, output folder and spot name are selected, this
        function imports the istl csv_create function to use on the bulk .csv
        files to create new directories for each sample and new .csv files
        for each sample to be used with LAM'''

        # Checks that no fields are left blank
        if self.__ofolder.get() == '' or self.__csv_folder.get() == '' or self.__name_input.get() == '':
            from tkinter import messagebox
            # Shows a warning message if a field is blank upon running
            messagebox.showinfo("Warning", "spot.csv path or output folder not"
                                           " selected! Or name not entered!")
        else:

            # Sets up a log in the chosen output folder to log any errors.
            logging.basicConfig(
                filename='%s/IMARIS_to_LAM.log' % self.__ofolder.get(),
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.INFO,
                datefmt='%d-%m-%Y %H:%M:%S')

            try:
                csv_path = str(self.__csv_folder.get())
                output_folder_path = str(self.__ofolder.get())
                spot = str(self.__name_input.get())
                self.__window.destroy()
                logging.info(
                    "Process started for %s" % spot)
                # Calls the csv_create function from the istl.py file which
                # should be in the same directory as this istl_RUN.py
                istl.csv_create(csv_path, output_folder_path, spot)
                logging.info(
                    "Process finished for %s" % spot)
            except Exception as e:
                logging.exception(str(e))

    def quit_func(self):

        self.__window.destroy()

    def start(self):

        self.__window.mainloop()


def main():
    ui = Imaris_to_lam()
    ui.start()


main()
