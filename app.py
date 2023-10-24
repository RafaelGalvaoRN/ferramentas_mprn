import streamlit as st
from calculadoras import prescricao_punitiva, prescricao_retroativa, prescricao_executoria
from calculadoras.prescricao_punitiva import menu_calc_prescricao_punitiva
from painel.controle_caso import evidencias
from quebra_pdf import split_pdf_by_size
from fragmentos_st import *
import zipfile
import os


st.set_page_config(
    page_title="Usar PyGWalker no Streamlit",
    layout="wide"
)

st.header('Calculadoras')
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Intro", "Prescrição Punitiva",
                                        "Prescrição Retroativa",
                                        "Prescrição Executória", "Visualizador", "Fragmentador_PDF"])

with tab1:
    boas_vindas()
    atualizacoes()

with tab2:
    menu_calc_prescricao_punitiva()

with tab3:
    prescricao_retroativa.calc_prescricao_retroativa()

with tab4:
    prescricao_executoria.calc_prescricao_executoria()

with tab5:
    evidencias()

with tab6:
    tamanho = st.number_input("Escolha o tamanho de cada parte do pdf, em megas", step=1, min_value=1)
    upload_file = st.file_uploader("Escolha um PDF")

    if upload_file is not None:
        if st.button("Fragmentar"):
            # Salvando o arquivo temporariamente
            temp_path = "temp_uploaded.pdf"
            with open(temp_path, "wb") as f:
                f.write(upload_file.getvalue())
            # Passando o caminho do PDF para a função split
            split_pdf_by_size(temp_path, tamanho)
            st.success("Fragmentação concluída")

            zip_filename = "arquivo_fragmentados.zip"
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for root, _, files in os.walk("pedacos_pdf"):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, file)

            # Botão para baixar o arquivo zip
            with open(zip_filename, "rb") as f:
                zip_data = f.read()
                st.success("Download disponível")
                st.download_button(label="Baixar todos os arquivos fragmentados", data=zip_data,
                                   file_name="arquivo_fragmentados.zip", mime="application/zip")



