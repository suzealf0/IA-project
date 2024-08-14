import streamlit as st
import os
import tensorflow as tf
from PIL import Image
import numpy as np
from datetime import datetime

# Carregar o modelo
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model('meu_modelo.h5')
    return model

model = load_model()

# Função para a tela de login
def tela_conectar():
    st.markdown("<h1 style='text-align: center; color: #00BF63;'>🔒 Login SnakeSense</h1>", unsafe_allow_html=True)

    st.write("Por favor, insira suas credenciais para acessar a aplicação:")
    username = st.text_input("Nome de Usuário", placeholder="Digite seu nome de usuário")
    password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
    
    if st.button("Conectar", key="connect_button", help="Clique para fazer login"):
        if username == "admin" and password == "senha123":  
            st.session_state.logged_in = True
            st.success("✅ Você está conectado! Redirecionando para a tela inicial...")
            st.experimental_set_query_params()
        else:
            st.error("❌ Nome de usuário ou senha inválidos. Tente novamente.")

# Função para logout
def logout():
    st.session_state.logged_in = False
    st.success("👋 Você foi desconectado.")
    st.experimental_set_query_params()

# Função para a tela inicial
def tela_inicial():
    st.markdown(
        """
        <style>
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-title {
            font-size: 2.5em;
            color: #2ecc71;
            margin-right: 20px;
        }
        .video-container {
            max-width: 150px;
            border-radius: 15px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Caminho absoluto para o vídeo local
    video_path = os.path.abspath("SnakeSense.mp4")

    st.markdown(
        f"""
        <div class="header-container">
            <div class="header-title">🐍 SnakeSense</div>
            <div class="video-container">
                <video autoplay loop muted style="max-width: 100%; border-radius: 15px;">
                    <source src="{video_path}" type="video/mp4">
                    Seu navegador não suporta o elemento <code>video</code>.
                </video>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border:1px solid #ddd;'>", unsafe_allow_html=True)

    if st.session_state.page == "Início":
        st.header("Bem-vindo ao SnakeSense")
        st.write("""
        Esta aplicação utiliza técnicas de aprendizado de máquina para identificar cobras e determinar se são venenosas ou não.
        Basta carregar uma imagem da cobra e o sistema fornecerá a sua classificação.
        """)
        
        st.image("https://th.bing.com/th/id/OIP.HXlVIzklKggin_T_LrO4TAHaE5?rs=1&pid=ImgDetMain", 
                 caption="Exemplo de Imagem de Cobra", use_column_width=True)
        
        st.subheader("Como usar a aplicação:")
        st.write("""
        1. **Carregue uma imagem**: Clique no botão abaixo para fazer o upload de uma imagem da cobra que deseja identificar.
        2. **Receba a análise**: A aplicação analisará a imagem e informará se a cobra é venenosa ou não.
        3. **Visualize os resultados**: Veja os resultados da identificação e obtenha informações adicionais se necessário.
        """)

        st.markdown("<hr style='border:1px solid #ddd;'>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Escolha uma imagem para identificar", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            if uploaded_file.name.endswith(('jpg', 'jpeg', 'png')):
                especie, tipo_veneno, descricao = resultado_tela(uploaded_file)
                st.success("🎉 Identificação Concluída!")
                adicionar_ao_historico(especie, tipo_veneno, descricao)
            else:
                st.error("❌ O arquivo carregado não é uma imagem válida. Por favor, carregue um arquivo de imagem nos formatos JPG, JPEG ou PNG.")
    
    elif st.session_state.page == "Sobre":
        st.markdown("<h2 style='color: #9b59b6;'>📚 Sobre a Aplicação</h2>", unsafe_allow_html=True)
        st.write("""
        Esta aplicação foi desenvolvida para identificar cobras e determinar se elas são venenosas ou não, utilizando técnicas de aprendizado de máquina.
        """)
        st.write("""
        Desenvolvido por: **Fernanda Caroline**, **Karen Alves**, **Suzane Alfaia**
        """)
    
    elif st.session_state.page == "Contato":
        st.markdown("<h2 style='color: #e74c3c;'>📞 Contato</h2>", unsafe_allow_html=True)
        st.write("""
        Para entrar em contato conosco, envie um e-mail para: **equipe4@gmail.com**
        """)
    
    elif st.session_state.page == "Histórico":
        st.markdown("<h2 style='color: #f39c12;'>📜 Histórico de Identificações</h2>", unsafe_allow_html=True)
        if 'historico' in st.session_state and len(st.session_state.historico) > 0:
            for idx, (especie, tipo_veneno, descricao, timestamp) in enumerate(st.session_state.historico):
                st.subheader(f"Identificação {idx + 1} - {timestamp}")
                st.write(f"**Espécie Identificada:** {especie}")
                st.write(f"**Tipo de Veneno:** {tipo_veneno}")
                st.write(f"**Descrição:** {descricao}")
                st.write("<hr style='border:1px solid #ddd;'>", unsafe_allow_html=True)
        else:
            st.info("Nenhuma identificação realizada ainda.")

    elif st.session_state.page == "Logout":
        logout()

# Função para a tela de resultados
def resultado_tela(uploaded_file):
    especie, tipo_veneno, descricao = process_image(uploaded_file)

    st.image(uploaded_file, caption="Imagem carregada", use_column_width=True)

    st.subheader("📊 Resultados da Identificação")
    st.write(f"**Espécie Identificada:** {especie}")
    st.write(f"**Tipo de Veneno:** {tipo_veneno}")
    st.write(f"**Descrição:** {descricao}")

    st.subheader("🔍 Mais Informações")
    st.write("""
    Se você encontrar uma cobra que parece ser venenosa, é importante manter distância e procurar ajuda médica imediatamente.
    Para mais informações sobre cobras e primeiros socorros, consulte um especialista em herpetologia ou um serviço de emergência.
    """)

    return especie, tipo_veneno, descricao

# Função para processar a imagem usando o modelo de CNN
def process_image(image):
    img = Image.open(image)
    
    # Redimensionar a imagem para (150, 150) como esperado pelo modelo
    img = img.resize((150, 150))  # Certifique-se de que este é o tamanho correto para o seu modelo
    
    img_array = np.array(img)

    # Normalizar a imagem (valores entre 0 e 1)
    img_array = img_array / 255.0

    # Adicionar uma dimensão extra para o lote
    img_array = np.expand_dims(img_array, axis=0)

    # Fazer a previsão
    prediction = model.predict(img_array)
    
    # Definindo as classes
    classes = ['Venomous', 'Non-Venomous']
    class_idx = np.argmax(prediction)
    especie = classes[class_idx]
    
    # Gerar a descrição baseada na classe identificada
    if especie == 'Venomous':
        descricao = "A cobra foi identificada como venenosa. Tenha cuidado!"
    else:
        descricao = "A cobra foi identificada como não venenosa."

    return especie, especie, descricao  # 'especie' é usado duas vezes pois 'tipo_veneno' é o mesmo valor

# Função para adicionar uma identificação ao histórico
def adicionar_ao_historico(especie, tipo_veneno, descricao):
    if 'historico' not in st.session_state:
        st.session_state.historico = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.historico.append((especie, tipo_veneno, descricao, timestamp))

# Função principal
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'page' not in st.session_state:
        st.session_state.page = "Início"

    if st.session_state.logged_in:
        # Estilização para os botões na barra lateral
        st.markdown("""
            <style>
            .sidebar .sidebar-content {
                padding: 10px;
            }
            .stButton button {
                width: 100%;
                padding: 10px;
                font-size: 18px;
                display: flex;
                align-items: center;
                justify-content: flex-start;
                border: none;
                background-color: #f4f4f4;
                color: #333;
                border-radius: 5px;
            }
            .stButton button:hover {
                background-color: #ddd;
            }
            .stButton button span {
                margin-right: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.sidebar:
            if st.button("Início"):
                st.session_state.page = "Início"
            if st.button("📚 Sobre"):
                st.session_state.page = "Sobre"
            if st.button("📞 Contato"):
                st.session_state.page = "Contato"
            if st.button("📜 Histórico"):
                st.session_state.page = "Histórico"
            if st.button("🔒 Logout"):
                logout()

        tela_inicial()
    else:
        tela_conectar()

if __name__ == "__main__":
    main()