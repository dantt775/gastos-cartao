import os
import json
import re
from datetime import datetime

def parse_currency(raw_str: str) -> float:
    # Remove R$, espaços e caracteres estranhos
    cleaned = re.sub(r"[^\d,\.]", "", raw_str).strip()
    
    # Se houver vírgula e ponto (ex: 1.250,50), remove o ponto de milhar e troca vírgula por ponto
    if "." in cleaned and "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "," in cleaned:
        # Se só tem vírgula (ex: 45,90)
        cleaned = cleaned.replace(",", ".")
        
    return float(cleaned)

def main():
    issue_body = os.environ.get("ISSUE_BODY", "")
    if not issue_body:
        raise ValueError("ISSUE_BODY está vazio.")

    # Extrai o valor
    valor_match = re.search(r"### Valor \(R\$\)\s*([^\n\r]+)", issue_body)
    if not valor_match:
        raise ValueError("Campo 'Valor (R$)' não encontrado na Issue.")
        
    valor = parse_currency(valor_match.group(1))

    # Extrai descrição
    desc_match = re.search(r"### Descrição / Estabelecimento\s*([^\n\r]+)", issue_body)
    descricao = desc_match.group(1).strip() if desc_match else "Sem descrição"

    # Extrai categoria
    cat_match = re.search(r"### Categoria\s*([^\n\r]+)", issue_body)
    categoria = cat_match.group(1).strip() if cat_match else "Outros"

    now = datetime.now()
    mes_atual = now.strftime("%Y-%m") # Ex: 2026-10
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Arquivo de dados
    os.makedirs("data", exist_ok=True)
    db_file = "data/gastos.json"

    dados = {"meses": {}}
    if os.path.exists(db_file):
        with open(db_file, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except Exception:
                dados = {"meses": {}}

    if "meses" not in dados:
        dados["meses"] = {}

    if mes_atual not in dados["meses"]:
        dados["meses"][mes_atual] = {
            "total": 0.0,
            "registros": []
        }

    # Adiciona novo registro
    novo_registro = {
        "data": timestamp,
        "descricao": descricao,
        "categoria": categoria,
        "valor": round(valor, 2)
    }
    dados["meses"][mes_atual]["registros"].append(novo_registro)

    # Recalcula total do mês
    total_mes = sum(item["valor"] for item in dados["meses"][mes_atual]["registros"])
    dados["meses"][mes_atual]["total"] = round(total_mes, 2)

    # Salva no arquivo JSON
    with open(db_file, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print(f"Gasto registrado: R$ {valor:.2f} | Categoria: {categoria} | Total do mês: R$ {total_mes:.2f}")

    # Exporta para o ambiente do GitHub Actions
    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a", encoding="utf-8") as env_f:
            env_f.write(f"NOVO_VALOR={valor:.2f}\n")
            env_f.write(f"NOVO_TOTAL={total_mes:.2f}\n")
            env_f.write(f"MES_ATUAL={mes_atual}\n")
            env_f.write(f"GASTO_DESC={descricao}\n")
            env_f.write(f"GASTO_CAT={categoria}\n")

if __name__ == "__main__":
    main()
