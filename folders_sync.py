from pathlib import Path
import os

def run_program() -> None:
    
    show_menu()



def show_menu() -> None:
    
    show_message("welcome")
    show_message("instructions")
    pause_console()
    
    if get_folder_path():
        get_sync_interval()
    
    return
    
    
    
def get_user_choice() -> bool:
    
    while True:
        user_start_answer = input("\n\033[32mDo you want to continue? \n\nType \033[37m\"y\"\033[32m to proceed or \033[37m\"n\"\033[32m to close the program: \033[0m")
        
        if user_start_answer == "y":
            return True
        elif user_start_answer == "n":
            print("\n\033[32mSee you next time!\033[0m\n")
            return False
        else:
            clean_console()
            print("\033[32mInvalid input. Please type 'y' or 'n'.\033[0m")
    
    
    
def get_folder_path() -> bool:
    
    user_choice = True
    
    while user_choice:
        
        source_folder_path = input("\n\033[32mEnter the Source Folder Path: \033[0m")
        
        if verify_folder_path(source_folder_path):
            
            while user_choice:
                
                replica_folder_path = input("\n\033[32mEnter the Replica Folder Path: \033[0m")
                
                if replica_folder_path != source_folder_path and verify_folder_path(replica_folder_path):
                    return True
                else:
                    print("\033[32mReplica Folder path same as Source Folder, inexistent or invalid.")
                    user_choice = get_user_choice()
                    if not user_choice:
                        return False
                if user_choice:
                    clean_console()
                
        else:
            print("\033[32mSource Folder path inexistent or invalid.")
            user_choice = get_user_choice()
            if not user_choice:
                return False
            
        if user_choice:
            clean_console()
            show_menu()
        return False
    

    
def verify_folder_path(folder_path: str) -> bool:
    
    if not folder_path or folder_path.isspace():
        return False
    
    path_checker = Path(folder_path)
    
    return path_checker.exists() and path_checker.is_dir()
    
    
    
def get_sync_interval():
    
    sync_interval = input("\n\033[32mEnter the Synchronization Interval: ")



def clean_console() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")



def show_message(message: str) -> None:
    
    separator = "---------------------------------------------"
    match message:
        case "welcome":
            print(f"\033[32m\n{separator}\nWelcome to your Personal Folders Sync Manager\n{separator}\n\033[0m")
        case "instructions":
            print("\033[32mYou will be asked to enter:\n\t--> the Source Folder Path, ex:\n\t\tsource_path/source_path/source_folder_name\n\n\t--> the Replica Folder Path, ex:\n\t\treplica_path/replica_path/replica_folder_name\n\n\t--> the Synchronization Interval Time or Day(s) with one (1) digit and one (1) letter:\n\t\t(h) for hours\n\t\t(d) for days\n\tex:\n\t\t1h (1 hour) \n\t\t1d (1 day)\033[0m")
        case "extensions":
            print("\033[32m--> The valid extensions are: ")
        


def pause_console() -> None:
    
    input("\n\033[32mPress any key to continue. \033[0m")
    


def main():

    run_program()
    
    
    
if __name__ == "__main__":
    main() 

