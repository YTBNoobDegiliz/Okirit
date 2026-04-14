import streamlit as st
import random

st.set_page_config(page_title="XOX Oyunu", page_icon="🎮")

# Modern CSS
st.markdown("""
<style>
    .xox-btn {
        width: 100%;
        height: 100px;
        font-size: 48px;
        font-weight: bold;
        border-radius: 15px;
        background-color: #2c3e50;
        color: white;
        border: 3px solid #34495e;
        transition: all 0.3s;
    }
    .xox-btn:hover {
        transform: scale(1.05);
        background-color: #e74c3c;
    }
    .title {
        text-align: center;
        font-size: 64px;
        font-weight: bold;
        color: #e74c3c;
        margin-bottom: 20px;
    }
    .turn-indicator {
        text-align: center;
        font-size: 24px;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        background-color: #34495e;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">⚡ X O X ⚡</div>', unsafe_allow_html=True)

# Session state
if 'board' not in st.session_state:
    st.session_state.board = [''] * 9
    st.session_state.current = 'X'
    st.session_state.game_over = False
    st.session_state.vs_computer = False
    st.session_state.winner = None

def check_winner():
    win_combo = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for combo in win_combo:
        if (st.session_state.board[combo[0]] == st.session_state.board[combo[1]] == 
            st.session_state.board[combo[2]] != ''):
            st.session_state.game_over = True
            st.session_state.winner = st.session_state.board[combo[0]]
            return True
    if '' not in st.session_state.board:
        st.session_state.game_over = True
        st.session_state.winner = 'berabere'
        return True
    return False

def make_move(index):
    if st.session_state.game_over:
        return
    if st.session_state.board[index] != '':
        return
    
    st.session_state.board[index] = st.session_state.current
    
    if not check_winner():
        if st.session_state.current == 'X':
            st.session_state.current = 'O'
        else:
            st.session_state.current = 'X'
        
        # Bilgisayar hamlesi
        if st.session_state.vs_computer and st.session_state.current == 'O' and not st.session_state.game_over:
            empty = [i for i, val in enumerate(st.session_state.board) if val == '']
            if empty:
                comp_move = random.choice(empty)
                st.session_state.board[comp_move] = 'O'
                check_winner()
                if not st.session_state.game_over:
                    st.session_state.current = 'X'

def reset_game():
    st.session_state.board = [''] * 9
    st.session_state.current = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

def set_mode(mode):
    reset_game()
    st.session_state.vs_computer = (mode == 'computer')

# Mod seçimi
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("👥 Arkadaşına Karşı", use_container_width=True):
        set_mode('friend')
with col2:
    if st.button("🤖 Bilgisayara Karşı", use_container_width=True):
        set_mode('computer')
with col3:
    if st.button("🔄 Yeni Oyun", use_container_width=True):
        reset_game()

# Sıra göstergesi
if st.session_state.game_over:
    if st.session_state.winner == 'X':
        st.success("🎉 SEN KAZANDIN! 🎉")
    elif st.session_state.winner == 'O':
        if st.session_state.vs_computer:
            st.error("🤖 BİLGİSAYAR KAZANDI! 🤖")
        else:
            st.error("🎉 ARKADAŞIN KAZANDI! 🎉")
    else:
        st.warning("🤝 BERABERE! 🤝")
else:
    if st.session_state.vs_computer:
        turn_text = "SEN (X)" if st.session_state.current == 'X' else "BİLGİSAYAR (O)"
    else:
        turn_text = f"OYUNCU {st.session_state.current}"
    st.markdown(f'<div class="turn-indicator">⭐ SIRA: {turn_text} ⭐</div>', unsafe_allow_html=True)

# Oyun tahtası (3x3 grid)
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        idx = i * 3 + j
        with cols[j]:
            if st.session_state.board[idx]:
                color = "#e74c3c" if st.session_state.board[idx] == 'X' else "#3498db"
                st.markdown(f"""
                <div style="
                    background-color: {color};
                    height: 100px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 48px;
                    font-weight: bold;
                    border-radius: 15px;
                    color: white;
                ">{st.session_state.board[idx]}</div>
                """, unsafe_allow_html=True)
            else:
                if st.button("⬜", key=f"btn_{idx}", use_container_width=True):
                    make_move(idx)
                    st.rerun()