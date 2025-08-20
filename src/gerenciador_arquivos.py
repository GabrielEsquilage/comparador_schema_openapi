import os
import re
from datetime import datetime

def _get_sorted_files(directory_path):
    """
    Returns a list of JSON files sorted by timestamp in their filenames.
    """
    file_pattern = re.compile(r'api-docs-.*-data-(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})\.json')
    files_with_timestamps = []
    try:
        filenames = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"Aviso: Diretório não encontrado: {directory_path}")
        return [] # Return empty list if directory doesn't exist

    for filename in filenames:
        match = file_pattern.match(filename)
        if match:
            timestamp_str = match.group(1)
            try:
                dt_object = datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
                files_with_timestamps.append((dt_object, os.path.join(directory_path, filename)))
            except ValueError:
                continue
    
    files_with_timestamps.sort(key=lambda x: x[0])
    return [file_path for dt, file_path in files_with_timestamps]

def get_latest_files(directory_path):
    """
    Identifies the two most recent JSON files in a given directory.
    Returns (old_file_path, new_file_path) or (None, None).
    """
    sorted_files = _get_sorted_files(directory_path)
    
    if len(sorted_files) >= 2:
        return sorted_files[-2], sorted_files[-1]
    elif len(sorted_files) == 1:
        print(f"Aviso: Apenas um arquivo encontrado em {directory_path}. Não é possível comparar.")
        return None, None
    else:
        print(f"Aviso: Nenhum arquivo JSON compatível encontrado em {directory_path}.")
        return None, None

def clean_old_files(directory_path, keep=2):
    """
    Deletes the oldest JSON files in a directory, keeping a specified number of recent files.
    """
    sorted_files = _get_sorted_files(directory_path)
    
    if len(sorted_files) > keep:
        files_to_delete = sorted_files[:-keep]
        print(f"Limpando arquivos antigos em '{directory_path}'...")
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"🗑️ Arquivo antigo removido: {os.path.basename(file_path)}")
            except OSError as e:
                print(f"❌ Erro ao deletar o arquivo {os.path.basename(file_path)}: {e}")
