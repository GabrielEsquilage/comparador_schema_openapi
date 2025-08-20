import baixar_erp
import baixar_inova
import os
import compare_docs

def main():
    print("Iniciando download do ERP...")
    baixar_erp.baixar_json("https://erp-api-stage-52421872894.us-central1.run.app/v3/api-docs")
    print("-" * 20)
    print("Iniciando download do Inova...")
    baixar_inova.baixar_json("https://cursos-livres-stage-52421872894.us-central1.run.app/api/v3/api-docs")
    print("-" * 20)
    print("Downloads concluídos.")

    print("\n--- Comparando documentação do ERP ---")
    erp_dir = os.path.join(os.path.dirname(__file__), "erp")
    old_erp_file, new_erp_file = compare_docs.get_old_new_files(erp_dir)
    if old_erp_file and new_erp_file:
        with open(old_erp_file, 'r') as f:
            old_erp_content = f.read()
        with open(new_erp_file, 'r') as f:
            new_erp_content = f.read()
        
        old_erp_endpoints = compare_docs.extract_endpoints(old_erp_content)
        new_erp_endpoints = compare_docs.extract_endpoints(new_erp_content)
        
        erp_diff = compare_docs.compare_endpoints(old_erp_endpoints, new_erp_endpoints)
        if erp_diff:
            print(f"Novos endpoints no ERP ({os.path.basename(new_erp_file)}):")
            for endpoint in erp_diff:
                print(f"- {endpoint}")
        else:
            print("Nenhum novo endpoint encontrado no ERP.")
    else:
        print("Não foi possível comparar os arquivos do ERP (necessário pelo menos dois arquivos).")

    print("\n--- Comparando documentação do Inova ---")
    inova_dir = os.path.join(os.path.dirname(__file__), "inova")
    old_inova_file, new_inova_file = compare_docs.get_old_new_files(inova_dir)
    if old_inova_file and new_inova_file:
        with open(old_inova_file, 'r') as f:
            old_inova_content = f.read()
        with open(new_inova_file, 'r') as f:
            new_inova_content = f.read()
        
        old_inova_endpoints = compare_docs.extract_endpoints(old_inova_content)
        new_inova_endpoints = compare_docs.extract_endpoints(new_inova_content)
        
        inova_diff = compare_docs.compare_endpoints(old_inova_endpoints, new_inova_endpoints)
        if inova_diff:
            print(f"Novos endpoints no Inova ({os.path.basename(new_inova_file)}):")
            for endpoint in inova_diff:
                print(f"- {endpoint}")
        else:
            print("Nenhum novo endpoint encontrado no Inova.")
    else:
        print("Não foi possível comparar os arquivos do Inova (necessário pelo menos dois arquivos).")

    print("\n--- Limpando arquivos antigos ---")
    compare_docs.delete_oldest_file(erp_dir)
    compare_docs.delete_oldest_file(inova_dir)

if __name__ == "__main__":
    main()
