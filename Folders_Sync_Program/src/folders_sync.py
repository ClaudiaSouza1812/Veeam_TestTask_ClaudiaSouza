"""
Dedicated class to one-way folders synchronization.

A class that maintains an identical copy of a source folder in a replica folder,
performing periodic synchronization and logging all operations.

Properties:
    source_folder_path (Path): Path to the source folder
    replica_folder_path (Path): Path to the replica folder
    log_file_path (Path): Path to the log file
    sync_interval (int): Interval between synchronizations in seconds   
"""
    
from datetime import datetime
import time
from pathlib import Path
import shutil
import hashlib
import re

class FoldersSync:
    
    LOG_FILE_NAME = "sync_log_file.txt"
    
    
    def __init__(self, source_folder_path: str, replica_folder_path: str, log_file_path: str, sync_interval: int):
        """
        Initialize a new FoldersSync instance.
        """
        
        self.source_folder_path = Path(source_folder_path)
        self.replica_folder_path = Path(replica_folder_path)
        self.log_file_path = Path(log_file_path) / self.LOG_FILE_NAME
        self.sync_interval = sync_interval
        
        
    
    def get_files(self, folder: Path) -> set[Path]:
        """
        Scan a folder and return all files found within it.    
        Raises:
            OSError: If there are errors
        """
        
        files_to_update = set()
        
        try:
            if not folder.exists():
                self.update_log_file(f"Folder not found: {folder}")
                return files_to_update
            
            for file in folder.rglob('*'):
                if file.is_file():
                    file_path = file.relative_to(folder)
                    files_to_update.add(file_path)
            
            if files_to_update:
                files_list = ", ".join(sorted(str(file) for file in files_to_update))
                self.update_log_file(f"Files found: \033[0m{files_list}")
            
            return files_to_update
        
        except Exception as error:
            self.update_log_file(f"Search folder error: {folder}: {str(error)}")
            return files_to_update
        
    
    
    def check_folders_files(self) -> tuple[set[Path], set[Path]] | None:
        """
        Scans both the source and replica folders to determine which files
        need to be created, updated, or deleted in the replica folder.
        """
        
        self.update_log_file("Searching files in Source folder")
        source_folder_files = self.get_files(self.source_folder_path)
        
        if not source_folder_files:
            self.update_log_file("Source folder is empty")
        
        self.update_log_file("Searching files in Replica folder")
        replica_folder_files = self.get_files(self.replica_folder_path)
        
        if not replica_folder_files:
            self.update_log_file("Replica folder is empty")
            
        if not source_folder_files and not replica_folder_files:
            self.update_log_file("Both folders are empty, nothing to synchronize")
            return None
        
        return source_folder_files, replica_folder_files
        
        
    
    def run_folders_sync(self) -> None:
        """
        Runs an infinite loop that performs synchronization at specified intervals.
        The process can be stopped with a keyboard interrupt (Ctrl+C).
        Raises:
            KeyboardInterrupt: When the user stops the synchronization
            Exception: For any other errors 
        """
        
        try:
            while True:
                self.sync_folders()
                time.sleep(self.sync_interval)
        except KeyboardInterrupt:
            self.update_log_file("Synchronization stopped by user")
        except Exception as error:
            self.update_log_file(f"Error: {str(error)}")
            
    
    
    def sync_folders(self) -> None:
        """
        Perform one complete synchronization cycle.
        1. Compares files between source and replica folders
        2. Removes files from replica that don't exist in source
        3. Creates new files and updates modified ones in replica
        4. Logs all operations and shows a summary
        The synchronization is one-way: changes in the source folder are
        made in the replica folder too, but not the opposite.
        """
        
        self.update_log_file("\033[32m------->\033[33m New synchronization \033[32m<-------\033[33m")

        try:
            folders_files = self.check_folders_files()
            
            if folders_files is None:
                return
            
            source_folder_files, replica_folder_files = folders_files
            
            files_to_create = source_folder_files - replica_folder_files
            files_to_delete = replica_folder_files - source_folder_files
            files_to_check = source_folder_files & replica_folder_files
            
            removed_files = self.remove_files(files_to_delete)
            updated_files = self.update_files(files_to_create, files_to_check)
            
        except Exception as error:
            self.update_log_file(f"Error during synchronization: {str(error)}")  
            return 
        
        self.show_sync_result(removed_files, updated_files)
        self.update_log_file("Synchronization completed successfully.")
    
            
            
    def remove_files(self, files_to_delete: set[Path]) -> int:
        """
        Remove files from the replica folder that don't exist in the source.
        Returns:
            int: Number of files deleted
        Raises:
            OSError: If there are errors
        """
        
        self.update_log_file("Looking for files to remove")
        
        if not files_to_delete:
            return 0
        
        for file_path in files_to_delete:
            replica_file = self.replica_folder_path / file_path
            replica_file.unlink()
            self.update_log_file(f"Deleted: \033[0m{file_path}")

        return len(files_to_delete)
        
    
    
    def update_files(self, files_to_create: set[Path], files_to_check: set[Path]) -> dict[str, int]:
        """
        Create new files and update modified ones in the replica folder.
        Raises:
            OSError: If there are errors
            shutil.Error: If there are errors during file copying
        """
        
        self.update_log_file("Creating / Updating files")
        
        updated_files = {
            "files_created": 0,
            "files_updated": 0
        }
        
        for file_path in (files_to_create):
            source_file = self.source_folder_path / file_path
            replica_file = self.replica_folder_path / file_path
            
            replica_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, replica_file)
            self.update_log_file(f"Created: \033[0m{file_path}")
            updated_files["files_created"] += 1
        
        for file_path in files_to_check:
            source_file = self.source_folder_path / file_path
            replica_file = self.replica_folder_path / file_path
            
            if self.create_hash_file(source_file) != self.create_hash_file(replica_file):
                replica_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, replica_file)
                self.update_log_file(f"Updated: \033[0m{file_path}")
                updated_files["files_updated"] += 1
            
        return updated_files
    
    
    
    def create_hash_file(self, file_path: Path) -> str:
        """
        Generate hash of a file.
        Returns:
            str: Hexadecimal string of file's MD5 hash
        Raises:
            OSError: If there are issues reading the file
        """
        
        hash_file = hashlib.md5()
        
        with open(file_path, "rb") as file:
            
            file_piece = file.read(8192)
            
            while file_piece:
                hash_file.update(file_piece)
                file_piece = file.read(8192)
        
        return hash_file.hexdigest()
        
        
        
    def update_log_file(self, message: str) -> None:
        """
        Write a message to both console and log file.
        The console output has color formatting for better user experience.
        Raises:
            OSError: If there are issues writing to the log file
        """
        
        log_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"\033[33m{log_date_time}:\033[0m \033[32m{message}\033[0m\n"
        print(log_message)
        
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        clean_message = re.compile(r"\033\[[0-9;]*[mGKH]")
        
        with open(self.log_file_path, "a", encoding="utf-8") as file:
            file.write(clean_message.sub("", log_message))
    
    
 
    def show_sync_result(self, removed_files: int, updated_files: dict[str, int]) -> None:
        """
        Display and log a summary of the synchronization.
        """
        
        sync_summary = {
            "files_created": updated_files["files_created"],
            "files_updated": updated_files["files_updated"],
            "files_removed": removed_files
        }
        
        self.update_log_file("\033[32m----->\033[33m Synchronization Summary \033[32m<-----\033[33m")
        self.update_log_file(f"Files created: {sync_summary['files_created']}")
        self.update_log_file(f"Files updated: {sync_summary['files_updated']}")
        self.update_log_file(f"Files removed: {sync_summary['files_removed']}")