## import libraries
import os, sys
from pathlib import Path
from deepmultilingualpunctuation import PunctuationModel

## Filter filler words from transcripts
def filter_filler_words(text):
    filler_words = ["um", "uh", "like", "you know", "so", "actually"]
    words = text.split()
    filtered_text = " ".join([word for word in words if word.lower() not in filler_words])
    return filtered_text

## Read file, filter filler words, spell check, punctuation restoration, write to new file
def clean_transcript(file_clean, final_file):
    ## Read lecture transcript
    with open(file_clean, "r") as file:
        transcript = file.read()
    
    ## remove fillter words
    filtered_transcript = filter_filler_words(transcript)

    ## define punctuation model, https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large
    model = PunctuationModel()
    # punctuation restoration
    punctuated_transcript = model.restore_punctuation(filtered_transcript)

    with open(final_file, "w") as file:
        file.write(punctuated_transcript)

if __name__ == "__main__":
    # sys arguments for input and output directories
    input_dir_name = sys.argv[1]
    output_dir_name = sys.argv[2]
    # Set your input and output folders
    input_dir = Path(input_dir_name)
    output_dir = Path(output_dir_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Loop through all .txt files in the input directory
    for file_path in input_dir.glob("*.txt"):
        output_path = output_dir / file_path.name  # same name, new folder
        clean_transcript(file_path, output_path)
        print(f"Cleaned: {file_path.name}")