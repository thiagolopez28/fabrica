# Importações de bibliotecas
import json
import os
from typing import Dict, List, Tuple
# Salva local do arquivo JSON
ARQUIVO_DADOS = "dados.json"

# =========================
# Funções de manipulação do arquivo JSON
# =========================
def existe_json() -> bool:
    return os.path.exists(ARQUIVO_DADOS)

def carregar_dados() -> Dict:
    """Carrega o JSON do disco. Estrutura: {"pecas": [ ... ]}"""
    if not existe_json():
        return {"pecas": []}
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Corrige arquivo corrompido
        return {"pecas": []}

def salvar_dados(dados: Dict) -> None:
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# =========================
# Funções que garantem a entrada correta do usuário
# =========================
def valida_float(msg: str) -> float:
    """Aceita ponto ou vírgula como separador decimal."""
    while True:
        s = input(msg).strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            print("⚠️  Valor numérico inválido. Tente novamente.")

def valida_str(msg: str) -> str:
    s = input(msg).strip()
    return s

# =========================
# Funções que garantem a regra de qualidade das peças
# =========================
def validar_peca(peso: float, cor: str, comprimento: float) -> Tuple[bool, List[str]]:
    motivos = []
    cor_norm = cor.lower().strip()

    if not (95 <= peso <= 105):
        motivos.append("Peso fora do intervalo (95 a 105g).")
    if cor_norm not in ("azul", "verde"):
        motivos.append("Cor inválida (apenas 'azul' ou 'verde').")
    if not (10 <= comprimento <= 20):
        motivos.append("Comprimento fora do intervalo (10 a 20cm).")

    return (len(motivos) == 0, motivos)

# =========================
# Funções que implementam as funcionalidades do sistema
# =========================
def cadastrar_peca():
    dados = carregar_dados()
    pecas = dados.get("pecas", [])

    print("\n=== Cadastrar nova peça ===")
    id_peca = valida_str("ID da peça (único): ")

    # Verifica duplicidade de ID
    if any(p["id"] == id_peca for p in pecas):
        print("⚠️  Já existe peça com esse ID. Operação cancelada.")
        return

    peso = valida_float("Peso (g): ")
    cor = valida_str("Cor (azul/verde): ")
    comp = valida_float("Comprimento (cm): ")

    aprovada, motivos = validar_peca(peso, cor, comp)

    registro = {
        "id": id_peca,
        "peso": peso,
        "cor": cor.lower().strip(),
        "comprimento": comp,
        "status": "aprovada" if aprovada else "reprovada",
        "motivos_reprovacao": motivos
    }

    pecas.append(registro)
    salvar_dados({"pecas": pecas})

    if aprovada:
        print("✅ Peça cadastrada e APROVADA!")
    else:
        print("❌ Peça cadastrada e REPROVADA. Motivos:")
        for m in motivos:
            print("   -", m)

def remover_peca():
    dados = carregar_dados()
    pecas = dados.get("pecas", [])
    if not pecas:
        print("\n⚠️  Não há peças cadastradas.")
        return

    print("\n=== Remover peça ===")
    id_peca = valida_str("Informe o ID da peça: ")

    novas = [p for p in pecas if p["id"] != id_peca]
    if len(novas) == len(pecas):
        print("⚠️  Nenhuma peça com esse ID foi encontrada.")
        return

    salvar_dados({"pecas": novas})
    print("🗑️  Peça removida com sucesso.")

def listar_aprovadas():
    dados = carregar_dados()
    aprovadas = [p for p in dados.get("pecas", []) if p["status"] == "aprovada"]

    print("\n=== Peças APROVADAS ===")
    if not aprovadas:
        print("Nenhuma peça aprovada no momento.")
        return

    for p in aprovadas:
        print(f"- ID: {p['id']} | Peso: {p['peso']}g | Cor: {p['cor']} | Comp: {p['comprimento']}cm")

