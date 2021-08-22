#Function for loading files
def load_file(file_path):
    file = open(file_path,encoding = "utf8",mode = "rt")
    text = file.read()
    file.close()
    return text


#Function for cleaning tamil text
def tamil_clean(text):
    # Importing the regex library
    import re

    # Splitting by newline character "\n"
    tam_text = text.split("\n")

    # Iteratively search through each line for unwanted substrings and removing them
    for i in range(len(tam_text)):
        tam_text[i] = re.sub("{.*?}", "", tam_text[i]) # Text in curly braces
        tam_text[i] = re.sub("\[.*?\]", "", tam_text[i]) # Text in square braces
        tam_text[i] = re.sub(r"\(\d+\)", "", tam_text[i]) # Multiple digits
        tam_text[i] = re.sub(r'[0-9]', "", tam_text[i]) # Numbers in square braces
        tam_text[i] = re.sub("\(-\)", "", tam_text[i]) # Hyphens left after number cleaning
        tam_text[i] = re.sub(r'[()]', "", tam_text[i]) # Removing empty braces
        tam_text[i] = re.sub("\(,\)", "", tam_text[i]) # Removing commas within braces
        tam_text[i] = re.sub("\n", "", tam_text[i]) # Stray new-line characters
    # Removing newline characters or spaces in the end of the file
    if (tam_text[-1] == "\n") or (tam_text[-1] == ""):
        tam_text.remove(tam_text[-1])
    # Combining the entire text with spaces to imitate a proper paragraph
    final_text = "".join(tam_text)

    # Finally splitting my full stop to get individual sentences
    sentences = final_text.split(".")

    # Removing newline characters or spaces in the end of the file after new split
    if (sentences[-1] == "\n") or (sentences[-1] == ""):
        sentences.remove(sentences[-1])
    # Returning a list of clean sentences
    return sentences




#Function for cleaning english files
def english_clean(text):
    # Importing the regex library
    import re

    # Splitting by newline character "\n"
    list_text = text.split("\n")

    # Checking if the first 2 lines are redundant or not
    if list_text[0].split(" ")[0] == "SECTION":
        rem_two_lines = list_text[2:]
    else:
        rem_two_lines = list_text

    # Removing the page number strings
    for i in rem_two_lines:
        if i.split(". ")[0] == "p":
            rem_two_lines.remove(i)

    # Removing newline characters or spaces in the end of the file
    if((list_text[-1] == "\n") or (list_text[-1] == "")):
        rem_two_lines.remove(list_text[-1])

    # Combining the entire text with spaces to imitate a proper paragraph
    final_text = "".join(rem_two_lines)

    # Finally splitting my full stop to get individual sentences
    sentences = final_text.split(".")

    # Removing newline characters or spaces in the end of the file after new split
    if((sentences[-1] == "\n") or (sentences[-1] == "")):
        sentences.remove(sentences[-1])
    # Checking if the last word is "Footnotes"
    if (sentences[-1] == "Footnotes"):
        last_line = sentences[-2].split(" ") # Preparing for word check
        flag = 2
    else:
        last_line = sentences[-1].split(" ") # Preparing for word check
        flag = 1
    
    # Checking for the last redundant line
    if (last_line[-2] == "Adi"):
        sentences = sentences[:(-1*flag)] # flag helps us deal with the anomaly in file 25
    # Joining back the sentences as a paragraph
    a = ".".join(sentences)
    
    # Replacing i.e. with 'that is' to avoid extra period characters
    final_out = a.replace("i.e.", "that is")
    
    # Returning a list of clean sentences
    return final_out.split(".")
