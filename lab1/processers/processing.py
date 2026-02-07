import spacy
import json
from typing import List, Dict, IO
from docx import Document


class JsonProcesser:
    @classmethod
    def process_json(cls, file_path: str):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data


class Processer:
    @classmethod
    def process(
        cls, text: str, role_rules_path: str, morph_rules_path: str
    ) -> List[Dict[str, str]]:
        text = text.replace("\n", " ")
        model = spacy.load("en_core_web_md")
        doc = model(text)
        result_dict = []
        dep_rules = JsonProcesser.process_json(role_rules_path)
        morph_rules = JsonProcesser.process_json(morph_rules_path)
        for token in doc:
            morph = token.pos_
            if morph == "PUNCT" or morph == "SPACE":
                continue
            word = token.text
            lemma = token.lemma_
            dep = token.dep_
            role = dep_rules.get(dep, "Unknown Role")
            morphology = morph_rules.get(morph, "Unknown Morph")
            full_analisis = dict(word=word, lemma=lemma, morph=morphology, role=role)
            result_dict.append(full_analisis)

        return result_dict


class DocReader:
    @classmethod
    async def read_doc(cls, file: IO[bytes]):
        doc_file = Document(file)
        merged_text = " ".join([word.text for word in doc_file.paragraphs])
        return merged_text
