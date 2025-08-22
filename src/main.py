import downloader
import os
import compare_docs
import gerenciador_arquivos
import json
from datetime import datetime

# --- Constants ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config.json')
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')
LOG_DIR = os.path.join(SCRIPT_DIR, 'logs')

def salvar_log(log_content):
    """Salva o conteúdo em um arquivo de log."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    log_file = os.path.join(LOG_DIR, 'diff_log.txt')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"--- {timestamp} ---\n")
        f.write(log_content)
        f.write("\n\n")

def comparar_e_reportar_diferencas(nome_servico, diretorio):
    output = []
    output.append(f"\n--- Comparando documentação do {nome_servico} ---")
    old_file, new_file = gerenciador_arquivos.get_latest_files(diretorio)
    if old_file and new_file:
        try:
            with open(old_file, 'r', encoding='utf-8') as f:
                old_content = f.read()
            with open(new_file, 'r', encoding='utf-8') as f:
                new_content = f.read()
            
            old_endpoints = compare_docs.extract_endpoints(old_content)
            new_endpoints = compare_docs.extract_endpoints(new_content)
            
            diff = compare_docs.compare_endpoints(old_endpoints, new_endpoints)
            if diff:
                output.append(f"Novos endpoints no {nome_servico} ({os.path.basename(new_file)}):")
                for endpoint in diff:
                    output.append(f"- {endpoint}")
            else:
                output.append(f"Nenhum novo endpoint encontrado no {nome_servico}.")
        except (IOError, json.JSONDecodeError) as e:
            output.append(f"Erro ao ler ou processar arquivos para o {nome_servico}: {e}")
    else:
        output.append(f"Não foi possível comparar os arquivos do {nome_servico} (necessário pelo menos dois arquivos).")
    
    log_output = "\n".join(output)
    print(log_output)
    salvar_log(log_output)

def main():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar o arquivo de configuração 'config.json': {e}")
        return

    services = config.get('services', [])
    if not services:
        print("Nenhum serviço encontrado no arquivo de configuração.")
        return

    # --- Download ---
    for service in services:
        print(f"Iniciando download do {service['name']}...")
        service_assets_dir = os.path.join(ASSETS_DIR, service['directory'])
        downloader.baixar_json(
            url=service['url'],
            target_dir_path=service_assets_dir,
            file_prefix=service['prefix']
        )
        print("-" * 20)
    print("Downloads concluídos.")

    # --- Comparação e Limpeza ---
    for service in services:
        service_assets_dir = os.path.join(ASSETS_DIR, service['directory'])
        comparar_e_reportar_diferencas(service['name'], service_assets_dir)
        
        print(f"\n--- Limpando arquivos antigos de {service['name']} ---")
        gerenciador_arquivos.clean_old_files(service_assets_dir)

if __name__ == "__main__":
    main()
