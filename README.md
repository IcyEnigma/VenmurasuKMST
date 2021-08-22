# Documentation #
The Venmurasu Programming contest aims at creating a dataset of Tamil lines mapped to their English translations. The data provided in the contest was very raw and contained a lot of useful embedded cues which helped us map the Tamil and English texts. Although it was advised to drop one-to-many and many-to-one maps of the data, we deemed it essential to retain as much data as possible, and hence performed manual sentence alignment on the data. Our strategy is elucidated in upcoming sections.

# Steps we Followed #

The platform we used to code our process was Google colab. The following chronology was implemented:

1. Cloning the GitHub repository into our colab notebook.
2. Creating a function to load the files onto the notebook.
3. Copying file paths and loading file contents as <class 'str'> objects.
4. Carrying out a visual inspection of the data and determining the various cleaning operations to be done.
5. Program the functions for cleaning Tamil and English files.
6. Cleaning the files and storing them line-wise in separate .txt files.
7. Visualising the lengths of the prefinal files to assess manual alignment scope
8. Carrying out minor alignment operations to match the few lines in each file that do not exactly translate into each other.
9. Importing clean file pairs as Pandas dataframes to run it on different models.

## Step 1-3: Data Loading ##
To clone the GitHub repository, a simple line of code is sufficient:

```
!git clone https://github.com/venmurasu-programming-team/Aug2021-contest.git
```

The function we used for loading the data into our document is load_file:
```
def load_file(file_path):
 file = open(file_path,encoding = "utf8",mode = "rt")
 text = file.read()
 file.close()
 return text
```
Using the above function, we copied the path of the files from the colab file directory and paste it in the function. The function will then return the raw content of the selected section of the text. For example, to load the thirtieth files, we did:
```
eng30 = load_file("/content/Aug2021-contest/resources/Mahabharatha-Adiparva-Section30-en.txt")
tam30 = load_file("/content/Aug2021-contest/resources/Mahabharatha-Adiparva-Section30-ta.txt")
```
In this way, we can obtain strings of all the data files. While working on this project, we realised the confusion that these files can create; hence we advise against haphazardly naming the files.

## Step 4: Visual Inspection of Data ##
The next step is to analyse the data. Upon perusing the given files, we found some common features among English and Tamil files.

### Features Common to Tamil files ###
Tamil files have certain phrases within curly braces which serve as supplementary information for the reader. While this is essential, we cannot have them in the dataset as the English translations of these bits are not included in the English files.

Tamil files have some segregation faults. For example, the 28th file begins with the words “வினதையிடம் விடைபெற்று சென்ற கருடன்”. These might be words from the conclusion of the previous section, which was omitted for some reason from the data before sharing it with the contestants. Such minor phrases have been removed manually.

The Tamil text is filled with numbers with or without punctuation inside parantheses or square brackets; for example, (1), (13-15), etc. We guessed that these might correspond to the index of English lines translated. However, we did not find them helpful in segregation. From the point of view of comfort of coding, working with full stops and new line characters was easier. All these specific substrings were removed using regex line substitutions as these appeared in between lines and not towards the end.

There were numerous instances where a single line in Tamil extrapolates to multiple lines in the given English translation. Such things cannot be taken into account by a cleaning function, and hence such operations were performed manually.

### Features Common to English files ###
The English texts are all reasonably comfortable to work with when split by the new-line character.

All English files except the 26th file begin with two lines: 

SECTION x 
(Astika Parva continued)
where x is the roman numeral for the file number.

These two lines are just lines that help the reader navigate the book at ease. However, these lines do not feature in the Tamil texts. Hence, these lines have to be removed while cleaning. To do so, we exploited the fact that lines are separated by new-line characters. Upon splitting the text by new-line character, we can remove the first two redundant lines.
 
All English files end with the following line except the 25th file:
“So ends the xth section in the Astika Parva of the Adi Parva” (where x denotes the file number).
This line, similar to those in point 2 given above, also does not feature in corresponding Tamil files. Hence, we removed these as well.
For the 25th file, there is an additional “Footnotes” string that is redundant. Our cleaning function takes care of removing all the above four kinds of redundant lines.

The page number of the texts (as they appear in the book) appear intermittently throughout the text in the format “p.x”, where x denotes the page number. The page numbers were all separated by new-line characters and hence a simple loop would take care of eliminating them.

There were numerous stray quotes (both single and double) which were manually removed to enhance the quality of the cleaned data.	

In few English files, the abbreviation ‘i.e.’ occurs. While splitting by the period character, even ‘i.e.’ splits into two strings, which is meaningless. We replaced this with the expansion of the substring, i.e., ‘that is’.
## Step 5: Coding the Cleaning Functions ##
The function used to clean Tamil data follows the following strategy, elucidated using comments:
```
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
 ```

The function used to clean Tamil data follows the following strategy, elucidated using comments:
```
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
 ```
## Step 6: Cleaning Data and Making Files ##
Once the cleaning functions were coded, we used the following lines of code to create a new file in a drive folder and write the contents of the cleaned string list line by line into the file. The below code was implemented for the 28th sections (English and Tamil). The same can be used in a for loop to iterate through all the data at once.
```
e = open("/content/drive/MyDrive/PSG/Semester 3/Venmurasu/28eng.txt", "w")
for element in engfinal:
   e.write(element)
   e.write("\n")
   e.write("\n")
e.close()
t = open("/content/drive/MyDrive/PSG/Semester 3/Venmurasu/28tam.txt", "w")
for element in tamfinal:
   t.write(element)
   t.write("\n")
   t.write("\n")
t.close()
```
## Step 7: Analysis of Texts through Plots ##
In order to better understand the difference in text lengths between the corresponding files, we used the Matplotlib library.

Plot 1: Comparison of Text Length between English and Tamil Files after Cleaning
!["Plot 1"](https://user-images.githubusercontent.com/89002098/130358123-0ce01785-1eb2-4d20-aa09-141af5fca455.jpeg)

Plot 2: Comparison of Text Length between English and Tamil Files after Manual Alignment
!["Plot 2"](https://user-images.githubusercontent.com/89002098/130358123-0ce01785-1eb2-4d20-aa09-141af5fca455.jpeg)

## Step 8: Manual Text Alignment ##
The files cleaned using the functions given above were manually aligned to match many-to-one and one-to-many text maps. Text alignment in the file was also taken care of. Lines were combined when the split did not seem meaningful. When lines were too large, they were split to make input line size smaller. There is definitely scope to perform alignment this using code, however, the manual route was chosen in order to create scope for our discretion in cleaning.

# BLEU Scores
| File Number   | AI4Bharat Score | Google API Score  |
| :-----------: |:---------------:| :----------------:|
|   22   | 12.5520949323 | 4.3291404094 |
|   23   |  9.2366716239 | 5.5086336647 |
|   24   |  8.7663537944 | 5.5488030438 |
|   25   | 8.0910895196  | 6.3795514817 |
|   26   | 6.0639248459  | 6.2636153077 |
|   27   | 8.3077738101  | 5.4586633117 |
|   28   | 8.9566962699  | 6.023255213 |
|   29   | 10.1245218033 | 9.5862504336 |
|   30   | 10.6218278182 | 5.9720760755 |
|   31   | 6.8141839322  | 4.5305431969 |

### Average Scores ###
AI4Bharat : 8.953513834979999 <br />
Google API: 5.9600532138 <br />
