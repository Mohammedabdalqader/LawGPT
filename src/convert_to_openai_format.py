import json

# Load the JSON data from the file
with open("preprocessed_data.json", 'r', encoding='utf-8') as file:
    preprocessed_data = json.load(file)

# Define a high quality prompt
system_prompt = "Translate the following Arabic text into English:"

# Function to convert translation pairs to the OpenAI API fine-tuning format
def convert_to_openai_format(pairs, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in pairs:
            # Construct the required structure
            if pair["accepted_for_finetuning"]:
                formatted_pair = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": pair["arabic"]},
                        {"role": "assistant", "content": pair["english"]}
                    ]
                }
                # Write the JSON object to the file followed by a newline
                f.write(json.dumps(formatted_pair, ensure_ascii=False) + '\n')

# Specify the output file name for the JSONL file
output_jsonl_file = 'openai_finetuning_data.jsonl'

# Convert and save the translation pairs in the OpenAI API format
convert_to_openai_format(preprocessed_data, output_jsonl_file)
print(f"All translation pairs have been saved to {output_jsonl_file} in the OpenAI API fine-tuning format.")
