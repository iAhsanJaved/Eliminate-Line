import os
import re
import logging 


def load_files(folder_name):
    datafiles = []
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            if file.lower().endswith(".csv") or file.lower().endswith(".txt"):
                file_path = os.path.join(root, file)
                if "\__MACOSX\\" not in file_path:
                    datafiles.append(file_path)
        
    print("\tThere are {} csv/txt files".format(len(datafiles)))
    return datafiles

def make_result_dir(file_path):
    # extract filename from path 
    file_name = os.path.basename(file_path)
    # remove file name
    file_path = file_path.replace(file_name, '')
    # joint file path with result dir
    file_path = os.path.join('Result', file_path)
    # abspath
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        try:
            os.makedirs(file_path)
        except OSError:
            print("\tCreation of the directory %s failed" % file_path)
    return file_path


def eliminate_words(words, text):
    for word in words:
        pattern = re.compile(word, re.IGNORECASE)
        text = pattern.sub("", text)
    return text

def is_contain_stopwords(words, text):
    contain_words = []
    for word in words:
        if word in text.lower():
            contain_words.append(word)
    return contain_words



if __name__ == '__main__':
    folderName = input('Enter the folder name: ')
    # Check dir exists
    if not os.path.isdir(folderName):
        print('Error: "{}" folder does not exists.'.format(folderName))
        exit()

    wordFileName = input('Enter the words file name (stop_words.txt): ')
    # Check file exists
    if not os.path.isfile(wordFileName):
        print('Error: "{}" file does not exists.'.format(wordFileName))
        exit()
    
    # Load stoping words/strings
    words = []
    with open(wordFileName, "r", encoding="ISO-8859-1") as word_file:
        for word in word_file:
            word = (word.rstrip()).lower()
            words.append(word)
    if not words:
        print('Error: Word file "{}" is empty.'.format(wordFileName))
        exit()    

    # Load files
    print('Step-1: Loading all the files...')
    files = load_files(folderName)

    # Create and configure logger 
    logging.basicConfig(filename="info.log", 
                    format='%(message)s', 
                    filemode='w') 
    
    # Creating an object 
    logger = logging.getLogger() 

    #Setting the threshold of logger to DEBUG 
    logger.setLevel(logging.DEBUG) 

    # Processing
    print('Step-2: Processing each file one by one...')
    for file_path in files:
        file_name = os.path.basename(file_path)
        print('\tFile: {}'.format(file_path))

        # make result folder
        result_path = make_result_dir(file_path)

        file_content = ''
        # Read file
        with open(file_path, "r", encoding="ISO-8859-1") as input_file:
            for line_number, line in enumerate(input_file, start=1):
                contain_words = is_contain_stopwords(words, line)
                if contain_words:
                    msg = 'File: {0} | Line#{1} | Words: {2}'.format(file_name, line_number, contain_words)
                    logger.info(msg)
                    print('\t'+msg)
                else:
                    file_content = file_content + line
        
        # Read file
        result_path_file = file_path = os.path.join(result_path, file_name)
        with open(result_path_file, "w", encoding="ISO-8859-1") as out_file:
            out_file.write(file_content)        
