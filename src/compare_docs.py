import json

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