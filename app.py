import os
import fitz  # PyMuPDF
import io
from PIL import Image
import time
from tqdm import tqdm
from google import genai
from google.genai import types
from support import convert_md_to_docx
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog

def process_pdf_images_to_markdown(pdf_path, api_key, system_prompt=None , save_images_of_pdf = False):
    """
    Process a PDF by extracting images and sending them to Gemini for processing.
    
    Args:
        pdf_path (str): Path to the PDF file
        api_key (str): Gemini API key
        system_prompt (str): System prompt for context
        
    Returns:
        str: Path to the generated markdown file
    """
    # Initialize Google Generative AI client
    client = genai.Client(api_key=api_key)
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    num_pages = len(doc)
    
    # Create output file
    # Create output folder if it doesn't exist
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    
    # Define output file path in the output folder
    output_file = os.path.join(output_folder, "lecture_notes.md")
    temp_folder = "temp_images"
    os.makedirs(temp_folder, exist_ok=True)
    
    print(f"Processing PDF with {num_pages} pages...")
    
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write("# Lecture Notes\n\n")
            
        # Process each page
        for page_num in tqdm(range(num_pages)):
            page = doc[page_num]
            
            # Get page as an image
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("png")
            
            # Save image temporarily (optional, for debugging)
            if save_images_of_pdf : 
                temp_img_path = os.path.join(temp_folder, f"page_{page_num}.png")
                with open(temp_img_path, "wb") as f:
                    f.write(img_bytes)
            
            # Load image for Gemini
            img = Image.open(io.BytesIO(img_bytes))
            
            try:
                # Process with Gemini
                prompt = """This is a page from lecture notes. Extract all text, correct any spelling mistakes or core conceptual errors, 
                and organize the information in a structured way with proper headings and bullet points.
                Format your response as clean markdown that I can directly use. Use proper indentation 
                and preserve all important information from the notes."""
                
                # Send to Gemini
                if system_prompt:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        config=types.GenerateContentConfig(
                                    system_instruction=system_prompt),
                        contents=[img, prompt]
                    )
                else:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[img, prompt]
                    )
                
                markdown_content = response.text
                
                # Clean up the markdown if needed
                if markdown_content.startswith("```markdown") and markdown_content.endswith("```"):
                    markdown_content = markdown_content[len("```markdown"):-3].strip()
                elif markdown_content.startswith("```") and markdown_content.endswith("```"):
                    markdown_content = markdown_content[3:-3].strip()
                # Remove the model's introductory text if present
                prefixes_to_remove = [
                    "Okay, here are the processed lecture notes, based on the OCR output and image, formatted in Markdown:",
                    "Here are the processed lecture notes based on the OCR output and image, formatted in Markdown:",
                    "Here are the lecture notes formatted in Markdown:",
                ]
                
                for prefix in prefixes_to_remove:
                    if markdown_content.lstrip().startswith(prefix):
                        markdown_content = markdown_content.replace(prefix, "", 1).lstrip()
                
                # Write to markdown file
                md_file.write(f"## Page {page_num+1}\n\n")
                md_file.write(f"{markdown_content}\n\n")
                md_file.write("---\n\n")
            
            except Exception as e:
                print(f"Error processing page {page_num + 1}: {e}")
                md_file.write(f"## Page {page_num+1}\n\n")
                md_file.write(f"*Error processing this page: {str(e)}*\n\n")
                md_file.write("---\n\n")
            
            # Simple rate limiting to avoid API throttling
            time.sleep(1)
    
    doc.close()
    print(f"Processing complete. Markdown saved to {output_file}")
    return output_file

def main():
    # Configuration
      # Your Gemini API key
    # Use file dialog to select PDF
    
    # Create and hide the root tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog to select PDF
    print("Please select a PDF file...")
    pdf_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    if not pdf_path:
        print("No file selected. Exiting.")
        return
        
    print(f"Selected file: {pdf_path}")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    
    # Biotechnology expert system prompt
    system_prompt = os.getenv("system_prompt")
    # Convert string "False" from env to actual boolean False
    save_images_of_pdf_str = os.getenv("save_images_of_pdf", "False")
    save_images_of_pdf = save_images_of_pdf_str.lower() == "true"

    # Get output file name from environment variable or use default
    output_file_name = os.getenv("output_file_name", "lecture_notes")
    output_file_name = os.path.join("output", output_file_name)
    
    # Process PDF directly to markdown
    markdown_file = process_pdf_images_to_markdown(pdf_path, api_key , system_prompt ,save_images_of_pdf)
    print(f"Process completed. Markdown saved to {markdown_file}")
    convert_md_to_docx(markdown_file , output_file_name)

if __name__ == "__main__":
    main()