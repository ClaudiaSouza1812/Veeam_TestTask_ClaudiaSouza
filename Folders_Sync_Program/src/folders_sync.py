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
                    self.update_log_file(f"File founded: {file_path}")
        
            return files_to_update
        
        except Exception as error:
            self.update_log_file(f"Search folder error: {folder}: {str(error)}")
            return files_to_update
        
        
        
    def update_log_file(self, message: str) -> None:
        
        log_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{log_date_time}: {message}\n"
        print(log_message)
        
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.log_file_path, "a", encoding="utf-8") as file:
            file.write(log_message)
    
    

        
    def sync_folders(self) -> None:
        
        self.update_log_file("New synchronization")

        try:
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
                return
            
            files_to_create = source_folder_files - replica_folder_files
            files_to_delete = replica_folder_files - source_folder_files
            files_to_ckeck = source_folder_files & replica_folder_files
            
            self.update_log_file("Removing files that don't exist in source")
            for file_path in files_to_delete:
                replica_file = self.replica_folder_path / file_path
                replica_file.unlink()
                self.update_log_file(f"Deleted: {file_path}")
                
            self.update_log_file("Creating/Updating files")
            for file_path in (files_to_create | files_to_ckeck):
                source_file = self.source_folder_path / file_path
                replica_file = self.replica_folder_path / file_path
                
                replica_file.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(source_file, replica_file)
                
                update_action = str()
                
                if file_path in files_to_create:
                    update_action = "Created"
                else:
                    update_action = "Updated"
                    
                self.update_log_file(f"{update_action}: {file_path}")
            
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
        