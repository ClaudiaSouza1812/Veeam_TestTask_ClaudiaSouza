import argparse
from pathlib import Path
from folders_sync import FoldersSync



def define_input_parser():
    
    input_parser = argparse.ArgumentParser(description="Folder Synchronization Program")
    input_parser.add_argument(dest="source_folder_path", type=Path, help="Path to Source Folder")
    input_parser.add_argument(dest="replica_folder_path", type=Path, help="Path to Replica Folder")
    input_parser.add_argument(dest="log_file_path", type=Path, help="Path to Log File Path")
    input_parser.add_argument(dest="sync_interval", type=int, help="Synchronization Interval in seconds")
    
    return input_parser



def check_folder_path(folder_path: str) -> bool:
    
    if not folder_path or folder_path.isspace():
        return False
    
    path_checker = Path(folder_path)
    
    return path_checker.exists() and path_checker.is_dir()



def validate_paths(user_inputs) -> bool:
    
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
    
    input_parser = define_input_parser()
    
    user_inputs = input_parser.parse_args()
    
    if not validate_paths(user_inputs):
        return
    
    sync_folders = FoldersSync(str(user_inputs.source_folder_path), str(user_inputs.replica_folder_path), str(user_inputs.log_file_path), user_inputs.sync_interval)
    sync_folders.run_folders_sync()
    
if __name__ == "__main__":
    main() 