# 🚀 Sistema de Monitoramento Operacional 

**Global Solution | FIAP — Ciência da Computação**

---

## 👤 Equipe

| Nome | RM |
|------|----|
| Leonardo Tims Carneiro Campello | 571048 |

---

## 📖 Resumo do Problema e Cenário Analisado

O projeto Global Solution é uma missão espacial experimental operando em órbita baixa com uma base avançada de operações. O sistema enfrenta uma situação crítica noturna: a geração solar caiu drasticamente (de 61 kW ao meio-dia para apenas 5 kW às 21:00), enquanto o consumo permanece elevado (61 kW). Paralelamente, o módulo de comunicação está offline, o nível de radiação é alto e a temperatura externa está em -63°C.

O sistema de monitoramento recebe os dados de telemetria, organiza-os em estruturas computacionais adequadas, detecta inconsistências, classifica o estado operacional, gera alertas priorizados, prevê o comportamento energético futuro e emite recomendações automáticas para manter a tripulação segura.

---

## 🗂️ Estruturas de Dados Utilizadas

| Estrutura | Onde é usada | Por quê |
|-----------|-------------|---------|
| **Dicionário (hash)** | Status dos módulos críticos e variáveis ambientais | Acesso O(1) por nome do módulo — eficiente para consulta rápida |
| **Lista** | Leituras de energia ao longo do tempo | Série temporal ordenada; permite iterar e indexar por horário |
| **Matriz (lista de listas)** | Tabela de energia: [horário, geração, consumo, reserva] | Representa dados bidimensionais (tempo × variável) |
| **Fila (deque)** | Alertas pendentes por prioridade | FIFO com inserção prioritária na frente para críticos |
| **Pilha (list)** | Últimos eventos críticos analisados | LIFO — o último crítico identificado fica no topo |
| **Dicionário aninhado (árvore)** | Hierarquia da missão (energia → solar/baterias; habitat → oxigênio/temp./comm.) | Representa relações hierárquicas entre sistemas e subsistemas |

---

## ⚙️ Regras Lógicas Principais do Diagnóstico

**Expressão booleana principal:**

```
STATUS_CRITICO = (comunicacao == 0 AND qualidade_comm < 50)
              OR (reserva < 60 OR (consumo > geracao AND reserva < 75))
              OR (radiacao == "alto" AND temperatura_externa < -50)

STATUS_ALERTA  = (60 <= reserva < 75)
              OR (NOT comunicacao OR qualidade_comm < 50)
              OR (radiacao == "alto")

STATUS_NORMAL  = NOT STATUS_CRITICO AND NOT STATUS_ALERTA
```

| Regra | Condição | Ação gerada |
|-------|----------|-------------|
| 1 | `NOT comunicacao AND qualidade < 50` | Status CRÍTICO — protocolo de emergência |
| 2 | `reserva < 60 OR (consumo > geracao AND reserva < 75)` | Status CRÍTICO — redução imediata de consumo |
| 3 | `radiacao == "alto" AND temperatura_ext < -50` | Status CRÍTICO — cancelar EVA, verificar blindagem |
| 4 | `60 <= reserva < 75` | Status ALERTA — monitoramento intensificado |
| 5 | `NOT comunicacao OR qualidade < 50` | Status ALERTA — comunicação degradada |
| 6 | `radiacao == "alto"` (isolada) | Status ALERTA — EVA não recomendado |

---

## 📈 Técnica de Previsão Utilizada

**Regressão Linear Simples** — implementada manualmente sem bibliotecas externas.

- **Variável analisada:** Reserva energética (%) ao longo de 6 horários
- **Método:** Mínimos quadrados — calcula coeficientes `a` (inclinação) e `b` (intercepto) da reta `y = ax + b`
- **Dados usados:** 81.0% → 83.5% → 85.0% → 79.0% → 68.0% → 54.0%
- **Equação ajustada:** `reserva = -5.36 × t + 88.48`
- **Resultado previsto:** **56.3%** no próximo ciclo (~00:00)
- **Influência na decisão:** A previsão abaixo de 60% aciona a recomendação de desligamento de módulos não essenciais e ativação do modo economia antes que a reserva atinja nível crítico.

---

## 📥 Exemplo de Entrada e Saída

**Entrada (embutida no código):**
```
comunicacao      = 0      (offline)
reserva_atual    = 54.0%
consumo_atual    = 61.0 kW
geracao_atual    = 5.0 kW
nivel_radiacao   = alto
temperatura_ext  = -63°C
qualidade_comm   = 23%
```

**Saída resumida:**
```
Status da missão: 🔴 CRÍTICO

Motivos:
  • [CRITICO] Comunicação offline e qualidade do sinal abaixo de 50%
  • [CRITICO] Reserva energética em 54.0% com consumo (61.0 kW) > geração (5.0 kW)
  • [CRITICO] Radiação elevada combinada com temperatura externa extrema (-63°C)

Previsão energética: reserva = -5.36 × t + 88.48 → 56.3% no próximo ciclo
```

---

## ✅ Recomendações Geradas pelo Sistema

1. **[CRÍTICA]** Manter suporte à vida operacional — prioridade absoluta de energia
2. **[CRÍTICA]** Ativar protocolo de comunicação de emergência (frequência de backup)
3. **[CRÍTICA]** Registrar falha de comunicação e tentar reconexão a cada 30 minutos
4. **[ALTA]** Reserva prevista em 56.3% — reduzir consumo e ativar modo economia
5. **[ALTA]** Cancelar todas as atividades externas (EVA) enquanto radiação permanecer elevada
6. **[ALTA]** Verificar blindagem do habitat e integridade dos escudos de radiação
7. **[MÉDIA]** Aumentar frequência de leituras de telemetria para ciclos de 30 minutos
8. **[MÉDIA]** Registrar todas as anomalias no diário de bordo para análise posterior

---

## 🎬 Link do Vídeo

https://youtu.be/R3MHZYcqmoE

---

## 🏁 Conclusões e Aprendizados

O projeto demonstrou como conceitos fundamentais de programação — estruturas de dados, lógica booleana e algoritmos simples — podem ser combinados para construir um sistema de monitoramento funcional e coerente com cenários reais da indústria espacial.

A regressão linear implementada manualmente evidenciou que é possível realizar previsões úteis sem depender de bibliotecas avançadas, bastando compreender o raciocínio matemático por trás da técnica. A arquitetura modular do código facilita a manutenção e a extensão do sistema para novos sensores ou regras no futuro.

Do ponto de vista ético, o sistema prioriza sempre o suporte à vida, refletindo a responsabilidade que sistemas computacionais carregam em operações críticas onde decisões automatizadas impactam diretamente a segurança humana.

---

