# ===============================================
# SCORING.PY
# Calcula el perfil, el interés y el outcome final
# Incluye desempate jerárquico de 4 pasos
# ===============================================

# Orden de preguntas "diagnósticas" para el paso 3 del desempate
PROFILE_DIAGNOSTIC_ORDER = [3, 5, 6, 7, 11]
INTEREST_DIAGNOSTIC_ORDER = [2, 12, 8, 1]

# Orden fijo para el paso 4 del desempate (solo si todo lo demás empata)
PROFILE_FIXED_ORDER = ["Escalador", "Aprendiz", "Especialista", "Innovador", "Equilibrado"]
INTEREST_FIXED_ORDER = ["Tecnologia", "Estrategia", "Finanzas", "Negocio", "Personas", "Juridico", "Sostenibilidad"]


def resolve_winner(totals, question_counts, points_by_question, diagnostic_order, fixed_order):
    """
    Aplica el desempate jerárquico de 4 pasos:
    1. Mayor puntuación total
    2. Mayor número de preguntas en las que ha sumado puntos
    3. Más puntos en las preguntas diagnósticas, en el orden dado
    4. Orden fijo predefinido
    """
    # -----------------------------
    # Paso 1: mayor puntuación total
    # -----------------------------
    max_score = max(totals.values())
    candidates = [k for k, v in totals.items() if v == max_score]

    if len(candidates) == 1:
        return candidates[0]

    # -----------------------------
    # Paso 2: número de preguntas en las que ha puntuado
    # -----------------------------
    max_count = max(question_counts[c] for c in candidates)
    candidates = [c for c in candidates if question_counts[c] == max_count]

    if len(candidates) == 1:
        return candidates[0]

    # -----------------------------
    # Paso 3: prioridad de preguntas diagnósticas
    # -----------------------------
    for qid in diagnostic_order:
        qpoints = points_by_question.get(qid, {})
        scores = {c: qpoints.get(c, 0) for c in candidates}
        max_q = max(scores.values())

        if max_q > 0:
            new_candidates = [c for c in candidates if scores[c] == max_q]
            if len(new_candidates) == 1:
                return new_candidates[0]
            candidates = new_candidates

    # -----------------------------
    # Paso 4: orden fijo
    # -----------------------------
    for c in fixed_order:
        if c in candidates:
            return c

    return candidates[0]


def calculate_result(questions, answers):
    # -----------------------------
    # Inicializar perfiles
    # -----------------------------
    profiles = {
        "Escalador": 0,
        "Aprendiz": 0,
        "Equilibrado": 0,
        "Especialista": 0,
        "Innovador": 0
    }

    # -----------------------------
    # Inicializar intereses
    # -----------------------------
    interests = {
        "Tecnologia": 0,
        "Finanzas": 0,
        "Estrategia": 0,
        "Negocio": 0,
        "Personas": 0,
        "Juridico": 0,
        "Sostenibilidad": 0
    }

    # -----------------------------
    # Contadores de preguntas donde cada perfil/interés ha puntuado
    # -----------------------------
    profile_question_count = {p: 0 for p in profiles}
    interest_question_count = {i: 0 for i in interests}

    # -----------------------------
    # Puntos por pregunta (para el paso 3 del desempate)
    # -----------------------------
    profile_points_by_question = {}
    interest_points_by_question = {}

    # -----------------------------
    # Recorrer todas las respuestas
    # -----------------------------
    for question, answer_index in zip(questions, answers):
        option = question["options"][answer_index]
        qid = question["id"]

        profile_points_by_question[qid] = option["profile"]
        interest_points_by_question[qid] = option["interest"]

        # Sumar perfiles
        for profile, points in option["profile"].items():
            if points > 0:
                profiles[profile] += points
                profile_question_count[profile] += 1

        # Sumar intereses
        for interest, points in option["interest"].items():
            if points > 0:
                interests[interest] += points
                interest_question_count[interest] += 1

    # -----------------------------
    # Obtener perfil ganador (con desempate)
    # -----------------------------
    best_profile = resolve_winner(
        profiles,
        profile_question_count,
        profile_points_by_question,
        PROFILE_DIAGNOSTIC_ORDER,
        PROFILE_FIXED_ORDER
    )

    # -----------------------------
    # Obtener interés ganador (con desempate)
    # -----------------------------
    best_interest = resolve_winner(
        interests,
        interest_question_count,
        interest_points_by_question,
        INTEREST_DIAGNOSTIC_ORDER,
        INTEREST_FIXED_ORDER
    )

    # -----------------------------
    # Crear identificador del outcome
    # -----------------------------
    outcome = f"{best_profile}_{best_interest}"

    return {
        "profile": best_profile,
        "interest": best_interest,
        "outcome": outcome,
        "profiles": profiles,
        "interests": interests
    }