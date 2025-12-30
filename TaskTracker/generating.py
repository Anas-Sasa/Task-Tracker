"""
### This module contains a generator class used to create new files/directories.

- Using the operating system(OS) and (csv) module.

The class contains the next methods:

1. make_directory(): Creates Directories
2. make_file():  Creates Files
"""

import os
from csv import writer

# Files & Folders gneratorf
class Generator():
    """
    A generator of files/directories"""

    def __init__(self):
        pass
        

    def make_directory(self, path):
        """
        ### Makes directory using OS.
        - Checks if the directory exist.
        
        :param path: Path of the Main Directory
        """

        # Create directory
        os.makedirs(path, exist_ok= True)

               
    def make_file(self, path, header:list):
        """
        
        - Checks The Existing of file. 
        - Creates File
        - Writes The Header 
        
        :param path: Full path location of the new file
        :type header: list
        """
        
        # Check if file is exist then make it
        if not os.path.exists(path= path):

            with open(path, "a", newline= "") as f:

                f.seek(0, 2)
                writer(f).writerow(header)

