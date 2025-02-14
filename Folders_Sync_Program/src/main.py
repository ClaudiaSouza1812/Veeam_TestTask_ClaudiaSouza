"""
Command-line interface for the folder synchronization program.

This script provides a command-line interface to run folder synchronization,
handling argument parsing, input validation, and program execution.
"""

import argparse
from pathlib import Path
from folders_sync import FoldersSync


def define_input_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command-line argument parser.
    """
    
    input_parser = argparse.ArgumentParser(description="Folder Synchronization Program")
    input_parser.add_argument(dest="source_folder_path", type=Path, help="Path to Source Folder")
    input_parser.add_argument(dest="replica_folder_path", type=Path, help="Path to Replica Folder")
    input_parser.add_argument(dest="log_file_path", type=Path, help="Path to Log File Path")
    input_parser.add_argument(dest="sync_interval", type=int, help="Synchronization Interval in seconds")
    
    return input_parser



def check_folder_path(folder_path: str) -> bool:
    """
    Verify if a path exists and if it is a directory.
    """
    
    if not folder_path or folder_path.isspace():
        return False
    
    path_checker = Path(folder_path)
    
    return path_checker.exists() and path_checker.is_dir()



def validate_paths(user_inputs: argparse.Namespace) -> bool:
    """
    Validate paths and synch interval provided.
    1. Source folder exists
    2. Replica folder exists
    3. Source and replica folders are different
    4. Log file directory exists
    5. Log file is not in source or replica folders
    6. Sync interval is positive
    """
    
    if not check_folder_path(str(user_inputs.source_folder_path)):
        print("Error: Source Folder Path doesn't exist")
        return False
    
    if not check_folder_path(str(user_inputs.replica_folder_path)):
        print("Error: Replica Folder Path doesn't exist")
        return False
    
    if user_inputs.replica_folder_path == user_inputs.source_folder_path:
        print("Error: Replica and Source Folders cannot be the same")
        return False
    
    if not check_folder_path(str(user_inputs.log_file_path)):
        print("Error: Log File Path doesn't exist")
        return False
    
    if user_inputs.log_file_path == user_inputs.replica_folder_path or user_inputs.log_file_path == user_inputs.source_folder_path:
        print("Error: For safety, the Log File cannot be in the Source or Replica Folders, choose another Folder.")
        return False
    
    if user_inputs.sync_interval <= 0:
        print("Error: Interval Sync must be greater than 0.")
        return False
    
    return True



def main():
    """
    Start of the folder synchronization program.
    Receive command-line arguments, validates the inputs and starts the
    sync process if all good.
    """
    
    input_parser = define_input_parser()
    
    user_inputs = input_parser.parse_args()
    
    if not validate_paths(user_inputs):
        return
    
    sync_folders = FoldersSync(str(user_inputs.source_folder_path), str(user_inputs.replica_folder_path), str(user_inputs.log_file_path), user_inputs.sync_interval)
    sync_folders.run_folders_sync()
    
if __name__ == "__main__":
    main() 