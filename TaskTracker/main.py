"""
Task Data Tracker - Main Execution Entry Point.

This script initializes the Command Line Interface (CLI) for the tracking program.
It handles the main application loop, user input validation, and orchestrates 
file system operations (Year/Task/Month creation) by invoking the Executor 
and Generator classes.
"""

import os
import time
import msvcrt
import pandas as pd
from manager import Executor
from generating import Generator


# Short month names list for validation and creation
MONTH_NAMES_LIST = [
    'Jan', 'Feb', 'Mar', 'Apr', 
    'May', 'Jun', 'Jul', 'Aug', 
    'Sep', 'Oct', 'Nov', 'Dec']


# Create absolute path directly to user directory
USER_DIR = os.path.expanduser("~")

# Path of the Base folder in user directory
BASE_DIR = os.path.join ( USER_DIR,"Documents","TaskData")

# Path of the existing years  tracker file
YEARS_CSV = os.path.join(BASE_DIR, "years.csv")

# Initialize helper calsses:

# Folder/File generator
generator = Generator()
# Handling Executor
executor = Executor()

# Generate a Base Directory
generator.make_directory( BASE_DIR )
# Create File Of Existing years
generator.make_file( path= YEARS_CSV, header= ["years"] )

# Clear screen terminal 
def clear_terminal():
    """
    Clear the terminal screen based of the operating system."""
    os.system("clear" if os.name == "posix" else "cls")


# To pause the executions
def sleep(second:int):
    """
    Pauses execution for a specified number of seconds."""

    time.sleep(second)


def show_options():
    """
    ### Displays orgenized options to the user.

    Ruterns:
    -------
    int
        The total count of available options.
    """

    print("\n\n")
    options = [
        ["1. Create Base Year Directory", "2. Create Task Directory in Year", "3. Create Month File in Task"],

        ["4. Add Data in Month","5. View Data","6. Delete Data"],

        ["7. Analyze Data","8. Exit Program ❗"] ]

    print("=============================")
    print("        MAIN MENU")
    print("=============================")

    num = 0
    # Iterate through option groups
    for group in options:
        
        # Iterate through specific options within the group.
        for option in group:
            
            # Incresse 1 every itrate to num
            num += 1
            
            # View such option in the group 
            print(option)

        print("-----------------------------")

    print("=============================")

    return num # Return count of options

# --- Main Execution Loop ---

program_on = True

while program_on:
    
    # Reset screen for fresh menu view
    clear_terminal()

    # Display menu and get total option count
    options = show_options()

    # Capture user input
    get_choice = input(f"\n\nEnter your choice ( 1 - {options} ): ").strip()

    clear_terminal()

    # Ensure it si a digit and within range
    if not get_choice.isdigit() or int(get_choice) > options or get_choice == "0":

        print(f"\n\nInvalid entry: [ {get_choice} ]❗ Pelase enter ( 1 to {options} ).")

    # Ensure base directroy exists ( unless creating year or existing)
    elif not executor.count_dirs( BASE_DIR ) and int(get_choice) != 1 and int(get_choice) != 8:

        print("\n\nEnter first the start year❗\n")

    else:

        # Conver valid choice to (int)
        choice = int(get_choice)

        # Retrieve the most recently active year and setup paths
        last_year = executor.get_latst_active_name(filepath= YEARS_CSV)
        current_year = str(last_year)

        # Path of the current year dir
        year_dir = os.path.join(BASE_DIR,current_year)

        # Path of the exist tasks file
        tasks_csv = os.path.join(year_dir,"tasks.csv")

        # [ 1 ]
        if choice == 1: # Create New Year Directory

            # Get year to start 
            year = executor.get_year(years_path= YEARS_CSV) 

            # Check if year has string value
            if isinstance(year, str):

                new_year = os.path.join(BASE_DIR, year)
                tasks_report_csv = os.path.join(new_year, "tasks_report.csv")
                tasks_csv = os.path.join(new_year, "tasks.csv")

                # Create physical directories and tracker files
                generator.make_directory(path= new_year)
                generator.make_file(path= tasks_csv, header= ["tasks"])
                generator.make_file(path= tasks_report_csv, header= ["task","months","days","hours","minutes"])

                # Register the new year in the years tracker
                executor.store_data(file_path= YEARS_CSV, data_list= [year])

                print("-" * 30)
                print(f"\nYear directroy [ {year} ] is successful created into:\n")
                print(f"- Directory: {BASE_DIR}")


        # [ 2 ]
        elif choice == 2: # Create a Task Folder

            # Prompt user and create task folder
            folder_name = executor.get_folder_name( folder_names_csv= tasks_csv ) 
 
            # Check if the task name is returned
            if isinstance(folder_name, str):

                # Create directory paths safely
                target_path = os.path.join(year_dir, folder_name)    
                months_csv = os.path.join(year_dir, folder_name, "months.csv")
                task_report = os.path.join(year_dir, folder_name, "task_report.csv")

                # Execute creation and storage
                generator.make_directory(path=target_path)
                executor.store_data(file_path=tasks_csv, data_list=[folder_name])
                
                # Initialize month tracker and task report files
                generator.make_file(path= months_csv, header= ["months"])
                generator.make_file(path= task_report, header= ["month","days","hours","minutes"])

                print(f"Success: Folder '{folder_name}' created.")
                

