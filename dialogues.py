# coding: utf-8
import nltk
from model import clear_phrase
from config import BOT_CONFIG
import random

def load_dialogues(filename='dialogues.txt'):
    with open(filename) as f:
        content = f.read()

    dialogues_str = content.split('\n\n')
    dialogues = [dialogue_str.split('\n')[:2] for dialogue_str in dialogues_str]
    dialogues_filtered = []
    questions = set()

    for dialogue in dialogues:
        if len(dialogue) != 2:
            continue

        question, answer = dialogue
        question = clear_phrase(question[2:])
        answer = answer[2:]

        if question != '' and question not in questions:
            questions.add(question)
            dialogues_filtered.append([question, answer])

    dialogues_structured = {}

    for question, answer in dialogues_filtered:
        words = set(question.split(' '))
        for word in words:
            if word not in dialogues_structured:
                dialogues_structured[word] = []
            dialogues_structured[word].append([question, answer])

    dialogues_structured_cut = {}
    for word, pairs in dialogues_structured.items():
        pairs.sort(key=lambda pair: len(pair[0]))
        dialogues_structured_cut[word] = pairs[:1000]

    return dialogues_structured_cut


dialogues_structured_cut = load_dialogues()


def generate_answer(replica):
    replica = clear_phrase(replica)
    words = set(replica.split(' '))
    mini_dataset = []
    for word in words:
        if word in dialogues_structured_cut:
            mini_dataset += dialogues_structured_cut[word]

    answers = []

    for question, answer in mini_dataset:
        if abs(len(replica) - len(question)) / len(question) < 0.2:
            distance = nltk.edit_distance(replica, question)
            distance_weighted = distance / len(question)
            if distance_weighted < 0.2:
                answers.append([distance_weighted, question, answer])

    if answers:
        return min(answers, key=lambda three: three[0])[2]


def get_failure_phrase():
    failure_phrases = BOT_CONFIG['failure_phrases']
    return random.choice(failure_phrases)


stats = {'intent': 0, 'generate': 0, 'failure': 0}


def bot(replica):
    from model import classify_intent, get_answer_by_intent

    intent = classify_intent(replica)
    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            stats['intent'] += 1
            return answer

    answer = generate_answer(replica)
    if answer:
        stats['generate'] += 1
        return answer

    stats['failure'] += 1
    return get_failure_phrase()
