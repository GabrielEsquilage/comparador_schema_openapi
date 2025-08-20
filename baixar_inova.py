import requests
import os
from datetime import datetime
from time import sleep

def limpar_arquivos_antigos(diretorio: str):
    """Mantém apenas os dois arquivos JSON mais recentes em um diretório."""
    try:
        arquivos_json = [f for f in os.listdir(diretorio) if f.endswith('.json') and os.path.isfile(os.path.join(diretorio, f))]
        
        if len(arquivos_json) > 2:
            # Ordena por data de modificação para encontrar os mais antigos
            arquivos_json.sort(key=lambda f: os.path.getmtime(os.path.join(diretorio, f)))
            
            # Os arquivos a serem removidos são todos, exceto os dois últimos
            arquivos_para_remover = arquivos_json[:-2]
            
            print(f"Limpando arquivos antigos em '{diretorio}'...")
            for arquivo in arquivos_para_remover:
                caminho_completo = os.path.join(diretorio, arquivo)
                os.remove(caminho_completo)
                print(f"🗑️ Arquivo antigo removido: {arquivo}")
    except Exception as e:
        print(f"❌ Erro ao limpar arquivos antigos: {e}")

def baixar_json(url: str, prefixo: str = "api-docs-inova-data", tentativas: int = 3, timeout: int = 120):
    diretorio_inova = os.path.join(os.getcwd(), "inova")
    if not os.path.exists(diretorio_inova):
        os.makedirs(diretorio_inova)

    for tentativa in range(1, tentativas + 1):
        try:
            print(f"Tentativa {tentativa} de {tentativas}...")
            resposta = requests.get(url, timeout=timeout)
            resposta.raise_for_status()

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"{prefixo}-{timestamp}.json"
            caminho_arquivo = os.path.join(diretorio_inova, nome_arquivo)

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(resposta.text)

            print(f"✅ JSON salvo em: {caminho_arquivo}")
            limpar_arquivos_antigos(diretorio_inova)
            return  # se deu certo, sai da função

        except requests.exceptions.Timeout:
            print(f"⏳ Timeout na tentativa {tentativa}.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na tentativa {tentativa}: {e}")

        # espera um pouco antes de tentar de novo
        sleep(5)

    print("❌ Não foi possível baixar o JSON após várias tentativas.")

if __name__ == "__main__":
    url = "https://cursos-livres-stage-52421872894.us-central1.run.app/api/v3/api-docs"
    baixar_json(url)
