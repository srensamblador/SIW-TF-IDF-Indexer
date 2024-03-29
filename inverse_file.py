import math


class InverseFile:
    def __init__(self):
        self.terms = []

    def __str__(self):
        self.terms.sort(key=lambda t: t.idf)  # Prints it sorted by idf
        to_ret = ""
        for term in self.terms:
            to_ret += "Term: " + term.term + " IDF: " + str(term.idf) + " Post-list: "
            for document in term.post_list:
                to_ret += "\n\t* Doc_ID: " + document.id + " TF: " + str(document.tf)
            to_ret += "\n"
        return to_ret

    def contains(self, term):
        for t in self.terms:
            if t.term == term:
                return True
        return False

    def get_term(self, term):
        for t in self.terms:
            if t.term == term:
                return t
        return None

    def add_document(self, term, doc_id, doc_tf):
        """
            Adds a document to the post_list of the specified term. If the term is not present in the inverse_file yet
            it is created with the document added
        :param term:
        :param doc_id:
        :param doc_tf:
        :return:
        """
        if not self.contains(term):
            self.terms.append(Term(term))
        entry = self.get_term(term)
        entry.add_document(Document(doc_id, doc_tf))

    def calculate_idfs(self, corpus_size):
        """
            Calculates the IDF of the term
        :param corpus_size: total document count
        """
        for term in self.terms:
            term.calculate_idf(corpus_size)

    def set_idf(self, term, idf):
        """
        Used when loading from a file
        :param term:
        :param idf:
        :return:
        """
        for t in self.terms:
            if t.term == term:
                t.idf = idf

    def to_json(self):
        data = {"terms": []}
        for term in self.terms:
            data["terms"].append(term.to_json())
        return data


class Term:
    def __init__(self, term):
        self.term = term
        self.idf = 0
        self.post_list = []

    def add_document(self, document):
        self.append = self.post_list.append(document)

    def calculate_idf(self, corpus_size):
        """
            Using -log(number of documents where the term is present / total documents) to avoid DivBy0 if
            the term doesnt appear in any documents
        """
        self.idf = -math.log((len(self.post_list)) / corpus_size)

    def to_json(self):
        data = {"term": self.term, "idf": self.idf, "post_list": []}
        for doc in self.post_list:
            doc_data = {"id": doc.id, "tf": doc.tf}
            data["post_list"].append(doc_data)
        return data


class Document:
    def __init__(self, doc_id, tf):
        self.id = doc_id
        self.tf = tf
