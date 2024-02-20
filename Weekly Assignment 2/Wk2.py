'''
Create a file called "ingest_this.txt" with the follwoing text:
This script
Is completely awesome
Like professor chaja

Import the file and print on the console and replace vowel with the number '7'
ex: "This" would be "Th7s"
'''
def replace_with_7(text):
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    for char in text:
        if char in vowels:
            text = text.replace(char, '7')
    return text

text_file = open("Weekly Assignment 2\ingest_this.txt")
text = text_file.read()

modified_text = replace_with_7(text)

print(modified_text)
text_file.close()