# BEFOR MAKING A NEW MONTH ANALIZE THE DATA OF THE CURRENT ONE AND ADD IT TO THE task_report.csv FILE


        # [ 3 ]
        elif choice == 3: # Create Month File

            # Enuser tasks exist before adding months
            if executor.read_csv(file_path= tasks_csv).empty:

                print(f"\n\nCreate First A Task❗ \n")
                
            # Show message to get choice of the view content
            print("\n\nWhich Task Needs A New Month❓ ")

            # Display Tasks Folder Names
            print("=" * 30)
            executor.print_formatted_csv_table(file_path= tasks_csv)
            print("=" *30 )

            # Get Task Name
            folder_name = input("\nEnter task name from the top list:  ").strip().lower()

            clear_terminal()

            # Validate task existence
            if not executor.is_exist(file_path= tasks_csv, name= folder_name):

                print(f"\n\nTask [ {folder_name} ] is not found in the list❗\n")

                print("=" * 30)
                executor.print_formatted_csv_table(file_path= tasks_csv)
                print("=" *30 )

            else:

                # Setup paths for the specific task
                task_dir = os.path.join( BASE_DIR, current_year, folder_name )
                months_csv =  os.path.join( task_dir, "months.csv" )
                
                # List To Store The Header Of The existing Month
                csv_headers = []

                # Get user input for month name
                month = executor.get_month_name(months_list= MONTH_NAMES_LIST, months_path= months_csv)


                if isinstance( month, str):

                    # Setup path of the new month
                    new_month = os.path.join( task_dir, f"{month}.csv" )

                    # CASE A: No months exist yet (Fresh Task) -> Ask for custom headers
                    if executor.read_csv(months_csv).empty:     

                        # Get Header For The New File
                        print("\n\nWhich details should be included in the file (header)?")

                        get_header = input("\n\nEnter header names separated by commas: ").strip()


                        # Check if is there a digit contains in the entry
                        if [num for num in get_header if num.isdigit()]:

                            print("\n\nThe header can not contain digits.\n")
                                
                        # Check if the entry is empty
                        elif not get_header:
                            print("\n\nThe header list can't be empty.\n")

                        # Split input by comma to sotre in the file
                        csv_headers = [
                            name.strip()
                            for name in get_header.split(',') 
                        ]

                    # CASE B: Months exist -> Copy header from the previous month
                    else:

                        # Get an existing month name
                        last_month = executor.get_latst_active_name( months_csv )

                        exist_month = os.path.join( task_dir, f"{last_month}.csv" )

                        # Read only header (neows=0)
                        df = pd.read_csv( exist_month, nrows= 0) 

                        # Extend The Header to The List 
                        csv_headers.extend( df.columns.to_list() )
                        

                    # Create the file and register it
                    header_clean = [name.lower() for name in csv_headers]
                    generator.make_file(path= new_month, header= header_clean)
                    executor.store_data(file_path= months_csv, data_list= [month])

                    print(f"With CSV Header Row: {csv_headers}")
                    print("-" * 30)

                    print(f"\nNew month file: [ {month} ] is successfuly created into:\n")
                    print(f"- Directory: {task_dir}")


        # [ 4 ] 
        elif choice == 4: # Add data

            # Ensuer the existin of tasks
            if executor.read_csv(tasks_csv).empty:
                
                print("\n\nThere is no active tasks to add data.\n")

            else:
 
                # Display Tasks
                print("=" *30 )   
                executor.print_formatted_csv_table(tasks_csv)
                print("=" * 30)
            
                # Get number of task
                task_idx = input("\nEnter Task Number:  ").strip()

                clear_terminal()

                # Validate entry if it is numeric
                if executor.validate_inputs(entry= task_idx, entry_type= "int"):
                    
                    # Check Range validity
                    if int(task_idx) > len(executor.read_csv(tasks_csv)) or int(task_idx) < 1:

                        print(f"\n\nEntry: [ {task_idx} ] is out of range\n")

                    else:
                        
                        # get the task name dir
                        task_record = executor.read_csv(tasks_csv).iloc[ int(task_idx) -1 ]
                        task_dir_name = task_record.iloc[0]

                        # Setup Paths of the choiced task
                        task_path = os.path.join( BASE_DIR, current_year, task_dir_name )
                        months_csv = os.path.join( task_path, "months.csv")

                        # validate if the months exist to add data into
                        if not executor.read_csv(months_csv).empty:
                            
                            # breng the last active month file name
                            month_name = executor.get_latst_active_name( months_csv )
                            
                            month_file_path = os.path.join( task_path, f"{month_name}.csv")
                            
                            # Trigger data entry workflow
                            executor.get_data( file_path= month_file_path )

                        else:
                            print("\n\nNo Active Months To Add Data❗Please Add First A Month\n")
          

        # [ 5 ]
        elif choice == 5: # Display Content
            
            # Trigger data displaying workflow
            executor.navigate_and_display_data(BASE_DIR)


        # [ 6 ]
        elif choice == 6: # Delete content      

            # Trigger Deletion Data Workflow
            executor.remove_data(main_dir= BASE_DIR)


        # [ 8 ] 
        elif choice == 7: # Analyze data

            pass
            
        # [ 9 ]
        elif choice == 8: # Exit !!

            program_on = False


    # Pause until any key is pressed
    if get_choice != "8":

        print("\n" + "="*40)
        print("  👉 Press ANY KEY to return to menu...❗")
        print("="*40)

        msvcrt.getch()  # Wait for a single keypress


# ==========================================
# DEVELOPER NOTES & ROADMAP (TODO)
# ==========================================
# 1. [LOGIC]  Define data flow: task_task() <--> get_data().
# 2. [DONE]   Fixed path error in Display Content (Targeted year dir, not active file).
# 3. [DONE]   Fixed 'months_path' issue: Now calls series header then converts to list.
# 4. [DONE]   UI: Content display organized with separators.
# 5. [DONE]   Bugfix: Pre-generation header data extraction verified.
# 6. [DONE]   Bugfix: Resolved invalid month header error even when month name was correct.
# 7. [DONE]   Fix: accepted entry of the string data and integer.
# 8. [DONE]   Structure: New tasks must generate default files:
#             - 'months.csv' (Active months tracker)
#             - 'task_report.csv' (Analysis data).
#             - Required Header: [month_name, days, hours, minutes].
# ==========================================
