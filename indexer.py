from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from inverse_file import InverseFile
import string
import argparse
import serializer


def main(args):
    documents = load_documents(args.file)
    indexed = index(documents)
    serializer.dump_inverse_file(args.output, indexed)  # Serializes the inverse file to disk


def index(documents):
    """
        Indexes a list of documents and returns a InverseFile object
        :param documents: list of documents to index
    """

    inverse_file = InverseFile()

    # To give feedback about indexing progress
    processed_docs = 0
    curr_progress = 0

    for document in documents:
        document_id = "".join(document.split()[0:1])  # Gets Document ID
        document_text = " ".join(document.split()[1:])  # Gets Document text
        document_terms, word_count = extract_terms(document_text)  # Tokenizes the text
        for term in document_terms:
            # Adds a new document to the terms's postlist with given ID and TF for that term
            # Using normalized TF: term frequency / num of terms in document
            inverse_file.add_document(term, document_id, document_terms[term]/word_count)

        # For progress feedback
        processed_docs += 1
        if processed_docs/len(documents)*100 >= curr_progress:
            print("Indexing... (" + str(curr_progress) + "% complete)")
            curr_progress += 10

    # Once we have all terms and their postlists, we calculate the idf of each term
    inverse_file.calculate_idfs(len(documents))

    return inverse_file


def extract_terms(document):
    """
        Extracts a list of terms from a text, and its term count

    :param document: text to extract terms from
    :return: tuple containing (list of terms, word_count[excluding stopwords])
    """
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
    """
    Extracts a list of documents from the given file
    :param filename: file to read
    :return: list of documents
    """
    documents = []
    try:
        f = open(filename)
        for document in f:
            documents.append(document)
        return documents
    except:
        print("An error has happening processing the document file")


def parse_args():
    parser = argparse.ArgumentParser(description="Indexes a collection of documents")
    parser.add_argument("file", help="Document collection to index")
    parser.add_argument("-o", "--output", default="index.json", help="Output file")
    args = parser.parse_args()
    return args


main(parse_args())


