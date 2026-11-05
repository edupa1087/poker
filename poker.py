import streamlit as st
import random
from collections import Counter

# region LOGICA_CARTAS
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i for i, r in enumerate(RANKS, start=2)}


def crear_mazo():
    return [(r, s) for r in RANKS for s in SUITS]


def repartir(mazo, n):
    cartas = mazo[:n]
    del mazo[:n]
    return cartas


# endregion

# region EVALUACION_MANOS
def evaluar_mano(mano):
    valores = sorted([RANK_VALUES[carta[0]] for carta in mano], reverse=True)
    palos = [carta[1] for carta in mano]

    es_flush = len(set(palos)) == 1
    es_straight = (valores[0] - valores[4] == 4 and len(set(valores)) == 5) or (valores == [14, 5, 4, 3, 2])

    conteo = Counter(valores)
    frecuencias = sorted(conteo.values(), reverse=True)

    if es_straight and es_flush:
        return "Straight Flush" if valores[0] != 14 else "Royal Flush"
    if frecuencias == [4, 1]:
        return "Poker (Cuatro de un tipo)"
    if frecuencias == [3, 2]:
        return "Full House"
    if es_flush:
        return "Color (Flush)"
    if es_straight:
        return "Escalera (Straight)"
    if frecuencias == [3, 1, 1]:
        return "Trío"
    if frecuencias == [2, 2, 1]:
        return "Doble Pareja"
    if frecuencias == [2, 1, 1, 1]:
        return "Pareja"
    return "Carta Alta"


# endregion

# region INTERFAZ_STREAMLIT
def main():
    st.title("Poker: Five Card Draw")

    if 'estado' not in st.session_state:
        st.session_state.estado = 'INICIO'
        st.session_state.mazo = []
        st.session_state.mano = []

    if st.session_state.estado == 'INICIO':
        if st.button("Repartir Nueva Mano"):
            st.session_state.mazo = crear_mazo()
            random.shuffle(st.session_state.mazo)
            st.session_state.mano = repartir(st.session_state.mazo, 5)
            st.session_state.estado = 'DESCARTE'
            st.rerun()

    elif st.session_state.estado == 'DESCARTE':
        st.subheader("Tu Mano Actual:")

        cols = st.columns(5)
        descartes = []
        for i, carta in enumerate(st.session_state.mano):
            with cols[i]:
                st.write(f"### {carta[0]}{carta[1]}")
                if st.checkbox(f"Descartar", key=f"desc_{i}"):
                    descartes.append(i)

        if st.button("Confirmar Descartes y Robar"):
            # Reemplazar cartas descartadas
            nuevas_cartas = repartir(st.session_state.mazo, len(descartes))
            for idx, nueva_carta in zip(descartes, nuevas_cartas):
                st.session_state.mano[idx] = nueva_carta

            st.session_state.estado = 'RESULTADO'
            st.rerun()

    elif st.session_state.estado == 'RESULTADO':
        st.subheader("Mano Final:")
        cols = st.columns(5)
        for i, carta in enumerate(st.session_state.mano):
            with cols[i]:
                st.write(f"### {carta[0]}{carta[1]}")

        resultado = evaluar_mano(st.session_state.mano)
        st.success(f"Resultado: **{resultado}**")

        if st.button("Jugar de Nuevo"):
            st.session_state.estado = 'INICIO'
            st.rerun()


if __name__ == "__main__":
    main()
# endregion