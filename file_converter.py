import logging
import os
from pathlib import Path
from docx import Document
from fpdf import FPDF
from pdf2docx import Converter

logger = logging.getLogger(__name__)

class FileConverter:
    def __init__(self):
        # Use absolute path for temp directory and ensure it exists with proper permissions
        self.temp_dir = Path(os.getcwd()) / "temp"
        try:
            self.temp_dir.mkdir(mode=0o755, exist_ok=True)
            logger.info(f"Temporary directory created/verified at {self.temp_dir}")
        except Exception as e:
            logger.error(f"Failed to create temp directory: {str(e)}")
            raise

    def word_to_pdf(self, word_file_path: str) -> str:
        """Convert Word document to PDF"""
        try:
            logger.info(f"Starting Word to PDF conversion for {word_file_path}")

            # Verify input file exists and is readable
            if not os.path.exists(word_file_path):
                raise FileNotFoundError(f"Input file not found: {word_file_path}")

            # Create PDF with proper configuration
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Read Word document
            logger.debug("Opening Word document...")
            doc = Document(word_file_path)
            logger.debug("Word document opened successfully")

            # Use Arial font (built into FPDF2)
            pdf.set_font("Arial", size=12)

            # Add text to PDF with proper encoding
            logger.debug("Processing paragraphs...")
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():  # Skip empty paragraphs
                    text = paragraph.text.encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(w=190, h=10, text=text, align='L')
            logger.debug("Paragraphs processed successfully")

            # Save PDF with absolute path
            output_path = str(self.temp_dir / f"{Path(word_file_path).stem}.pdf")
            logger.debug(f"Saving PDF to {output_path}")
            pdf.output(output_path)

            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Output file not found at {output_path}")

            logger.info(f"Successfully converted Word file to PDF: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error converting Word to PDF: {str(e)}")
            if os.path.exists(word_file_path):
                logger.error(f"Input file size: {os.path.getsize(word_file_path)} bytes")
            raise

    def pdf_to_word(self, pdf_file_path: str) -> str:
        """Convert PDF to Word document"""
        try:
            logger.info(f"Starting PDF to Word conversion for {pdf_file_path}")

            # Verify input file exists and is readable
            if not os.path.exists(pdf_file_path):
                raise FileNotFoundError(f"Input file not found: {pdf_file_path}")

            # Create output path with absolute path
            output_path = str(self.temp_dir / f"{Path(pdf_file_path).stem}.docx")
            logger.debug(f"Output path set to {output_path}")

            # Convert PDF to Word with proper error handling
            logger.debug("Initializing PDF converter...")
            cv = Converter(pdf_file_path)
            logger.debug("Starting conversion process...")
            cv.convert(output_path, start=0, end=None)
            cv.close()
            logger.debug("Conversion completed")

            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Conversion completed but output file not found at {output_path}")

            logger.info(f"Successfully converted PDF to Word: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error converting PDF to Word: {str(e)}")
            if os.path.exists(pdf_file_path):
                logger.error(f"Input file size: {os.path.getsize(pdf_file_path)} bytes")
            raise

    def cleanup_temp_files(self, file_path: str):
        """Remove temporary files"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {str(e)}")