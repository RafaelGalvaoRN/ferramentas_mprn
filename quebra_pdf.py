import os
import PyPDF2


def split_pdf_by_size(input_file_path, max_size_mb):
    # Caminho para a pasta "pedacos_pdf"
    output_directory = "pedacos_pdf"

    # Verificar se a pasta existe, se não, criar
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Limpar todos os arquivos na pasta "pedacos_pdf" se existirem
    for filename in os.listdir(output_directory):
        file_path_to_remove = os.path.join(output_directory, filename)
        if os.path.isfile(file_path_to_remove):
            os.remove(file_path_to_remove)

    with open(input_file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(reader.pages)

        start_page = 0
        end_page = 0
        file_count = 0

        temp_file_path = os.path.join(output_directory, 'temp_split.pdf')

        while end_page < total_pages:
            output = PyPDF2.PdfWriter()

            while end_page < total_pages:
                output.add_page(reader.pages[end_page])
                with open(temp_file_path, 'wb') as temp_file:
                    output.write(temp_file)
                if os.path.getsize(temp_file_path) / (1024 * 1024) < max_size_mb:
                    end_page += 1
                else:
                    break

            output_file_name = rf"Arquivo_parte_{file_count}_fl_{start_page}_a_fl_{end_page - 1}.pdf"
            final_output_path = os.path.join(output_directory, output_file_name)
            with open(final_output_path, 'wb') as output_file:
                output.write(output_file)

            print(f"[INFO] Created: {final_output_path}")
            start_page = end_page
            file_count += 1

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
