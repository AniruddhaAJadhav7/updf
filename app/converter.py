import io
from PyPDF2 import PdfFileReader
from ebooklib import epub

def pdf_to_epub(pdf_content, original_filename):
    # Create a PDF reader object
    pdf_reader = PdfFileReader(io.BytesIO(pdf_content))
    
    # Create a new EPUB book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier(f'id_{original_filename}')
    book.set_title(original_filename.rsplit('.', 1)[0])
    book.set_language('en')
    
    # Add chapters
    chapters = []
    for page_num in range(pdf_reader.getNumPages()):
        chapter = epub.EpubHtml(title=f'Page {page_num + 1}', file_name=f'page_{page_num + 1}.xhtml', lang='en')
        chapter.content = f'<h1>Page {page_num + 1}</h1>'
        chapter.content += f'<p>{pdf_reader.getPage(page_num).extractText()}</p>'
        book.add_item(chapter)
        chapters.append(chapter)
    
    # Define Table of Contents
    book.toc = (epub.Link('nav.xhtml', 'Table of Contents', 'nav'),
                (epub.Section('Pages'),
                 chapters))
    
    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define CSS style
    style = '''
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        h1 { color: #333; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Write to in-memory file
    epub_file = io.BytesIO()
    epub.write_epub(epub_file, book, {})
    epub_file.seek(0)
    
    return epub_file
