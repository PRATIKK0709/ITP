from PIL import Image
from reportlab.pdfgen import canvas
from io import BytesIO
import os
import PyPDF2
import time

def create_pdf(images, output_pdf, compress_pdf=True):
    try:
        start_time = time.time()

        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer)

        for image_path in images:
            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"Error opening {image_path}: {e}")
                continue

            width, height = img.size

            # Ensure landscape or portrait orientation based on the image size
            if width > height:
                pdf.setPageSize((width, height))
            else:
                pdf.setPageSize((height, width))

            pdf.showPage()
            pdf.drawInlineImage(image_path, 0, 0, width, height)

        pdf.save()

        if compress_pdf:
            compress_output_pdf(pdf_buffer, output_pdf)
        else:
            with open(output_pdf, 'wb') as pdf_file:
                pdf_file.write(pdf_buffer.getvalue())

        end_time = time.time()
        print(f"PDF created successfully: {output_pdf}")
        print(f"Total processing time: {end_time - start_time:.2f} seconds")

    except Exception as e:
        print(f"Error: {e}")

def compress_output_pdf(pdf_buffer, output_pdf):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_buffer)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        with open(output_pdf, 'wb') as pdf_file:
            pdf_writer.write(pdf_file)

        print(f"Compressed PDF created successfully: {output_pdf}")

    except Exception as e:
        print(f"Error compressing PDF: {e}")

def get_image_paths():
    image_paths = []
    while True:
        image_path = input("Enter the path of an image (or 'exit' to finish): ")
        if image_path.lower() == 'exit':
            break
        elif os.path.exists(image_path) and os.path.isfile(image_path):
            image_paths.append(image_path)
        else:
            print("Invalid file path. Please enter a valid path to an existing file.")

    return image_paths

def get_output_pdf_path():
    while True:
        output_pdf_path = input("Enter the output PDF file path (or 'exit' to cancel): ")
        if output_pdf_path.lower() == 'exit':
            break
        elif output_pdf_path.lower().endswith('.pdf'):
            return output_pdf_path
        else:
            print("Invalid PDF file path. Please enter a valid path ending with '.pdf'.")

def get_compression_option():
    while True:
        compress_option = input("Do you want to compress the PDF to reduce file size? (yes/no): ").lower()
        if compress_option in ['yes', 'no']:
            return compress_option == 'yes'
        else:
            print("Invalid option. Please enter 'yes' or 'no'.")

def confirm_overwrite(output_pdf):
    if os.path.exists(output_pdf):
        user_input = input(f"The file {output_pdf} already exists. Do you want to overwrite it? (yes/no): ").lower()
        return user_input == 'yes'
    return True

if __name__ == "__main__":
    print("Welcome to the Enhanced Image to PDF Converter!")

    # Get input images from the user
    image_paths = get_image_paths()

    if not image_paths:
        print("No valid images provided. Exiting.")
    else:
        # Get output PDF file path from the user
        output_pdf_path = get_output_pdf_path()

        if output_pdf_path.lower() != 'exit':
            # Check if the user wants to overwrite an existing PDF file
            if not confirm_overwrite(output_pdf_path):
                print("Operation canceled. Exiting.")
            else:
                # Ask the user if they want to compress the PDF
                compress_pdf = get_compression_option()

                # Convert images to PDF
                create_pdf(image_paths, output_pdf_path, compress_pdf)
