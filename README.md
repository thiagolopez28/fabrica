# Gestor de Peças (Python, JSON, CLI)

Projeto simples e direto para **cadastro, validação e organização** de peças com **persistência em JSON** e **interface de linha de comando**.
Código 100% em **funções** (sem classes), com foco em legibilidade e manutenção.

> Este repositório resolve o desafio proposto: controlar peças, validar qualidade, embalar aprovadas em “caixas” lógicas e gerar relatório.

---

## Sumário

* [Requisitos](#requisitos)
* [Como executar](#como-executar)
* [Funcionalidades](#funcionalidades)
* [Regras de Qualidade](#regras-de-qualidade)
* [Estrutura de dados (JSON)](#estrutura-de-dados-json)
* [Detalhes de implementação](#detalhes-de-implementação)
* [Fluxo do menu](#fluxo-do-menu)
* [Exemplos de uso](#exemplos-de-uso)
* [Limitações e próximos passos](#limitações-e-próximos-passos)
* [Troubleshooting](#troubleshooting)
* [Licença](#licença)

---

## Requisitos

* **Python 3.8+** (biblioteca padrão)
* Sistema operacional: Windows, macOS ou Linux

Não há dependências externas. Tudo roda com `json`, `os` e `typing`.

---

## Como executar

1. Salve o arquivo do projeto (por exemplo) como `gestor_pecas.py`.
2. No terminal:

   ```bash
   python gestor_pecas.py
   ```
3. Um arquivo `dados.json` será criado automaticamente na primeira execução.

---

## Funcionalidades

* **Cadastrar nova peça**: ID único, peso (g), cor, comprimento (cm) e validação automática.
* **Listar aprovadas / reprovadas**: com detalhes e motivos da reprovação.
* **Remover peça por ID**.
* **Listar caixas**: agrupa peças **aprovadas** em lotes de **10** (apenas exibição; não persiste “caixas”).
* **Relatório geral**: total de peças, aprovadas/reprovadas, e resumo de caixas (fechadas/abertas).

---

## Regras de Qualidade

Uma peça é **aprovada** se atender **todas** as condições:

| Critério         | Regra                   |
| ---------------- | ----------------------- |
| Peso (g)         | `95 ≤ peso ≤ 105`       |
| Cor              | `azul` **ou** `verde`   |
| Comprimento (cm) | `10 ≤ comprimento ≤ 20` |

> Qualquer violação gera **status = reprovada** + **motivos de reprovação**.

---

## Estrutura de dados (JSON)

Arquivo: `dados.json`

```json
{
  "pecas": [
    {
      "id": "P001",
      "peso": 100.0,
      "cor": "azul",
      "comprimento": 15.0,
      "status": "aprovada",
      "motivos_reprovacao": []
    }
  ]
}
```

* `status`: `"aprovada"` ou `"reprovada"`.
* `motivos_reprovacao`: lista de strings. Vazia se aprovada.

---

## Detalhes de implementação

### Persistência

* `dados.json` é o **ponto único de verdade**.
* Em caso de arquivo ausente ou corrompido, o sistema inicia com `{"pecas": []}`.

### Entrada do usuário

* `valida_float()` aceita **vírgula ou ponto** como separador decimal.
* `valida_str()` padroniza strings (strip).

### Organização em “caixas”

* Função `embalar_em_caixas(…, capacidade=10)` **deriva** caixas **on-the-fly** a partir das peças **aprovadas**.
* Uma “caixa” é apenas um agrupamento lógico para exibição/relatório:

  ```python
  [{"indice": 1, "pecas": ["P001","P002",...], "fechada": True}, ...]
  ```

### Complexidade

* Operações são lineares sobre a lista de peças (O(n)). Suficiente para cargas pequenas/médias.

---

## Fluxo do menu

```
========= GESTOR DE PEÇAS =========
1 - Cadastrar nova peça
2 - Listar peças aprovadas
3 - Listar peças reprovadas
4 - Remover peça por ID
5 - Listar caixas (aprovadas em lotes de 10)
6 - Gerar relatório
0 - Sair
```

* **1**: Coleta dados, valida e persiste.
* **2/3**: Filtragem em memória (com leitura do JSON).
* **4**: Remove por ID e salva.
* **5**: Exibe caixas derivadas (não persiste caixas).
* **6**: Estatísticas agregadas + motivos de reprovação.

---

## Exemplos de uso

### Cadastro (com vírgula como decimal)

```
=== Cadastrar nova peça ===
ID da peça (único): P010
Peso (g): 100,5
Cor (azul/verde): verde
Comprimento (cm): 18
✅ Peça cadastrada e APROVADA!
```

### Reprovada (mensagens de motivo)

```
=== Cadastrar nova peça ===
ID da peça (único): P011
Peso (g): 120
Cor (azul/verde): vermelho
Comprimento (cm): 25
❌ Peça cadastrada e REPROVADA. Motivos:
   - Peso fora do intervalo (95 a 105g).
   - Cor inválida (apenas 'azul' ou 'verde').
   - Comprimento fora do intervalo (10 a 20cm).
```

### Caixas (derivadas)

```
=== Caixas (derivadas das peças aprovadas) ===
Caixa 01 [FECHADA] - 10 peça(s): P001, P002, ..., P010
Caixa 02 [ABERTA]  - 4 peça(s): P012, P013, P014, P015
```

---

## Troubleshooting

* **`ValueError` ao inserir números**
  Use **ponto ou vírgula**. O sistema converte vírgula para ponto (`valida_float`).
* **Arquivo `dados.json` corrompido**
  O sistema inicializa vazio. Se quiser preservar, faça backup antes de executar novamente.
* **ID duplicado**
  Cada peça deve ter **ID único**. Ao tentar duplicar, a operação é cancelada.

---

> **Nota de quem já quebrou muita pedra**: simples, legível e previsível ganha da complexidade “esperta” na maioria dos cenários. Se dói testar ou manter, refatore cedo. 😉
