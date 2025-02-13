from datetime import datetime
import time
from pathlib import Path
import shutil

class FoldersSync:
    
    LOG_FILE_NAME = "sync_log_file.txt"
    
    # Parameterized constructor
    def __init__(self, source_folder_path: str, replica_folder_path: str, log_file_path: str, sync_interval: int):
        self.source_folder_path = Path(source_folder_path)
        self.replica_folder_path = Path(replica_folder_path)
        self.log_file_path = Path(log_file_path) / self.LOG_FILE_NAME
        self.sync_interval = sync_interval
        
        
        
    def get_files(self, folder: Path) -> set[Path]:
        
        files_to_update = set()
        
        try:
            if not folder.exists():
                self.update_log_file(f"Folder not found: {folder}")
                return files_to_update
            
            for file in folder.rglob('*'):
                if file.is_file():
                    file_path = file.relative_to(folder)
                    files_to_update.add(file_path)
                    self.update_log_file(f"File found: \033[0m{file_path}")
        
            return files_to_update
        
        except Exception as error:
            self.update_log_file(f"Search folder error: {folder}: {str(error)}")
            return files_to_update
        
    
    
    def check_folders_files(self) -> tuple[set[Path], set[Path]] | None:
         
        self.update_log_file("Searching files in source folder")
        source_folder_files = self.get_files(self.source_folder_path)
        
        if not source_folder_files:
            self.update_log_file("Source folder is empty")
        
        self.update_log_file("Searching files in replica folder")
        replica_folder_files = self.get_files(self.replica_folder_path)
        
        if not replica_folder_files:
            self.update_log_file("Replica folder is empty")
            
        if not source_folder_files and not replica_folder_files:
            self.update_log_file("Both folders are empty. Nothing to synchronize")
            return None
        
        return source_folder_files, replica_folder_files
        
        
    
    def remove_files(self, files_to_delete: set[Path]) -> None:
        
        self.update_log_file("Looking for file to remove")
        
        if not files_to_delete:
            self.update_log_file(f"No files removed from the Source to performe a removal")
            return
        
        for file_path in files_to_delete:
            replica_file = self.replica_folder_path / file_path
            replica_file.unlink()
            self.update_log_file(f"Deleted: {file_path}")
    
        
        
    def update_files(self, files_to_create: set[Path], files_to_check: set[Path]) -> None:
        
        self.update_log_file("Creating/Updating files")
        
        for file_path in (files_to_create):
            source_file = self.source_folder_path / file_path
            replica_file = self.replica_folder_path / file_path
            
            replica_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, replica_file)
            self.update_log_file(f"Created: {file_path}")
        
        for file_path in files_to_check:
            source_file = self.source_folder_path / file_path
            replica_file = self.replica_folder_path / file_path
            
            if source_file.stat().st_mtime != replica_file.stat().st_mtime:
                replica_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, replica_file)
                self.update_log_file(f"Updated: {file_path}")
            else:
                self.update_log_file(f"The files don't have changes to perform an update")
            
            
        
    def update_log_file(self, message: str) -> None:
        
        log_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"\033[33m{log_date_time}:\033[0m \033[32m{message}\033[0m\n"
        print(log_message)
        
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.log_file_path, "a", encoding="utf-8") as file:
            file.write(log_message)
    
    
 
    def sync_folders(self) -> None:
        
        self.update_log_file("-----> New synchronization <-----")

        try:
            folders_files = self.check_folders_files()
            
            if folders_files is None:
                return
            
            source_folder_files, replica_folder_files = folders_files
            
            files_to_create = source_folder_files - replica_folder_files
            files_to_delete = replica_folder_files - source_folder_files
            files_to_check = source_folder_files & replica_folder_files
            
            self.remove_files(files_to_delete)
            self.update_files(files_to_create, files_to_check)
            
        except Exception as error:
            self.update_log_file(f"Error during synchronization: {str(error)}")  
            return 
        
        self.update_log_file("Synchronization completed successfully")
    
    
    
    def run_folders_sync(self) -> None:
        try:
            while True:
                self.sync_folders()
                time.sleep(self.sync_interval)
        except KeyboardInterrupt:
            self.update_log_file("Synchronization stopped by user")
        except Exception as error:
            self.update_log_file(f"Error: {str(error)}")
        