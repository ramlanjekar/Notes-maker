import fitz
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Loop through each page in the PDF
    for page_index in range(len(doc)):
        # Get all images on the page
        for img_index, img in enumerate(doc[page_index].get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save the image to the output folder
            image_path = os.path.join(output_folder, f"page_{page_index}_img_{img_index}.{image_ext}")
            with open(image_path, "wb") as f:
                f.write(image_bytes)
    
    print(f"Images extracted to {output_folder}")

# Usage
pdf_path = r"C:\Users\HP\Downloads\DocScanner Apr 5, 2025 10-31 PM.pdf"
output_folder = "output"
extract_images_from_pdf(pdf_path, output_folder)
