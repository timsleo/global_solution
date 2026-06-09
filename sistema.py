# =============================================================================
# SISTEMA INTELIGENTE DE MONITORAMENTO 
# Global Solution - FIAP | Ciência da Computação
# =============================================================================
# Descrição: Sistema de monitoramento operacional para missão espacial
#            experimental, com diagnóstico automático, alertas priorizados
#            e previsão energética por regressão linear simples.
#            Os dados de telemetria são gerados aleatoriamente a cada execução
#            via numpy.random, simulando leituras reais de sensores.
# =============================================================================

import numpy as np
from collections import deque


# =============================================================================
# MÓDULO 1 — GERAÇÃO ALEATÓRIA DOS DADOS DA MISSÃO (numpy.random)
# Cada execução produz uma telemetria diferente, simulando sensores reais.
# Os dados respeitam faixas físicas coerentes com um ambiente marciano.
# =============================================================================

def gerar_modulos():
    """
    Gera status binário (0/1) para 6 módulos críticos via np.random.
    - Suporte à vida e habitat têm alta probabilidade de estar operacionais (95%)
    - Comunicação tem maior chance de falha (50%) — reflete instabilidade real
    - Demais módulos têm 80% de chance de estar operacionais
    Retorna dicionário (tabela hash) para acesso rápido por nome.
    """
    modulos = {
        "suporte_vida":  int(np.random.choice([0, 1], p=[0.05, 0.95])),
        "energia":       int(np.random.choice([0, 1], p=[0.20, 0.80])),
        "comunicacao":   int(np.random.choice([0, 1], p=[0.50, 0.50])),
        "habitat":       int(np.random.choice([0, 1], p=[0.05, 0.95])),
        "laboratorio":   int(np.random.choice([0, 1], p=[0.20, 0.80])),
        "armazenamento": int(np.random.choice([0, 1], p=[0.20, 0.80])),
    }
    return modulos


