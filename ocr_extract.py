import sys
import subprocess
import pkg_resources
import os

def check_and_install_packages():
    required_packages = ['pytesseract', 'pillow']
    missing_packages = []
    
    for package in required_packages:
        try:
            pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        install = input("Do you want to install them now? (y/n): ").lower()
        
        if install == 'y':
            for package in missing_packages:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("All required packages installed successfully.")
            return True
        else:
            print("\nPlease install the following packages manually:")
            for package in missing_packages:
                print(f"pip install {package}")
            return False
    return True

# Check dependencies first
if not check_and_install_packages():
    print("\nExiting due to missing dependencies.")
    input("Press Enter to close...")
    sys.exit(1)

try:
    import pytesseract
    from PIL import Image
    import tkinter as tk
    from tkinter import filedialog

    # Check if Tesseract is installed
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        print("Tesseract OCR is not installed or not in PATH.")
        print("Please install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("After installation, add the Tesseract directory to your PATH or set pytesseract.pytesseract.tesseract_cmd")
        input("Press Enter to exit...")
        sys.exit(1)

    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open file dialog to select an image
    print("Please select an image file...")
    image_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff")
        ]
    )

    # Check if a file was selected
    if not image_path:
        print("No file selected. Exiting.")
        sys.exit(0)

    print(f"Processing image: {image_path}")

    # Process the selected image
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)

    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Save the extracted text to a markdown file
    output_file = os.path.join(output_dir, "lecture_notes.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Extracted Text\n\n")
        f.write(text)

    print(f"\nExtracted text saved to: {output_file}")
    print("\nExtracted text preview:")
    print("-" * 50)
    print(text[:500] + "..." if len(text) > 500 else text)
    print("-" * 50)

except Exception as e:
    print(f"Error occurred: {str(e)}")
    input("Press Enter to exit...")