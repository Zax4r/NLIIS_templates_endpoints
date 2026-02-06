import spacy
import json
from typing import List, Dict


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


res = Processer.process(
    """Lucas goes to school every day of the week. He has many subjects to go to each school day: English, art, science, mathematics, gym, and history. His mother packs a big backpack full of books and lunch for Lucas.

His first class is English, and he likes that teacher very much. His English teacher says that he is a good pupil, which Lucas knows means that she thinks he is a good student.

His next class is art. He draws on paper with crayons and pencils and sometimes uses a ruler. Lucas likes art. It is his favorite class.

His third class is science. This class is very hard for Lucas to figure out, but he gets to work with his classmates a lot, which he likes to do. His friend, Kyle, works with Lucas in science class, and they have fun.

Then Lucas gets his break for lunch. He sits with Kyle while he eats. The principal, or the headmaster as some call him, likes to walk around and talk to students during lunch to check that they are all behaving.""",
    "dep_rules.json",
    "morph_rules.json",
)

for w in res:
    print(w)