def listar_reprovadas():
    dados = carregar_dados()
    reprovadas = [p for p in dados.get("pecas", []) if p["status"] == "reprovada"]

    print("\n=== Peças REPROVADAS ===")
    if not reprovadas:
        print("Nenhuma peça reprovada no momento.")
        return

    for p in reprovadas:
        print(f"- ID: {p['id']} | Peso: {p['peso']}g | Cor: {p['cor']} | Comp: {p['comprimento']}cm")
        for m in p.get("motivos_reprovacao", []):
            print("   •", m)

# =========================
# Funções adicionais: Embalagem em caixas e relatório
# =========================
def embalar_em_caixas(pecas_aprovadas: List[Dict], capacidade: int = 10) -> List[Dict]:
    """
    Retorna uma lista de caixas: [{"indice": 1, "pecas": [ids...], "fechada": bool}, ...]
    A última caixa pode estar aberta se tiver menos que 'capacidade'.
    """
    ids = [p["id"] for p in pecas_aprovadas]
    caixas = []
    indice = 1
    for i in range(0, len(ids), capacidade):
        lote = ids[i:i+capacidade]
        caixas.append({
            "indice": indice,
            "pecas": lote,
            "fechada": len(lote) == capacidade
        })
        indice += 1
    return caixas

def listar_caixas():
    dados = carregar_dados()
    aprovadas = [p for p in dados.get("pecas", []) if p["status"] == "aprovada"]
    caixas = embalar_em_caixas(aprovadas, capacidade=10)

    print("\n=== Caixas (derivadas das peças aprovadas) ===")
    if not caixas:
        print("Nenhuma caixa gerada (não há peças aprovadas).")
        return

    for cx in caixas:
        status = "FECHADA" if cx["fechada"] else "ABERTA"
        print(f"Caixa {cx['indice']:02d} [{status}] - {len(cx['pecas'])} peça(s): {', '.join(cx['pecas'])}")

def gerar_relatorio():
    dados = carregar_dados()
    pecas = dados.get("pecas", [])
    aprovadas = [p for p in pecas if p["status"] == "aprovada"]
    reprovadas = [p for p in pecas if p["status"] == "reprovada"]
    caixas = embalar_em_caixas(aprovadas, capacidade=10)

    total = len(pecas)
    total_aprov = len(aprovadas)
    total_reprov = len(reprovadas)
    caixas_fechadas = sum(1 for c in caixas if c["fechada"])
    caixas_abertas = sum(1 for c in caixas if not c["fechada"])

    print("\n=== Relatório Geral ===")
    print(f"Total de peças cadastradas: {total}")
    print(f" - Aprovadas: {total_aprov}")
    print(f" - Reprovadas: {total_reprov}")
    print(f"Caixas geradas: {len(caixas)}")
    print(f" - Caixas fechadas (10/10): {caixas_fechadas}")
    print(f" - Caixas abertas (parciais): {caixas_abertas}")

    if reprovadas:
        print("\nMotivos de reprovação (por peça):")
        for p in reprovadas:
            motivos = p.get("motivos_reprovacao", [])
            print(f" • ID {p['id']}: " + ("; ".join(motivos) if motivos else "—"))

# =========================
# Menu de operações
# =========================
def menu():
    opcoes = {
        "1": ("Cadastrar nova peça", cadastrar_peca),
        "2": ("Listar peças aprovadas", listar_aprovadas),
        "3": ("Listar peças reprovadas", listar_reprovadas),
        "4": ("Remover peça por ID", remover_peca),
        "5": ("Listar caixas (aprovadas em lotes de 10)", listar_caixas),
        "6": ("Gerar relatório", gerar_relatorio),
        "0": ("Sair", None),
    }

    while True:
        print("\n========= GESTOR DE PEÇAS =========")
        for k, (nome, _) in opcoes.items():
            print(f"{k} - {nome}")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Até mais! 👋")
            break

        func = opcoes.get(escolha, (None, None))[1]
        if func is None:
            print("⚠️  Opção inválida.")
        else:
            func()

# =========================
# Execução do sistema
# =========================
if __name__ == "__main__":
    # Garante arquivo base
    if not existe_json():
        salvar_dados({"pecas": []})
    menu()
