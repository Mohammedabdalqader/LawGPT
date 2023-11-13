import os
from docx import Document
import json
import re
import tiktoken

def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# Function to check if a string contains Arabic characters
def contains_arabic(text):
    return any('\u0600' <= char <= '\u06FF' or
               '\u0750' <= char <= '\u077F' or
               '\u08A0' <= char <= '\u08FF' or
               '\uFB50' <= char <= '\uFDFF' or
               '\uFE70' <= char <= '\uFEFF' for char in text)


# Function to clean up the text by reducing all instances of multiple spaces to single spaces
def clean_up_text(text, with_new_lines= True):
    if with_new_lines:
        # Replace multiple spaces (but not new lines) with a single space
        text = re.sub(r'[ \t]+', ' ', text)

        # Optionally, if you want to clean up spaces before and after each new line, please uncomment the line bellow.
        #text = re.sub(r' ?\n ?', '\n', text)

        # Strip leading and trailing whitespace without removing new lines
        text = text.strip(' \t')
    else:
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)

        # Strip leading and trailing whitespace
        text = text.strip()

    return text



# Function to extract text from tables and create a list of translation pairs
def extract_translations_from_tables(doc):
    translations = []
    for table in doc.tables:
        for row in table.rows:
            cells = row.cells
            # Process each pair of cells
            for i in range(0, len(cells), 2):
                if i + 1 < len(cells):  # Ensure there is a pair of cells to evaluate
                    # Split the text by two or three new lines and clean up text
                    english_parts = [clean_up_text(part, True) for part in re.split(r'\n\n\n|\n\n', cells[i].text)]
                    arabic_parts = [clean_up_text(part, True) for part in re.split(r'\n\n\n|\n\n', cells[i + 1].text)]

                    # Check if there is a mismatch in the number of parts
                    if len(arabic_parts) != len(english_parts):
                        print(f"Warning: Mismatched parts in the document for row {row}.")
                        
                        

                    # Pair up the split parts
                    for english_text, arabic_text in zip(english_parts,arabic_parts):
                        if contains_arabic(arabic_text):  # Checking for Arabic text
                            num_token_ar = num_tokens_from_string(arabic_text,model_name="gpt-3.5-turbo")
                            num_token_en = num_tokens_from_string(english_text,model_name="gpt-3.5-turbo")

                            if num_token_ar + num_token_en < 4000:
                                accepted_for_finetuning = True
                            else:
                                accepted_for_finetuning = False


                            translations.append({
                                "arabic": arabic_text,
                                "english": english_text,
                                "num_token_ar":num_token_ar,
                                "num_tocken_en":num_token_en,
                                "accepted_for_finetuning": accepted_for_finetuning
                            })
    return translations


# Function to save translation pairs to a JSON file
def save_to_json(pairs, output_file):
    # Use a dictionary to remove duplicates, converting each pair to a tuple which will be the dictionary key
    unique_pairs = {json.dumps(pair, ensure_ascii=False): pair for pair in pairs}
    # Now we have only unique pairs, write them to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(list(unique_pairs.values()), f, ensure_ascii=False, indent=4)


# Root path of the 'data' folder
root_dir = 'data'  # Make sure this is the correct path to your 'data' folder

# Initialize an empty list to hold all preprocessed_data
preprocessed_data = []

if __name__ == "__main__":

    for sub in os.listdir(root_dir):
        sub_folder_path = os.path.join(root_dir, sub)
        if os.path.isdir(sub_folder_path):  # Check if it is a folder
            for file in os.listdir(sub_folder_path):
                if file.endswith('.docx'):
                    doc_path = os.path.join(sub_folder_path, file)
                    print(doc_path)
                    # Load the document
                    doc = Document(doc_path)
                    # Get the translation pairs from the current document
                    pairs = extract_translations_from_tables(doc)
                    # Add the pairs from this document to the overall list
                    preprocessed_data.extend(pairs)

    # After all files have been processed, save all translation pairs to a JSON file
    save_to_json(preprocessed_data, 'preprocessed_data.json')
    print("All arabic-english pairs have been saved to preprocessed_data.json")
