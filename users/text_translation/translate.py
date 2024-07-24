from .attention_based_translation import evaluateAndShowAttention as translate


def read_sentences(file_path):
    """Read sentences from a file and return them as a list, converted to lowercase."""
    with open(file_path, 'r', encoding='utf-8') as file:
        sentences = file.readlines()
    return [sentence.strip().lower() for sentence in sentences]


def find_sentence_index(sentence, sentences_list):
    """Find the index of a sentence in a list of sentences. Returns None if not found."""
    sentence = sentence.lower()  # Convert the sentence to lowercase before searching
    try:
        return sentences_list.index(sentence)
    except ValueError:
        return None


def translate_sentence(input_sentence, english_sentences, nweh_sentences):
    """Translate an English sentence to Nweh using the provided lists."""
    index = find_sentence_index(input_sentence, english_sentences)
    if index is not None:
        return nweh_sentences[index] + " <EOS>"
    else:
        main_translation = translate(input_sentence)
        return main_translation + " <EOS>"


# Paths to your text files
english_file_path = 'users/text_translation/data/english_sentences.txt'
nweh_file_path = 'users/text_translation/data/nweh_sentences.txt'

# Read sentences from files
english_sentences = read_sentences(english_file_path)
nweh_sentences = read_sentences(nweh_file_path)

# Example usage
input_sentence = "Hello"
translate_sentence(input_sentence, english_sentences, nweh_sentences)
