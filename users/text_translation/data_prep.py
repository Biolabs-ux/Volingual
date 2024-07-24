from sklearn.model_selection import train_test_split


def add_period_if_missing(string):
    """Adds a period at the end of the string if not present."""
    if not string.endswith('.'):
        string += '.'
    return string


# Load data
f_en = open('./data/english_sentences.txt', 'r', encoding='utf-8').readlines()
f_nwh = open('./data/nweh_sentences.txt', 'r', encoding='utf-8').readlines()

# Check if both files have the same number of lines
assert len(f_en) == len(f_nwh), "The number of sentences in both files should be the same."

# Split the data into training and testing sets
train_en, test_en, train_nweh, test_nweh = train_test_split(
    f_en, f_nwh, test_size=0.2, random_state=42
)

# Write the test sets to files
with open('./data/test_en.txt', 'w', encoding='utf-8') as file_test_en:
    file_test_en.writelines(test_en)

with open('./data/test_nweh.txt', 'w', encoding='utf-8') as file_test_nweh:
    file_test_nweh.writelines(test_nweh)


# Write the training sets to files
with open('./data/train.txt', 'w', encoding='utf-8') as file_train:
    for (string1, string2) in zip(train_en, train_nweh):
        string1 = string1.lower().rstrip('\n')
        string2 = string2.lower().rstrip('\n')  # Preserve original Nweh text
        if '/' in string2:  # Check if there are alternative translations
            alternatives = string2.split('/')
            for alt in alternatives:
                file_train.write(f'{alt.strip()}\t{string1}\n')  # Write each alternative with the English sentence
        else:
            file_train.write(f'{string2}\t{string1}\n')

print("Data has been split into training and testing sets.")
