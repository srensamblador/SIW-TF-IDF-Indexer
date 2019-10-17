import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
from inverse_file import InverseFile
import serializer


def main():
    inverse_file = InverseFile()
    documents = load_documents("cran-queries.txt")
    for document in documents:
        document_id = "".join(document.split()[0:2])
        document_text = " ".join(document.split()[2:])
        document_terms, word_count = extract_terms(document_text)
        for term in document_terms:
            inverse_file.add_document(term, document_id, document_terms[term]/word_count)
    inverse_file.calculate_idfs(len(documents))

    serializer.dump_inverse_file("inverse_file.json", inverse_file)


def extract_terms(document):
    tokens = word_tokenize(document)
    stemmer = PorterStemmer()
    terms = {}  # Dictionary {term: appearances}
    word_count = 0  # To return total (meaningful) word count
    for token in tokens:
        token = token.lower()  # Lowercase
        token = token.strip(string.punctuation)  # Remove punctuation
        if token and token not in stopwords.words("english"):  # Remove stopwords
            token = stemmer.stem(token)  # Using Porter Stemmer
            if token not in terms:
                terms[token] = 1
            else:
                terms[token] += 1
            word_count += 1
    return terms, word_count


def load_documents(filename):
    documents = []
    try:
        f = open(filename)
        for document in f:
            documents.append(document)
        return documents
    except:
        print("An error has happening processing the document file")


#main()
serializer.load_inverse_file("inverse_file_serialized.json")

