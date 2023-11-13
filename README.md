# LawGPT

LawGPT is an innovative project that focuses on fine-tuning ChatGPT for machine translation between Arabic and English, specifically tailored for legal documents. This project is designed to bridge the language gap in legal contexts, making vital legal information accessible across language barriers.

## Project Structure

src/

    data_preprocessing.py
    convert_to_openai_format.py
    data_analysis.py

data/
    [Subfolders containing .docx files]


### Scripts Description

- `data_preprocessing.py`: Extracts Arabic-English text pairs, particularly from legal documents, to prepare for fine-tuning ChatGPT for Arabic to English translation.
- `convert_to_openai_format.py`: Converts the preprocessed data into a format compatible with OpenAI's API, ensuring the data is ready for model input.
- `data_analysis.py`: Analyses the preprocessed data to estimate the total cost and resources required for the fine-tuning process.

## Requirements

This project requires the following:

    Python 3.8 or higher
    Libraries as listed in requirements.txt




## Installation

To get started with LawGPT, follow these steps:

```bash
git clone https://github.com/Mohammedabdalqader/LawGPT.git
cd LawGPT
pip install -r requirements.txt
```

## Usage

Run the scripts from the root folder of the project as shown below:

    python src/data_preprocessing.py
    python src/convert_to_openai_format.py
    python src/data_analysis.py
