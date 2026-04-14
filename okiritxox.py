import streamlit as st

st.set_page_config(page_title="Hesap Makinesi + XOX", page_icon="🎮")

st.title("🎮 XOX OYUNU & HESAP MAKİNESİ")

# Sekmeler oluştur
tab1, tab2 = st.tabs(["🎮 XOX Oyunu", "🧮 Hesap Makinesi"])

# ========== XOX OYUNU ==========
with tab1:
    st.markdown('<div style="text-align: center; font-size: 36px; font-weight: bold; color: #e74c3c;">X O X</div>', unsafe_allow_html=True)
    
    if 'board' not in st.session_state:
        st.session_state.board = [''] * 9
        st.session_state.current = 'X'
        st.session_state.game_over = False
    
    def check_winner():
        win = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for w in win:
            if st.session_state.board[w[0]] == st.session_state.board[w[1]] == st.session_state.board[w[2]] != '':
                st.session_state.game_over = True
                return st.session_state.board[w[0]]
        if '' not in st.session_state.board:
            st.session_state.game_over = True
            return 'berabere'
        return None
    
    def make_move(i):
        if st.session_state.game_over or st.session_state.board[i] != '':
            return
        st.session_state.board[i] = st.session_state.current
        winner = check_winner()
        if not winner:
            st.session_state.current = 'O' if st.session_state.current == 'X' else 'X'
        st.rerun()
    
    def reset():
        st.session_state.board = [''] * 9
        st.session_state.current = 'X'
        st.session_state.game_over = False
        st.rerun()
    
    # Tahta
    cols = st.columns(3)
    for i in range(9):
        with cols[i % 3]:
            if st.session_state.board[i]:
                color = "#e74c3c" if st.session_state.board[i] == 'X' else "#3498db"
                st.markdown(f'<div style="background-color:{color};height:80px;display:flex;align-items:center;justify-content:center;font-size:40px;border-radius:10px;color:white;">{st.session_state.board[i]}</div>', unsafe_allow_html=True)
            else:
                if st.button("⬜", key=f"btn_{i}", use_container_width=True):
                    make_move(i)
    
    if st.button("🔄 Yeni Oyun", use_container_width=True):
        reset()
    
    if st.session_state.game_over:
        winner = check_winner()
        if winner == 'X':
            st.success("🎉 SEN KAZANDIN!")
        elif winner == 'O':
            st.error("❌ O KAZANDI!")
        else:
            st.warning("🤝 BERABERE!")
    else:
        st.info(f"🎯 Sıra: {st.session_state.current}")

# ========== HESAP MAKİNESİ ==========
with tab2:
    if 'expr' not in st.session_state:
        st.session_state.expr = ""
    
    def update(val):
        if val == "C":
            st.session_state.expr = ""
        elif val == "=":
            try:
                r = eval(st.session_state.expr.replace('×','*').replace('÷','/'))
                st.session_state.expr = str(int(r) if isinstance(r, float) and r.is_integer() else r)
            except:
                st.session_state.expr = "Hata"
        else:
            st.session_state.expr += val
        st.rerun()
    
    st.markdown(f'<div style="background-color:#2c3e50;padding:20px;border-radius:10px;text-align:right;font-size:40px;color:white;margin-bottom:20px;">{st.session_state.expr or "0"}</div>', unsafe_allow_html=True)
    
    btns = [['C','±','%','÷'],['7','8','9','×'],['4','5','6','-'],['1','2','3','+'],['0','.','=']]
    for row in btns:
        cols = st.columns(len(row))
        for col, btn in zip(cols, row):
            if col.button(btn, use_container_width=True):
                update(btn)