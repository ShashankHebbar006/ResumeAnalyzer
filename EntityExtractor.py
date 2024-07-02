import fitz
import spacy
import os
import json

class EntityExtractor:
    def __init__(self, path) -> None:
        cwd = os.getcwd()
        self.path = os.path.join(cwd,path)

    # def list2str(self,list) -> str:
    #     print(", ".join(list))

    def extract_data(self):
        filepath = os.path.join(self.path,os.listdir(self.path)[0])
        pdf = fitz.open(filepath)
        resume_text = ''

        for page in pdf.pages():
            resume_text += page.get_text()

        nlp = spacy.load("en_cv_info_extr")
        doc = nlp(resume_text)
        dictionary = dict()
        dict_string = dict()

        # dictionary = {dictionary[ent.label_].append([]) if ent.label_ not in dictionary.keys() else dictionary[ent.label_].append(ent.text) for ent in doc.ents}
        for ent in doc.ents:
            if ent.label_ not in dictionary.keys():
                dictionary[ent.label_] = []
            dictionary[ent.label_].append(ent.text)

        for k,v in dictionary.items():
            dict_string[k] = ", ".join(v)

        return dict_string

# if __name__ == '__main__':
#     path = "uploads"

#     obj = EntityExtractor(path)
#     obj.extract_data()