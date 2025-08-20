import os
import re
import json
from datetime import datetime

def get_old_new_files(directory_path):
    """
    Identifies the two most recent JSON files in a given directory based on their timestamps in the filename.
    Assumes filenames are in the format: api-docs-<project>-data-YYYY-MM-DD_HH-MM-SS.json
    Returns (old_file_path, new_file_path) or (None, None) if not enough files.
    """
    file_pattern = re.compile(r'api-docs-.*-data-(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json')
    
    files_with_timestamps = []
    for filename in os.listdir(directory_path):
        match = file_pattern.match(filename)
        if match:
            timestamp_str = match.group(1)
            try:
                # Parse timestamp from filename
                dt_object = datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
                files_with_timestamps.append((dt_object, os.path.join(directory_path, filename)))
            except ValueError:
                # Ignore files with malformed timestamps
                continue
    
    # Sort files by timestamp (oldest first)
    files_with_timestamps.sort(key=lambda x: x[0])
    
    if len(files_with_timestamps) >= 2:
        old_file = files_with_timestamps[-2][1]
        new_file = files_with_timestamps[-1][1]
        return old_file, new_file
    elif len(files_with_timestamps) == 1:
        print(f"Aviso: Apenas um arquivo encontrado em {directory_path}. Não é possível comparar.")
        return None, None
    else:
        print(f"Aviso: Nenhum arquivo JSON compatível encontrado em {directory_path}.")
        return None, None

def extract_endpoints(json_content):
    """
    Parses JSON content and extracts endpoint paths from the 'paths' key.
    Returns a list of endpoint strings.
    """
    try:
        data = json.loads(json_content)
        if 'paths' in data and isinstance(data['paths'], dict):
            return list(data['paths'].keys())
        return []
    except json.JSONDecodeError:
        print("Erro: Conteúdo JSON inválido.")
        return []

def compare_endpoints(old_endpoints, new_endpoints):
    """
    Compares two lists of endpoints and returns endpoints present in new_endpoints but not in old_endpoints.
    """
    old_set = set(old_endpoints)
    new_set = set(new_endpoints)
    return list(new_set - old_set)

def delete_oldest_file(directory_path):
    """
    Deletes the oldest JSON file in a given directory if there are more than two files.
    Assumes filenames are in the format: api-docs-<project>-data-YYYY-MM-DD_HH-MM-SS.json
    """
    file_pattern = re.compile(r'api-docs-.*-data-(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json')
    
    files_with_timestamps = []
    for filename in os.listdir(directory_path):
        match = file_pattern.match(filename)
        if match:
            timestamp_str = match.group(1)
            try:
                dt_object = datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
                files_with_timestamps.append((dt_object, os.path.join(directory_path, filename)))
            except ValueError:
                continue
    
    # Sort files by timestamp (oldest first)
    files_with_timestamps.sort(key=lambda x: x[0])
    
    if len(files_with_timestamps) > 2:
        file_to_delete = files_with_timestamps[0][1] # The oldest file
        try:
            os.remove(file_to_delete)
            print(f"Arquivo antigo deletado: {os.path.basename(file_to_delete)}")
        except OSError as e:
            print(f"Erro ao deletar o arquivo {os.path.basename(file_to_delete)}: {e}")
