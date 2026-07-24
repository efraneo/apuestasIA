import streamlit as st
import database as db
from datetime import datetime

db.init_db()
st.set_page_config(page_title="AI Bet Generator PRO", page_icon="🤖", layout="wide")

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        import auth
        auth.show_auth()
        return

    user = st.session_state.user
    # NUEVOS ÍNDICES por la columna 'nombre': user[2]=nombre, user[3]=usuario, user[8]=ffinal, user[9]=perfil, user[13]=membresia
    nombre_user = user[2]
    perfil = user[9]
    fecha_final_str = user[8]
    membresia = user[13]

    if perfil != 'administrador' and fecha_final_str != 'NA':
        try:
            fecha_final = datetime.strptime(fecha_final_str, "%Y-%m-%d")
            if datetime.now() > fecha_final and membresia == 'gratis':
                import payment
                st.sidebar.button("Cerrar Sesión", on_click=logout)
                payment.show_payment()
                return
        except: pass

    # Mostrar Nombre y Rol (administrador) en el menú
    st.sidebar.title(f"👋 Hola, {nombre_user}")
    st.sidebar.markdown(f"**Rol:** {perfil.capitalize()}")
    if st.sidebar.button("🚪 Cerrar Sesión"): logout()

    if perfil == 'administrador':
        import dashboard
        import betting_app
        tab1, tab2 = st.tabs(["📊 Panel Admin", "🤖 Bot de Apuestas"])
        with tab1: dashboard.show_dashboard()
        with tab2: betting_app.show_betting_app()
    else:
        import betting_app
        import payment
        tab1, tab2 = st.tabs(["🤖 Bot de Apuestas", "💳 Mi Suscripción"])
        with tab1: betting_app.show_betting_app()
        with tab2: payment.show_payment()

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

if __name__ == "__main__":
    main()