def gerar_energia():
    """
    Gera matriz (lista de listas) com 6 leituras de energia ao longo do dia.
    Cada linha: [horario, geracao_kw, consumo_kw, reserva_pct]

    Lógica física simulada:
    - Geração solar segue uma curva diurna (alta ao meio-dia, baixa à noite)
      com ruído gaussiano (np.random.normal) para variação realista
    - Consumo oscila em torno de um valor base com variação aleatória uniforme
    - Reserva é calculada incrementalmente: sobe quando geração > consumo,
      cai quando consumo > geração (limitada entre 10% e 100%)
    """
    horarios = ["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]

    # Perfil de geração solar base ao longo do dia (kW) — curva de sino
    geracao_base = [38.0, 52.0, 65.0, 45.0, 15.0, 4.0]

    # Consumo base com leve crescimento ao longo do dia (kW)
    consumo_base = [35.0, 40.0, 44.0, 50.0, 55.0, 58.0]

    # Reserva inicial aleatória entre 60% e 92%
    reserva = round(float(np.random.uniform(60.0, 92.0)), 1)

    leituras = []
    for i in range(6):
        # Adiciona ruído gaussiano à geração (desvio padrão de 5 kW)
        geracao = round(float(np.random.normal(geracao_base[i], 5.0)), 1)
        geracao = max(0.5, geracao)  # geração nunca negativa

        # Adiciona variação uniforme ao consumo (±8 kW)
        consumo = round(float(np.random.uniform(consumo_base[i] - 8, consumo_base[i] + 8)), 1)
        consumo = max(20.0, consumo)  # consumo mínimo para manter sistemas básicos

        # Atualiza reserva: cada kW de saldo equivale a ~0.3% de reserva no ciclo de 3h
        saldo   = geracao - consumo
        reserva = round(reserva + saldo * 0.3, 1)
        reserva = max(10.0, min(100.0, reserva))  # limita entre 10% e 100%

        leituras.append([horarios[i], geracao, consumo, reserva])

    return leituras


def gerar_variaveis_ambientais():
    """
    Gera variáveis ambientais com np.random dentro de faixas físicas marcianas.

    Faixas utilizadas:
    - Temperatura interna: 18–26°C (zona de conforto humano)
    - Temperatura externa: -80 a -40°C (superfície marciana)
    - Radiação: baixa / moderada / alto (sorteia com pesos)
    - Qualidade de comunicação: 10–95% (uniforme)
    - Velocidade do vento: 5–25 m/s (ventos marcianos típicos)
    """
    niveis_radiacao = ["baixo", "moderado", "alto"]
    pesos_radiacao  = [0.30, 0.35, 0.35]   # 35% de chance de radiação alta

    ambiente = {
        "temperatura_interna_c":     round(float(np.random.uniform(18.0, 26.0)), 1),
        "temperatura_externa_c":     round(float(np.random.uniform(-80.0, -40.0)), 1),
        "nivel_radiacao":            str(np.random.choice(niveis_radiacao, p=pesos_radiacao)),
        "qualidade_comunicacao_pct": int(np.random.randint(10, 96)),
        "velocidade_vento_ms":       round(float(np.random.uniform(5.0, 25.0)), 1),
    }
    return ambiente


def gerar_log_eventos(modulos, ambiente):
    """
    Gera log de eventos com exatamente 8 registros.
    Os eventos são sorteados de um banco de mensagens e complementados
    com eventos determinísticos baseados nos dados gerados (modulos, ambiente),
    garantindo ao menos uma FALHA ou REINICIO para a inconsistência proposital.

    Retorna lista de dicionários: {"horario", "tipo", "descricao"}
    """
    # Banco de eventos possíveis por tipo
    banco_info = [
        "Sistema inicializado com sucesso",
        "Painéis solares ajustados para máxima geração",
        "Modo economia de energia ativado no laboratório",
        "Verificação de integridade estrutural concluída",
        "Backup de dados científicos realizado com sucesso",
        "Calibração dos sensores ambientais concluída",
    ]
    banco_alerta = [
        "Consumo energético acima do planejado",
        "Pressão interna levemente abaixo do nominal",
        "Interferência detectada na frequência primária",
        "Temperatura dos painéis solares acima do ideal",
        "Nível de CO₂ interno próximo do limite de alerta",
    ]
    banco_falha = [
        "Sensor de comunicação reportou erro de sincronização",
        "Falha intermitente no módulo de armazenamento",
        "Erro de leitura no sensor de pressão externa",
        "Módulo de laboratório reportou falha de energia interna",
    ]
    banco_reinicio = [
        "Módulo de comunicação reiniciado sem sucesso",
        "Tentativa de reinício do sensor de telemetria falhou",
        "Sistema de backup de comunicação não respondeu",
    ]

    eventos = []
    horarios_disponiveis = [
        "05:30", "07:15", "08:40", "10:00", "11:50",
        "13:20", "15:10", "16:45", "18:00", "19:30", "20:30",
    ]

    # Embaralha os horários para variar a cada execução
    horarios = list(np.random.choice(horarios_disponiveis, size=8, replace=False))
    horarios.sort()  # mantém ordem cronológica no log

    # Slots fixos (garante diversidade de tipos no log)
    # 2 INFO obrigatórios
    for h in horarios[:2]:
        eventos.append({
            "horario":   h,
            "tipo":      "INFO",
            "descricao": str(np.random.choice(banco_info)),
        })

    # 1 ALERTA obrigatório de radiação se nivel for alto
    if ambiente["nivel_radiacao"] == "alto":
        eventos.append({
            "horario":   horarios[2],
            "tipo":      "ALERTA",
            "descricao": "Nível de radiação elevado detectado",
        })
    else:
        eventos.append({
            "horario":   horarios[2],
            "tipo":      "ALERTA",
            "descricao": str(np.random.choice(banco_alerta)),
        })

    # 1 ALERTA genérico
    eventos.append({
        "horario":   horarios[3],
        "tipo":      "ALERTA",
        "descricao": str(np.random.choice(banco_alerta)),
    })

    # 1 CRÍTICO se reserva baixou muito (último horário)
    eventos.append({
        "horario":   horarios[4],
        "tipo":      "CRITICO",
        "descricao": "Reserva energética abaixo de 70% no turno noturno",
    })

    # --- INCONSISTÊNCIA PROPOSITAL ---
    # Registra falha de comunicação no log, mas o status do módulo
    # pode aparecer como operacional (1) dependendo do sorteio em gerar_modulos().
    # O sistema deve detectar essa contradição no diagnóstico de inconsistências.
    eventos.append({
        "horario":   horarios[5],
        "tipo":      "FALHA",
        "descricao": str(np.random.choice(banco_falha)),
    })

    # 1 INFO de ação corretiva
    eventos.append({
        "horario":   horarios[6],
        "tipo":      "INFO",
        "descricao": str(np.random.choice(banco_info)),
    })

    # 1 REINICIO
    eventos.append({
        "horario":   horarios[7],
        "tipo":      "REINICIO",
        "descricao": str(np.random.choice(banco_reinicio)),
    })

    # Reordena cronologicamente
    eventos.sort(key=lambda e: e["horario"])
    return eventos


def construir_hierarquia(energia, ambiente):
    """
    Constrói hierarquia da missão com os valores gerados aleatoriamente.
    Estrutura: sistema → subsistema → valor atual
    """
    ultima_reserva = energia[-1][3]
    status_bat     = "critico" if ultima_reserva < 40 else ("alerta" if ultima_reserva < 65 else "normal")
    status_comm    = "critico" if ambiente["qualidade_comunicacao_pct"] < 30 else (
                     "alerta"  if ambiente["qualidade_comunicacao_pct"] < 60 else "normal")

    hierarquia = {
        "energia": {
            "solar":    {"geracao_kw": energia[2][1], "status": "operacional"},  # pico ao meio-dia
            "baterias": {"reserva_pct": ultima_reserva, "status": status_bat},
        },
        "habitat": {
            "oxigenio":    {"nivel_pct": round(float(np.random.uniform(92.0, 99.0)), 1), "status": "normal"},
            "temperatura": {"valor_c": ambiente["temperatura_interna_c"], "status": "normal"},
            "comunicacao": {"qualidade_pct": ambiente["qualidade_comunicacao_pct"], "status": status_comm},
        },
    }
    return hierarquia


# =============================================================================
# MÓDULO 2 — DIAGNÓSTICO E REGRAS LÓGICAS
# Classifica a situação operacional usando IF/ELIF/ELSE e AND/OR/NOT
#
# Expressão booleana principal do diagnóstico:
#   STATUS_CRITICO = (comunicacao == 0 AND qualidade_comm < 50)
#                OR (reserva < 60 OR (consumo > geracao AND reserva < 75))
#                OR (radiacao == "alto" AND temperatura_externa < -50)
#   STATUS_ALERTA  = (60 <= reserva < 75)
#                OR (NOT comunicacao OR qualidade_comm < 50)
#                OR (radiacao == "alto")
#   STATUS_NORMAL  = NOT STATUS_CRITICO AND NOT STATUS_ALERTA
# =============================================================================

def diagnosticar_missao(modulos, energia, ambiente):
    """
    Aplica regras lógicas para classificar o estado da missão.
    Retorna: ("CRITICO"|"ALERTA"|"NORMAL", lista de motivos)
    """
    ultima_leitura = energia[-1]
    reserva_atual  = ultima_leitura[3]
    consumo_atual  = ultima_leitura[2]
    geracao_atual  = ultima_leitura[1]
    radiacao       = ambiente["nivel_radiacao"]
    qualidade_comm = ambiente["qualidade_comunicacao_pct"]

    motivos = []

    # --- Regra 1: comunicação offline E qualidade baixa
    # Razão: dupla falha de comunicação = impossibilidade de contato com a Terra
    if not modulos["comunicacao"] and qualidade_comm < 50:
        motivos.append(("CRITICO", "Comunicação offline e qualidade do sinal abaixo de 50%"))

    # --- Regra 2: reserva crítica OU consumo supera geração com reserva baixa
    # Razão: sem energia suficiente, suporte à vida fica em risco
    if reserva_atual < 60 or (consumo_atual > geracao_atual and reserva_atual < 75):
        motivos.append(("CRITICO",
            f"Reserva energética em {reserva_atual:.1f}% com consumo "
            f"({consumo_atual:.1f} kW) > geração ({geracao_atual:.1f} kW)"))

    # --- Regra 3: radiação alta E temperatura externa extrema
    # Razão: combinação eleva risco para equipamentos externos e EVA
    if radiacao == "alto" and ambiente["temperatura_externa_c"] < -50:
        motivos.append(("CRITICO",
            f"Radiação elevada + temperatura externa extrema "
            f"({ambiente['temperatura_externa_c']:.1f}°C)"))

    if motivos:
        return "CRITICO", motivos

    # --- Regra 4: reserva em zona de alerta moderado
    if 60 <= reserva_atual < 75:
        motivos.append(("ALERTA", f"Reserva energética em zona de alerta: {reserva_atual:.1f}%"))

    # --- Regra 5: comunicação degradada isolada
    if not modulos["comunicacao"] or qualidade_comm < 50:
        motivos.append(("ALERTA", f"Qualidade de comunicação em {qualidade_comm}%"))

    # --- Regra 6: radiação alta isolada (sem os outros fatores críticos)
    if radiacao == "alto":
        motivos.append(("ALERTA", "Nível de radiação elevado — EVA não recomendado"))

    if motivos:
        return "ALERTA", motivos

    return "NORMAL", [("NORMAL", "Todos os sistemas dentro dos parâmetros operacionais")]


# =============================================================================
# MÓDULO 3 — DETECÇÃO DE INCONSISTÊNCIAS
# Identifica contradições entre o status dos módulos e o log de eventos
# =============================================================================

def detectar_inconsistencias(modulos, log_eventos):
    """
    Verifica se algum módulo marcado como operacional (1) tem registro
    de FALHA ou REINICIO no log — a inconsistência proposital do projeto.
    """
    inconsistencias = []

    for evento in log_eventos:
        if evento["tipo"] in ("FALHA", "REINICIO"):
            for modulo in modulos:
                nome_normalizado = modulo.replace("_", " ")
                if (nome_normalizado in evento["descricao"].lower() or
                        modulo in evento["descricao"].lower()):
                    if modulos[modulo] == 1:
                        inconsistencias.append(
                            f"[INCONSISTÊNCIA] Módulo '{modulo}' consta como operacional, "
                            f"mas log das {evento['horario']} registra: \"{evento['descricao']}\""
                        )

    # Checagem explícita: log de reinício de comunicação vs status do módulo
    reinicio_comm = [
        e for e in log_eventos
        if e["tipo"] in ("FALHA", "REINICIO") and "comunicação" in e["descricao"].lower()
    ]
    if reinicio_comm and modulos.get("comunicacao") == 1:
        inconsistencias.append(
            "[INCONSISTÊNCIA] Módulo 'comunicacao' aparece como operacional, "
            "mas há registros de falha/reinício sem sucesso no log."
        )

    if not inconsistencias:
        inconsistencias.append("Nenhuma inconsistência detectada entre status e log de eventos.")

    return inconsistencias


# =============================================================================
# MÓDULO 4 — SISTEMA DE ALERTAS (FILA + PILHA)
# Fila: alertas pendentes por ordem de chegada (FIFO)
# Pilha: últimos eventos críticos analisados (LIFO)
# =============================================================================

def gerar_alertas(status, motivos, modulos, ambiente):
    """
    Gera fila de alertas priorizados e empilha eventos críticos para análise.
    Retorna: (fila de alertas, pilha de eventos críticos)
    """
    fila_alertas   = deque()
    pilha_criticos = []

    # Alertas por módulos offline — prioridade máxima (insere na frente da fila)
    for modulo, estado in modulos.items():
        if not estado:
            alerta = {
                "nivel":    "CRITICO",
                "modulo":   modulo,
                "mensagem": f"Módulo '{modulo}' está OFFLINE",
            }
            fila_alertas.appendleft(alerta)
            pilha_criticos.append(alerta)

    # Alertas dos motivos do diagnóstico
    for nivel, mensagem in motivos:
        alerta = {"nivel": nivel, "modulo": "SISTEMA", "mensagem": mensagem}
        if nivel == "CRITICO":
            fila_alertas.appendleft(alerta)
            pilha_criticos.append(alerta)
        else:
            fila_alertas.append(alerta)

    # Alerta adicional de sinal degradado
    if ambiente["qualidade_comunicacao_pct"] < 50:
        fila_alertas.append({
            "nivel":    "ALERTA",
            "modulo":   "comunicacao",
            "mensagem": f"Qualidade de sinal em {ambiente['qualidade_comunicacao_pct']}% — risco de perda total",
        })

    return fila_alertas, pilha_criticos


# =============================================================================
# MÓDULO 5 — PREVISÃO ENERGÉTICA (REGRESSÃO LINEAR SIMPLES)
# Implementada manualmente — sem bibliotecas externas de ML
# Variável: reserva energética (%) ao longo das 6 leituras
# =============================================================================

def calcular_regressao_linear(x_vals, y_vals):
    """
    Calcula coeficientes a e b da reta y = ax + b pelo método dos mínimos quadrados.
    Implementação manual sem uso de numpy.polyfit ou similar.
    """
    n       = len(x_vals)
    soma_x  = sum(x_vals)
    soma_y  = sum(y_vals)
    soma_xy = sum(x_vals[i] * y_vals[i] for i in range(n))
    soma_x2 = sum(x * x for x in x_vals)

    a = (n * soma_xy - soma_x * soma_y) / (n * soma_x2 - soma_x ** 2)
    b = (soma_y - a * soma_x) / n
    return a, b


def prever_reserva_energetica(energia):
    """
    Usa regressão linear sobre as 6 leituras de reserva para prever
    o valor no próximo ciclo (+3h após a última leitura).
    Retorna: (previsao_pct, coef_a, coef_b)
    """
    x_vals = list(range(len(energia)))
    y_vals = [leitura[3] for leitura in energia]

    a, b         = calcular_regressao_linear(x_vals, y_vals)
    previsao_pct = a * len(energia) + b

    return previsao_pct, a, b


# =============================================================================
# MÓDULO 6 — RECOMENDAÇÕES AUTOMÁTICAS
# =============================================================================

def gerar_recomendacoes(status, modulos, ambiente, previsao_reserva):
    """
    Retorna lista de recomendações ordenadas por prioridade,
    adaptadas aos dados gerados aleatoriamente.
    """
    recomendacoes = []

    if modulos["suporte_vida"]:
        recomendacoes.append("[CRÍTICA] Manter suporte à vida operacional — prioridade absoluta de energia")

    if not modulos["comunicacao"]:
        recomendacoes.append("[CRÍTICA] Ativar protocolo de comunicação de emergência (frequência de backup)")
        recomendacoes.append("[CRÍTICA] Registrar falha de comunicação e tentar reconexão a cada 30 minutos")

    if previsao_reserva < 45:
        recomendacoes.append(
            f"[ALTA]    Previsão indica reserva em {previsao_reserva:.1f}% no próximo ciclo — "
            "desligar laboratório e sistemas não essenciais imediatamente"
        )
    elif previsao_reserva < 60:
        recomendacoes.append(
            f"[ALTA]    Reserva prevista em {previsao_reserva:.1f}% — reduzir consumo e ativar modo economia"
        )

    if ambiente["nivel_radiacao"] == "alto":
        recomendacoes.append("[ALTA]    Cancelar todas as atividades externas (EVA) enquanto radiação permanecer elevada")
        recomendacoes.append("[ALTA]    Verificar blindagem do habitat e integridade dos escudos de radiação")

    if ambiente["velocidade_vento_ms"] > 20:
        recomendacoes.append(
            f"[ALTA]    Vento em {ambiente['velocidade_vento_ms']:.1f} m/s — "
            "recolher equipamentos externos e reforçar ancoragem da base"
        )

    recomendacoes.append("[MÉDIA]   Aumentar frequência de leituras de telemetria para ciclos de 30 minutos")
    recomendacoes.append("[MÉDIA]   Registrar todas as anomalias no diário de bordo para análise posterior")

    return recomendacoes


# =============================================================================
# MÓDULO 7 — EXIBIÇÃO DOS RESULTADOS
# =============================================================================

def exibir_cabecalho():
    print("=" * 65)
    print("   SISTEMA DE MONITORAMENTO OPERACIONAL   ")
    print("=" * 65)


def exibir_modulos(modulos):
    print("\n📡 STATUS DOS MÓDULOS CRÍTICOS")
    print("-" * 45)
    print(f"  {'Módulo':<22} {'Status':<12} {'Binário'}")
    print(f"  {'-'*22} {'-'*12} {'-'*7}")
    for modulo, estado in modulos.items():
        status_txt = "✔  NORMAL" if estado else "✖  OFFLINE"
        print(f"  {modulo:<22} {status_txt:<12} [{estado}]")


def exibir_energia(energia):
    print("\n⚡ LEITURAS DE ENERGIA (kW / % reserva)")
    print("-" * 55)
    print(f"  {'Horário':<10} {'Geração':>10} {'Consumo':>10} {'Reserva':>10}")
    print(f"  {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
    for leitura in energia:
        horario, geracao, consumo, reserva = leitura
        print(f"  {horario:<10} {geracao:>9.1f}  {consumo:>9.1f}  {reserva:>8.1f}%")


def exibir_ambiente(ambiente):
    print("\n🌡  VARIÁVEIS AMBIENTAIS")
    print("-" * 45)
    for chave, valor in ambiente.items():
        chave_fmt = chave.replace("_", " ").capitalize()
        if isinstance(valor, float):
            print(f"  {chave_fmt:<35} {valor:.1f}")
        else:
            print(f"  {chave_fmt:<35} {valor}")


def exibir_hierarquia(hierarquia):
    print("\n🌳 HIERARQUIA DA MISSÃO")
    print("-" * 45)
    for sistema, subsistemas in hierarquia.items():
        print(f"  [{sistema.upper()}]")
        for subsistema, dados in subsistemas.items():
            linha = "  ".join(f"{k}: {v}" for k, v in dados.items())
            print(f"    ├─ {subsistema:<15} {linha}")


def exibir_log(log_eventos):
    print("\n📋 LOG DE EVENTOS DA MISSÃO")
    print("-" * 65)
    icones = {"INFO": "ℹ", "ALERTA": "⚠", "CRITICO": "🔴", "FALHA": "✖", "REINICIO": "🔄"}
    for evento in log_eventos:
        icone = icones.get(evento["tipo"], "•")
        print(f"  {evento['horario']}  {icone}  [{evento['tipo']:<8}]  {evento['descricao']}")


def exibir_inconsistencias(inconsistencias):
    print("\n🔍 DIAGNÓSTICO DE INCONSISTÊNCIAS")
    print("-" * 65)
    for item in inconsistencias:
        print(f"  {item}")


def exibir_previsao(energia, previsao, coef_a, coef_b):
    print("\n📈 PREVISÃO ENERGÉTICA — REGRESSÃO LINEAR SIMPLES")
    print("-" * 65)
    print(f"  Variável analisada : Reserva energética (%)")
    print(f"  Dados utilizados   : 6 leituras (06:00 → 21:00)")
    reservas = [f"{l[3]:.1f}%" for l in energia]
    print(f"  Valores observados : {' → '.join(reservas)}")
    print(f"  Equação ajustada   : reserva = {coef_a:.2f} × t + {coef_b:.2f}")
    print(f"  Previsão (próximo ciclo) : {previsao:.1f}%")
    if previsao < 40:
        situacao = "⚠  CRÍTICO — risco de colapso energético"
    elif previsao < 60:
        situacao = "⚠  ALERTA — reserva insuficiente para operação completa"
    else:
        situacao = "✔  Reserva dentro do limite mínimo aceitável"
    print(f"  Interpretação      : {situacao}")
    print(f"\n  → Esta previsão influencia as recomendações de desligamento")
    print(f"    de módulos não essenciais no próximo ciclo operacional.")


def exibir_diagnostico(status, motivos):
    print("\n🛰  DIAGNÓSTICO OPERACIONAL")
    print("-" * 65)
    icones_status = {"CRITICO": "🔴 CRÍTICO", "ALERTA": "🟡 ALERTA", "NORMAL": "🟢 NORMAL"}
    print(f"  Status da missão: {icones_status[status]}")
    print(f"\n  Motivos identificados:")
    for nivel, mensagem in motivos:
        print(f"    • [{nivel}] {mensagem}")


def exibir_alertas(fila_alertas, pilha_criticos):
    print("\n🚨 ALERTAS PENDENTES (FILA — ordem de prioridade)")
    print("-" * 65)
    if not fila_alertas:
        print("  Nenhum alerta ativo.")
    else:
        for i, alerta in enumerate(fila_alertas, 1):
            print(f"  [{i}] [{alerta['nivel']:<8}] {alerta['mensagem']}")

    print(f"\n📚 ÚLTIMOS EVENTOS CRÍTICOS ANALISADOS (PILHA)")
    print("-" * 65)
    if not pilha_criticos:
        print("  Nenhum evento crítico na pilha.")
    else:
        for evento in reversed(pilha_criticos):
            print(f"  → [{evento['nivel']}] {evento['mensagem']}")


def exibir_recomendacoes(recomendacoes):
    print("\n✅ RECOMENDAÇÕES AUTOMÁTICAS (por prioridade)")
    print("-" * 65)
    for i, rec in enumerate(recomendacoes, 1):
        print(f"  {i}. {rec}")


def exibir_rodape():
    print("\n" + "=" * 65)
    print("   FIM DO RELATÓRIO   ")
    print("=" * 65)


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

def executar_sistema():
    # --- Geração aleatória dos dados (novo conjunto a cada execução)
    modulos    = gerar_modulos()
    energia    = gerar_energia()
    ambiente   = gerar_variaveis_ambientais()
    log        = gerar_log_eventos(modulos, ambiente)
    hierarquia = construir_hierarquia(energia, ambiente)

    # --- Exibição dos dados
    exibir_cabecalho()
    exibir_modulos(modulos)
    exibir_energia(energia)
    exibir_ambiente(ambiente)
    exibir_hierarquia(hierarquia)
    exibir_log(log)

    # --- Análises
    inconsistencias              = detectar_inconsistencias(modulos, log)
    previsao, coef_a, coef_b     = prever_reserva_energetica(energia)
    status, motivos              = diagnosticar_missao(modulos, energia, ambiente)
    fila_alertas, pilha_criticos = gerar_alertas(status, motivos, modulos, ambiente)
    recomendacoes                = gerar_recomendacoes(status, modulos, ambiente, previsao)

    # --- Exibição dos resultados
    exibir_inconsistencias(inconsistencias)
    exibir_previsao(energia, previsao, coef_a, coef_b)
    exibir_diagnostico(status, motivos)
    exibir_alertas(fila_alertas, pilha_criticos)
    exibir_recomendacoes(recomendacoes)
    exibir_rodape()


if __name__ == "__main__":
    executar_sistema()
