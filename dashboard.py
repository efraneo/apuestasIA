import streamlit as st
import pandas as pd
import plotly.express as px
import database as db

def show_dashboard():
    st.title("📊 Dashboard Administrador")
    
    users = db.get_all_users()
    df = pd.DataFrame(users, columns=['Identificación', 'Nombre', 'Usuario', 'Correo', 'F. Inicio', 'F. Final', 'Perfil', 'Ingresos', 'Análisis', 'Estado', 'Membresía'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Usuarios", len(df))
    col2.metric("Usuarios Aprobados", len(df[df['Estado'] == 'aprobado']))
    col3.metric("Pendientes / Rechazados", len(df[df['Estado'] != 'aprobado']))
    
    st.divider()
    
    st.subheader("Distribución de Usuarios")
    pie_data = df['Estado'].value_counts().reset_index()
    pie_data.columns = ['Estado', 'Cantidad']
    fig = px.pie(pie_data, values='Cantidad', names='Estado', title='Estado de Registros', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("⚙️ Gestión y Edición Total de Usuarios")
    st.dataframe(df, use_container_width=True)
    
    # --- PANEL DE EDICION Y ELIMINACION ---
    with st.expander("✏️ Modificar, Actualizar o Eliminar Usuario"):
        user_ids = df['Identificación'].tolist()
        if user_ids:
            sel_id = st.selectbox("Selecciona usuario por Identificación", user_ids)
            sel_user = df[df['Identificación'] == sel_id].iloc[0]
            
            with st.form("edit_user_form"):
                nombre = st.text_input("Nombre", sel_user['Nombre'])
                usuario = st.text_input("Usuario", sel_user['Usuario'])
                correo = st.text_input("Correo", sel_user['Correo'])
                fecha_final = st.text_input("Fecha Final (YYYY-MM-DD o NA)", sel_user['F. Final'])
                estado = st.selectbox("Estado", ['pendiente', 'aprobado', 'rechazado'], index=['pendiente', 'aprobado', 'rechazado'].index(sel_user['Estado']))
                membresia = st.selectbox("Membresía", ['gratis', 'paga'], index=['gratis', 'paga'].index(sel_user['Membresía']))
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("💾 Guardar Cambios"):
                    db.update_user(sel_id, nombre, usuario, correo, fecha_final, estado, membresia)
                    st.success("Usuario actualizado exitosamente.")
                    st.rerun()
                if c2.form_submit_button("🗑️ Eliminar Usuario"):
                    db.delete_user(sel_id)
                    st.warning("Usuario eliminado permanentemente.")
                    st.rerun()
        else:
            st.info("No hay usuarios.")
            
    st.divider()
    st.subheader("👑 Top 5 Usuarios (Más Análisis)")
    top_users = df.sort_values(by='Análisis', ascending=False).head(5)
    st.dataframe(top_users[['Nombre', 'Usuario', 'Ingresos', 'Análisis']], use_container_width=True)
