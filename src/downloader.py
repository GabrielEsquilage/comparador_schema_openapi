import requests
import os
from datetime import datetime
from time import sleep

def baixar_json(url: str, target_dir_path: str, file_prefix: str, tentativas: int = 3, timeout: int = 120):
    """
    Baixa um arquivo JSON de uma URL e o salva em um diretório específico.
    """
    if not os.path.exists(target_dir_path):
        os.makedirs(target_dir_path)

    for tentativa in range(1, tentativas + 1):
        try:
            print(f"Tentativa {tentativa} de {tentativas}...")
            resposta = requests.get(url, timeout=timeout)
            resposta.raise_for_status()

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nome_arquivo = f"{file_prefix}-{timestamp}.json"
            caminho_arquivo = os.path.join(target_dir_path, nome_arquivo)

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(resposta.text)

            print(f"✅ JSON salvo em: {caminho_arquivo}")
            return

        except requests.exceptions.Timeout:
            print(f"⏳ Timeout na tentativa {tentativa}.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na tentativa {tentativa}: {e}")

        sleep(5)

    print(f"❌ Não foi possível baixar o JSON de {url} após várias tentativas.")
