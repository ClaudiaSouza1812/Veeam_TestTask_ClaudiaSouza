from pathlib import Path
import os

def run_program() -> None:
    
    show_instructions()
    source_folder_path = get_source_folder()
    
    if not source_folder_path:
        return
    
    # stooped here!
    source_replica_folders_path = get_replica_folder(source_folder_path)
    get_sync_interval()
    return


def show_instructions():
    
    show_message("welcome")
    show_message("instructions")
    pause_console()



def get_user_choice() -> bool:
    
    while True:
        user_start_answer = input("\n\033[32mDo you want to continue? \n\nType \033[37m\"y\"\033[32m to proceed or \033[37m\"n\"\033[32m to close the program: \033[0m").strip()
        
        if user_start_answer == "y":
            return True
        elif user_start_answer == "n":
            print("\n\033[32mSee you next time!\033[0m\n")
            return False
        else:
            clean_console()
            print("\033[32mInvalid input. Please type 'y' or 'n'.\033[0m")
    
    
    
def get_source_folder() -> str | None:
    
    while True:
        
        source_folder_path = input("\n\033[32mEnter the Source Folder Path: \033[0m").strip()
        
        if verify_folder_path(source_folder_path):
            return source_folder_path        
        else:
            print("\033[32mSource Folder path inexistent or invalid.")
            if not get_user_choice():
                return None
            else:
                clean_console()
                show_instructions()
                
        
    
def get_replica_folder(source_folder_path: str) -> tuple[str, str] | None:
    
    while True:
        
        replica_folder_path = input("\n\033[32mEnter the Replica Folder Path: \033[0m").strip()
        
        if replica_folder_path != source_folder_path and verify_folder_path(replica_folder_path):
            return source_folder_path, replica_folder_path
        else:
            print("\033[32mReplica Folder path same as Source Folder, inexistent or invalid.")
            if not get_user_choice():
                return None
            else:
                clean_console()
                show_instructions()
                
        
    
    
def get_log_folder(source_replica_paths: tuple[str, str]) -> str | None:
    
    source_folder_path, replica_folder_path = source_replica_paths
    
    while True:
        
        log_file_path = input("\n\033[32mEnter the Replica Folder Path: \033[0m").strip()
        
        if log_file_path != source_folder_path and log_file_path != replica_folder_path:
            if verify_folder_path(log_file_path):
                return log_file_path
        else:
            print("\033[32mLog File folder path same as Source/Replica Folder, inexistent or invalid.")
            if not get_user_choice():
                return None
            else:
                clean_console()
                show_instructions()
        
        
    

def verify_folder_path(folder_path: str) -> bool:
    
    if not folder_path or folder_path.isspace():
        return False
    
    path_checker = Path(folder_path)
    
    return path_checker.exists() and path_checker.is_dir()
    
    
    
def get_sync_interval():
    
    sync_interval = input("\n\033[32mEnter the Synchronization Interval: ").strip()



def clean_console() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")



def show_message(message: str) -> None:
    
    separator = "-" * 100
    title = "Welcome to your Personal Folders Sync Manager"
    pad_right_title = title.rjust(10, " ")
    
    match message:
        case "welcome":
            print(f"\033[32m\n{separator}\n{title.center(len(separator))}\n{separator}\n\033[0m")
        case "instructions":
            print("\033[32mYou will be asked to enter:\n\n\t--> the Source Folder Path, ex:\n\t\t/source_path/source_path/source_folder_name\n\n\t--> the Replica Folder Path, ex:\n\t\t/replica_path/replica_path/replica_folder_name\n\n\t--> the Log File Path, ex:\n\t\t/log_path/log_path/log_file_path_name\n\n\t--> the Synchronization Interval Time or Day(s) with one (1) digit and one (1) letter:\n\t\t(h) for hours\n\t\t(d) for days\n\tex:\n\t\t1h (1 hour) \n\t\t1d (1 day)\033[0m")
        case "extensions":
            print("\033[32m--> The valid extensions are: ")
        


def pause_console() -> None:
    
    input("\n\033[32mPress any key to continue. \033[0m")
    


def main():

    run_program()
    
    
    
if __name__ == "__main__":
    main() 

