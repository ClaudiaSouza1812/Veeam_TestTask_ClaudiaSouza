# Folder Synchronization Program

A program that maintains a replica of a source folder, performing periodic one-way synchronization.

## Description

This tool synchronizes two folders by maintaining an exact copy of a source folder in a replica folder. All file operations (creation, copying, removal) are logged both to a file and console output.

## Features
- One-way folder synchronization
- Periodic updates at specified intervals
- Operation logging to file and console
- Support for nested folders
- File comparison using MD5 hashing

## Requirements
- Python 3.10+
- Standard library only

## Usage

```bash
python main.py source_folder replica_folder log_folder interval
```

Where:
- `source_folder`: Path to source directory
- `replica_folder`: Path to replica directory
- `log_folder`: Path to store log files
- `interval`: Time between syncs in seconds

Example:
```bash
python main.py ./Source_Folder ./Replica_Folder ./Log_File_Folder 60
```

## Implementation Details

The program consists of two main components:
- `main.py`: Handles command-line arguments and program initialization
- `folders_sync.py`: Contains the core synchronization logic

The synchronization process:
1. Scans source and replica folders
2. Identifies files to create, update, or remove
3. Performs necessary operations
4. Logs all actions
5. Waits for specified interval before next sync

## Project Structure

```
VEEAM_TESTTASK_CLA
├── src
│   ├── folders_sync.py
│   └── main.py
├── Log_File_Folder
│   └── sync_log_file.txt
├── Replica_Folder
│   └── test files
├── Source_Folder
│   └── test files
└── README.md
```

## Notes

- Log folder must be separate from source and replica folders
- Sync interval must be greater than 0
- Source and replica folders must exist and be different
- Program can be stopped with Ctrl+C

![Class_Diagram](https://github.com/user-attachments/assets/eee69025-f350-4451-98df-d6240c94a2c8)

    FoldersSync ..> Path : uses
    ArgumentParser ..> Path : validates
