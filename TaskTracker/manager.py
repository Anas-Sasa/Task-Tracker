"""
Manager Module
================

This module contains the `Executor` class, which handles the core logic for:
1. File system navigation (Directories/Files).
2. CSV read/write operations.
3. User input validation.
4. Data deletion and display workflows.
"""

import csv
import os
import shutil
import pandas
from pathlib import Path

class Executor():
    """
    Handles file system operations, CSV management, and user interaction flows.
    """

    def __init__(self):
        
        # Default starting year for suggestions
        self.default_year = 2026

    # Clear screen terminal 
    def clear_terminal(self):
        """
        Clears the terminal screen based on the operating system."""

        os.system("clear" if os.name == "posix" else "cls")


    # Read CSV files
    def read_csv(self, file_path):

        """
        ### Read csv-files and returns its content as a pandas DataFrame.
        
        :param file_path (str): The full path to the CSV file that should be loaded.

        Retruns
        ------
        pandas.DataFrame
            A DataFrame containing all rows and columns from the CSV file.
            All values are read as strings (dtype=str) to prevent unwanted
            type conversion, and no rows are skipped (skiprows=0).
        """
        return pandas.read_csv(file_path, dtype= str, skiprows= 0)
    

    # Count exist directories in the passed dir_path 
    def count_dirs(self,dir_path):
        """
        ### Counts the directories into the a directory using (pathlib) module.
        
        :param dir_path: 
            The full path of the directory that should be counted.

        Returns
        -------
        The number of subfolders inside dir_path.
        """
        # Count the folder in the directory
        return len([p for p in Path(dir_path).iterdir() if p.is_dir()])

        
    # Count exist files in dirs
    def count_files(self,dir_path):
        """
        Counts the number of files within a given path.

        Args:
            dir_path (str): The path to investigate.

        Returns:
            int: The count of files found.
        """

        count = 0

        # Create a Path object
        p = Path(dir_path)


        # Iterate through items and count only if it is a file
        for entry in p.iterdir():

            if entry.is_file():

                count += 1

        return count
    

    # Delete conten 
    def remove_data(self, main_dir):
        """
        Interactive menu to delete hierarchical data (Year, Task, Month, or Row).
        
        Prompts the user to select a scope for deletion and removes both the 
        physical file/directory and its corresponding entry in the CSV tracker.
        
        Parameters:
            main_dir (str): The base directory path containing the data structure.
            
        Returns:
            None: If the operation is canceled or input is invalid.
        """


        # Vliedat if main_dir has exist dir
        if not self.count_dirs(main_dir):
            print(f"\n\nNo active years are exist❗\n")
            return
        

        # Path of the year tracker file
        years_csv = os.path.join( main_dir, "years.csv" )

        # List of year names
        year_list_names = self.read_csv( years_csv )["years"].to_list()


        # Display Deletion Scope Options
        print("\n\nChoose the scope of data to delete:\n")

        options = [
            "1. Delete Year (removes all tasks and months)",
            "2. Delete Task (removes all months within the task)",
            "3. Delete Month or Specific data in it"
        ]

        print("\n".join(options))
        print("-" * 20)


        # Get Scope choice
        get_content_num = input("\n\nEnter choice number from the top list:  ").strip()

        self.clear_terminal()

        # Ensure the entry is numeric
        if not get_content_num.isdigit():

            print(f"\n\nInvalid entry: [ {get_content_num} ]. Only digits are accepted.\n")
            return

        # Convert the entry num to (int)
        sub_choice = int(get_content_num)

        # Validate Range Validity
        if sub_choice > len(options) or sub_choice < 1:

            print(f"\n\nEntry [ {get_content_num} ] is out of range. Valid range is 1 to {len(options)}\n")
            return


        # Select Year
        print("=" * 30)
        print("      Year directory(s)")
        print("=" * 30)
        self.print_formatted_csv_table(years_csv)

        # Show a warning message
        print("=" * 30)
        print("Warning❗\n\nThe data can not recovered after deletion❗")
        print("=" * 30)

        # Get a year name
        get_year = input("\n\nEnter a year from the top list: ").strip()

        # Reset terminal for Clarity
        self.clear_terminal()

        # Check if the year exist in the list names
        if get_year not in year_list_names:

            print(f"\n\nInvalid entry. Year [ {get_year} ] is not found\n")
            return
        

        # Path of the task names
        tasks_path = os.path.join(main_dir,get_year,"tasks.csv")

        # Dataframe of tasks
        tasks_file = self.read_csv(tasks_path)


        # [Option 1 ]
        if sub_choice == 1: #  Remove a year

            # Dataframe of the year names
            data = pandas.read_csv(years_csv, dtype= str)

            # Delete the entered year from the dataframe and update it
            update_file = data[data["years"] != get_year]
            
            # Make a new csv file after updating
            update_file.to_csv(years_csv, index=False) # Saves the update as csv_file

            year_dir = os.path.join(main_dir, get_year)

            # Remove the year dir
            shutil.rmtree( year_dir )
            
            # Show successful message
            print(f"\nRemoving year [ {get_year} ] was successful\n\n")

            return


        # Validate tasks exist for Options 2 & 3
        if tasks_file.empty:

            print("\n\nNo active tasks to delete. Please add a task first.\n")
            return

        # Select Task
        self.print_formatted_csv_table(tasks_path)
        print("-" * 20)

        get_task_idx = input("\nEnter task number from the top list to remove the choiced data:  ").strip()

        self.clear_terminal()

        # Ensure the entry is numeric
        if not self.validate_inputs(get_task_idx, "int"):

            return
        
        # Convert The Choice to (int)
        task_index = int( get_task_idx )

        # Validate Entry Range Validity
        if task_index > len (tasks_file) or task_index < 1 :

            print(f"\n\nEntry: [ {task_index} ] is out of range. Valid range is 1 to {len (tasks_file)}\n")
            return

        # Get the task name from the tasks tracker
        task_name = tasks_file["tasks"].iloc[ task_index - 1]


        # [Option 2 ]
        if sub_choice == 2: # Remove task dir
            
            # Delete the task name from the tasks tracker
            update_file = tasks_file[tasks_file["tasks"] != task_name]
            
            # Make new CSV file content after deletion
            update_file.to_csv(tasks_path, index=False) # Saves the new data to csv file

            # Setup The Paht of Dir
            task_dir = os.path.join( main_dir, get_year, task_name )

            # Remove task dir
            shutil.rmtree( task_dir )
            
            # Show successful message
            print(f"\nTask [ {task_name} ] removed successfully.\n")


        # [Option 3 ] 
        else: # Remove Month file or a specific data row in month

            
            # Display Score Options
            print("\n\nSelect the data you want to delete❗\n")

            print("1. Entire monthly file")
            print("2. Specific data row")
            print("-" * 30 )

            # Get number choice
            sub_choice = input("\n\nEnter a choice number: ").strip()

            # Clear terminal
            self.clear_terminal()

            # Check if the  entry in range
            if not sub_choice in [ "1", "2"]:

                print(f"'\n\nEentry [ {sub_choice} ] is not accepted❗\n")
                return

            # Path of the months file
            months_csv =  os.path.join( main_dir, get_year, task_name, "months.csv" )

            # Dataframe of the month names file
            months_file = self.read_csv(months_csv)


            # View the exist months in the file
            print(f"\n\n---[ {task_name} ]---")
            print("-" * 20)
            self.print_formatted_csv_table(months_csv)

            # Get month choice number
            get_month_idx = input("\n\nEnter month number from the top list:  ").strip()

            self.clear_terminal()

            # Validate if entry is numeric
            if not self.validate_inputs(get_month_idx, "int"):

                print(f"\n\nInvalid input [ { get_month_idx } ]. Enter only digits\n")
                return
            
            # Convert Choice to (int)
            month_index = int(get_month_idx)

            # Ensure that the entry is in range
            if month_index > len( months_file ) or month_index < 1:

                print(f"\n\nEntry [ {get_month_idx} ] is out of range❗Valid range is 1 to {len( months_file )}\n")
                return
            

            # Get month name from it's file
            month_name = months_file.months.iloc[ month_index - 1]

            # Path of the month
            current_month_path = os.path.join( main_dir, get_year, task_name, f"{month_name}.csv" )


            # [3.1] Delete entire month file
            if int(sub_choice) == 1: 

                if os.path.exists(current_month_path):

                    os.remove(current_month_path)
                    
                    # Delete the month name from the monthsfile
                    update_file = months_file[months_file.months != month_name]

                    # Generate the update months_file
                    update_file.to_csv(months_csv, index= False)

                    print(f"\n\nMonth [ {month_name} ] has been deleted🗑️\n")
                    return True
                
                else:
                    print(f"\n\nMonth [ {month_name} ] does not exist!\n")
                    return


            # [3.2] Delete specific row
            if int(sub_choice) == 2: 

                # Length of the file rows 
                file_len = len( self.read_csv(current_month_path))

                # Ensure Month has data
                if not file_len:

                    print(f"\n\nMonth [ {month_name} ] has no data. Add first activity❗")
                    return
                
                # View month data
                print(f"\n\n---[ {month_name} ]---")
                print("-" * 20)
                self.print_formatted_csv_table(current_month_path)
                print("-" * 30) 

                # Get Index number of the data row
                get_row_num = input("\nEnter a number of data row from the top list to delete:  ").strip()

                self.clear_terminal()

                # Validate if entry was digit
                if not self.validate_inputs(get_row_num, "int"):
                    return
                
                # Convert data type of entry from 'str' to 'int'
                row_index = int(get_row_num)

                # Validate Range Validity
                if row_index > file_len or row_index < 1:

                    print(f"\n\nEntry [ {get_row_num} ] is out of range. Valid range is 1 to {file_len}.\n")
                    return  
                
                # Read month file
                df = self.read_csv( current_month_path)
                
                # Row of the data as list to view it to the user
                row_data = df.iloc[ row_index - 1 ].to_list()
                
                # View list row data
                print(f"\nData: { row_data }")
                print("-" * 20)

                # Delete data row
                df = df.drop(row_index - 1)

                # Create a niew ver data fram witout the deleted data
                df.to_csv(current_month_path, index= False)

                # Show message that evrything was successful
                print("\nRow deleted successfully!\n")


    # Reads and displaying the csv file content
    def print_formatted_csv_table(self, file_path):
        """
        ### Reads a CSV and displays it as a formatted table with 1-based indexing.
        
        :param file_path: The path to the CSV file.

        Ruterns:
        --------
        None if the opertion invalid
        """

        # Read CSV and contan it it as dataframe
        data = pandas.read_csv(file_path, dtype= str ,skiprows= 0 )
        
        # Check if it has content
        if len(data) == 0:
            print(f"\n\nNo content to view. Add first content❗\n\n")
            return None
        
        # Start indexing from 1 for user friendliness
        data.index = pandas.RangeIndex(start= 1, stop= len(data) +1, step= 1) 

        # repeare the header to display it like a string
        header = data.columns.to_list()

        # Print the header of data
        print("\n\n" + ",".join(header).strip()+":" + "\n")

        # Print the data rows
        print(data.iloc[0::].to_string(header= False) + "\n\n")


    # Read CSV and Returns the name of the last index.
    def get_latst_active_name(self, filepath):
        """
        ### Retrieves the last entry name from a CSV file.
        
        :param filepath: Path to the CSV.

        Returns: 
        -------
        str: The name in the last row, or None if empty.
        """
        
        # Read the CSV
        df = pandas.read_csv(filepath, dtype=str, skiprows=0)
        
        # Check if dataframe is empty to prevent errors
        if df.empty:
            return None

        # Get the last row (Series)
        last_row = df.iloc[-1]

        # Get the first value from the row
        latest_name = last_row.iloc[0] 

        return latest_name # (str) value
    

    # Displaying all data of a folder/file
    def navigate_and_display_data(self, base_dir):
        """
        ### Displays the exist year, task folder names or contets of tasks(Months or Entries)

        Flow: Year -> Task -> Month/Entries.

        - Showing options to view
        - Get content choice
        - Checks entry 
        - If want display tasks or content (follow more process)
        - If want display year. Start displaying

        :param base_dir: Root directory of the data
        """
        
        # Path of the CSV years file
        years_csv =  os.path.join(base_dir, "years.csv")

        # Check if years path is exists
        if not os.path.exists(years_csv):

            print(f"\n\nNo years or tasks exist\n")
            return 
        

        # Read the years CSV
        years_file = self.read_csv(years_csv)


        # Ensure existence of years
        if not len(years_file):

            print("\n\nNo active years exist! Please add an active year first!")
            return 

        options = [
            "1. Years (top-level directories)",
            "2. Tasks (within a selected Year)",
            "3. Entries in Month (from month.csv)",
            "4. Months (within a selected Task)"]
    
        # Display The Scope Of The Options
        print("\n\nWhich content would you like to display?\n\n")

        print("\n".join(options))
        print("-" * 30)

        
        # Get a choice number of content
        get_content_num = input("\n\nEnter a number of the content to view:  ").strip()

        self.clear_terminal()

        # Check if entry in range
        if get_content_num not in ["1", "2", "3", "4"]:

            print(f"\nInvalid entry: [ {get_content_num} ]! Valid choice is 1 to {len(options)}\n")
            return 
        

        # [ 1 ]
        if get_content_num == "1": # View Years

            self.print_formatted_csv_table(file_path= years_csv)
            return

  
        # Select Year for options [2, 3, 4]
        self.print_formatted_csv_table(file_path= years_csv)
        print("Which year would you like to view content?\n")

        # Get year
        get_year = input("\nEnter a year from the top list:  ").strip()

        self.clear_terminal()

        # Check if year is exists
        if get_year not in years_file.years.to_list():

            print(f"\nEntry year: {get_year} does not exist\n")
            return


        # Full path of the entered year tasks
        tasks_csv = os.path.join( base_dir, get_year, "tasks.csv" )

        # Read tasks CSV
        tasks_file = self.read_csv(tasks_csv)


        # Check if tasks file has contint 
        if tasks_file.empty:

            print("\n\nThere is no tasks conten❗ Add a task first❗")
            return 


        # Display Tasks
        self.print_formatted_csv_table( tasks_csv )

        # [2] View Tasks (Done)
        if get_content_num == "2": # Get out of the function
            return


        # Select Taks for [3, 4]
        get_task_num = input("\nEnter the task number from the top list: ").strip()

        self.clear_terminal()

        # Ensure Entry is numeric
        if not get_task_num.isdigit():

            print(f"\n\nUnaccepted entry: [ {get_task_num} ]❗Enter only digits.\n")
            return 
        

        # Convert the data type of entry number to (int)
        task_num = int(get_task_num)


        # Check if the number in range
        if task_num > len(tasks_file) or task_num == 0:

            print(f"\n\nChoice: {task_num} is out of range\n\n")
            return 


        # Task name
        task_name =  tasks_file.iloc[task_num - 1].iloc[0]

        # Full path of the task folder
        task_dir = os.path.join( base_dir, get_year, task_name )

        # Check if task has active month files
        if self.count_files(task_dir) < 3: # < 3 because dir has 2 default files (months.csv, report.csv)

            print(f"\n\nTask: [ { task_name} ] has no acitve months yet❗ Please start an active month first.\n\n")
            return 

        # Months path CSV
        months_csv = os.path.join( task_dir, "months.csv" )

        # List of the exists months
        months_list = self.read_csv(file_path= months_csv)["months"].to_list()

        # [3] View specific month entries
        if get_content_num == "3":
            
            # View the exists months
            self.print_formatted_csv_table( months_csv )

            # Get the month name
            get_month = input("\n\nEnter a month name from the top list:  ").strip().capitalize()

            self.clear_terminal()

            # Check if the name correct/exists
            if get_month not in months_list:

                print(f"\n\nIncorrect month name: [ {get_month} ]\n")
                return 
            
            # View data of the choiced month
            print(f"\n\n--- Task: {task_name} / Month: {get_month} ---\n")
            self.print_formatted_csv_table(file_path= os.path.join(task_dir, f"{get_month}.csv"))
        
        # [4] View All Months Data
        if get_content_num == "4": 
            
            # View the choiced task name
            print(f"\n\n")
            print(f"=" * 50)
            print(" " * 15,f"Task: {task_name}")
            print(f"=" * 50)

            print("\nExist Month(s):")
            # Display content for all months sequentially
            for month in months_list:
                    
                this_month = os.path.join( task_dir, f"{month}.csv" )
                
                if not os.path.exists(this_month):
                    return None
                
                else:

                    print("-" * 50)

                    print(f"{month}:")

                    print("-" * 50)
                    
                    self.print_formatted_csv_table( this_month )

            print(f"=" * 50)


    # Check if the entry name is exist in the passed path_file
    def is_exist(self, file_path: str, name:str):
        """
        ### Checks if a specific name exists within a CSV file.

        :param file_path: Full CSV path.
        :param name: The name to search for.

        Ruterns:
        --------
            bool: True if found. False Otherwise
        """

        data = pandas.read_csv(file_path, dtype= str).to_dict()

        for key in data: # key = header item

            for i in data[key]: # data[key] = int(index) of such row 

                if name == data[key][i]: # data[key][i] = item in the index key

                    return True

        return False
    

    # Saves data in the passed CSV file
    def store_data(self, file_path, data_list):
        """
        ### Appends a list of data as a row to a CSV file.
     
        :param file_path: Target CSV file.
        :param data_list: Data to append.
        """
        
        with open( file_path, "a", newline= "") as f:

            # set marker(pointer) at the end of file and reset it to the start
            f.seek(0, 2) # 2 get the end of file (0, 2), 1 stay currect postion (0, 1), 0 set to start (0, 0)

            # Write data in the file
            csv.writer(f).writerow(data_list)
            
            # View details of the storged data
            print(f"\nEntry(s): {data_list} successfully stored into:\n")
            print(f"- File: {file_path}\n")
        

    # Inputs validation
    def validate_inputs(self, entry, entry_type:str):
        """
        ### Validates user input based on expected type.

        :param entry: The user input.
        :param entry_type (str): Expected type ("int", "time", "str").

        Ruterns:
        -------
            bool: True if valid. False Otherwise
        """
        if not entry:

            print(f"\nEntry [ {entry} ] can not be empty❗\n")
            return False
  
        # Validate Interger
        if entry_type == "int":
    
            for num in entry:
        
                if num.isdigit() or num in [".", " ", "-"]:
                    continue

                else:
                    print(f"\n\nInvalid Entry [ { num } ]. Only digits are accepted\n")
                    return False
                

        # Validate Time (Simple heuristic: digits or colon)
        if entry_type == "time":

            for char in entry:

                if char.isdigit() or char == ":":
                    continue

                else:
                    print(f"\n\nInvalid duration: [ {entry} ]❗ Use format H:MM or MM\n\n")
                    return False
                    
        # Validate String ( Alpha or Spaces)
        if entry_type == "str":

            for content in entry:

                if content.isalpha() or content.isdigit() or content in [ " ", "_", "@", "."]:
                    continue

                else:
                    print(f"\n\nInvalid entry: [ {entry} ]❗ Only characters accepted.\n\n")
                    return False
                
        return True


    # Get a new year dir name
    def get_year(self, years_path):
        """
        ### Suggests and validates a new year directory name.

        - Prompts the user for a year name based on the last active year. 
        - Validates that the input is a digit and does not already exist 
        in the registry.

        :param years_path (str): Path to years.csv

        Returns:
            str: The validated year name if successful.
            None: If the input is invalid or already exists.
        """


        # Get the last active year number name as (str)
        recommend_year = self.get_latst_active_name(years_path)

        # Check if is there an exist year
        if recommend_year:
            
            # View recommended year + 1 to be like the current year number
            print(f"\n- Recommended year: [ {int(recommend_year) + 1} ]")

            # Update the defaulte year number
            self.default_year = int(recommend_year) + 1

        else:
            # Show the defaulte year number as example
            print(f"\nPlease enter a year (e.g., {self.default_year}).")


        # Get year 
        get_year = input("\n\nEnter a year:  ").strip()

        self.clear_terminal()

        # Ensure The Year Not Older Than the Currentlly one.
        if not get_year.isdigit() or int(get_year) < self.default_year:

            # View an error 
            print(f"\n\nInvalid entry: [ {get_year} ], (Format: {self.default_year})❗")
            return
      
        # Check if year is already exists
        elif get_year in self.read_csv( years_path )["years"].to_list():

            # Clear terminal
            self.clear_terminal()
    
            print(f"\n\nYear: [ {get_year} ] already exists❗")
            return

        return get_year # Return the str(year name)


    # Get a new month file name
    def get_month_name(self, months_list: list, months_path: str):
        """
        ### Prompts for a new month name and validates uniqueness.

        :param months_list: Standard list of month names.
        :param months_path: Path to the existing months CSV.

        Ruterns: 
        --------
            None: If operation failure, otherwise Month name.
        """
    
        # prepare list to display
        months_str = " __ ".join(months_list) 

        # Select Month
        print(f"\n\n{months_str}\n")
        print( "-" * 30)

        print(f"\n\nSelect a month name from the top list❗")

        # Aks month name
        get_month = input("\n\nEnter month:  ").strip().capitalize()

        self.clear_terminal()

        # Check if entry is not in months list
        if get_month not in months_list:

            # Show an error message
            print(f"\nEntry Month [ {get_month} ] Not Found in the List❗\n")
            print(months_str)
            return None
  
        # Check if the month name is already used
        if self.is_exist(months_path, get_month):
            
            print(f"Month: [ {get_month} ] already exist❗")
            return None

        return get_month


    # Create task folder
    def get_folder_name(self, folder_names_csv: str):
        """
        ### Creates a new task folder and registers it.

        :param folder_names_csv (str): Path to tasks.csv Tracker.

        Returns:
            None: If operation failure, otherwise Folder name.
        """

        # Get and clean input
        folder_name = input("\nEnter folder name: ").strip().lower()

        self.clear_terminal()

        # Validate Entry in empty
        if not folder_name:

            print("Folder name cannot be empty.")
            return None
        
        # Validate DataType of input
        if not self.validate_inputs(entry=folder_name, entry_type="str"):
            return None

        # Check Duplicate Of Entry
        if self.is_exist( file_path=folder_names_csv, name=folder_name ):

            print(f"Task '{folder_name}' already exists in registry!")

            self.print_formatted_csv_table(file_path=folder_names_csv)
            return None


        return folder_name
            


    # Geting data as recorded in the existing header
    def get_data(self, file_path: str):
        """
        ### Interactive loop to get row data corresponding to a CSV header.
        ### Validates input types (int/time/str) dynamically and stores valid rows.
   
        :param file_path: Path to the CSV file to append data to.
        """
 
        # List of the file header
        header = list(pandas.read_csv(file_path).columns)

        # List to apped the new data
        row_entries = []

        # Iterate through required columns
        for col_name in header:

            self.clear_terminal()
            get_entry = input(f"\n\nEnter {col_name}:  ").strip()

            if not get_entry:
                print("You forgot to enter data!\n")
                return None
            
            # Auto-detect type based on first character/format
            current_type = "str"

            for char in get_entry:

                if char.isdigit():
                    current_type = "int"
                
                if ":" in get_entry:
                    current_type = "time"

                break

            if self.validate_inputs(entry= get_entry, entry_type= current_type):

                row_entries.append(get_entry)
            else:
                print(f"Validation failed for {col_name}\n\n")
                return None
        
        if len(row_entries) == len(header):
            self.store_data(file_path= file_path, data_list= row_entries)

