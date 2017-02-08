#!/usr/bin/env python

import argparse
import random

# Add more types of words to try to make sensible sentences
CONJUNCTIONS = ('and', 'or', 'but', 'as', 'yet', 'although', 'because', 'unless', 'until')
ARTICLES = ('the', 'a', 'one', 'some', 'few', 'many', 'several')
PREPOSITIONS = ('about', 'among', 'before', 'after', 'during', 'except', 'near', 'over')
ADVERBS = ('very', 'often', 'quickly', 'really', 'usually', 'almost', 'generally', 'never', 'finally', 'constantly')

def parse_wordfile(filename):
    file = open(filename)
    return file.readline().split(',')

def use_percentage(percent):
    choice = choose_from_range(1, 100)
    if choice <= percent:
        return True
    return False

def choose_word(words):
    return random.choice(words)

def choose_from_range(start, end):
    return random.randint(start, end) 

class ParagraphBuilder(object):
    def __init__(self, nouns, verbs, adjectives, conjunctions, articles, prepositions, adverbs):
        self.nouns = nouns
        self.verbs = verbs
        self.adjectives = adjectives
        self.conjunctions = conjunctions
        self.articles = articles
        self.prepositions = prepositions
        self.adverbs = adverbs

    def _build_noun(self, use_article_percentage=70):
        noun = []
        if use_percentage(use_article_percentage):
            noun.append(choose_word(self.articles))

        adjectives = choose_from_range(0, 2)
        for i in range(adjectives):
            noun.append(choose_word(self.adjectives))

        noun.append(choose_word(self.nouns))
        return " ".join(noun)

    def _build_verb(self):
        verb = []
        adverbs = choose_from_range(0, 2)
        for i in range(adverbs):
            verb.append(choose_word(self.adverbs))

        verb.append(choose_word(self.verbs))
        return " ".join(verb)

    def _build_standard_phrase(self):
        words = []

        words.append(self._build_noun())
        words.append(self._build_verb())
        if use_percentage(50):
            words.append(self._build_noun(use_article_percentage=100))
        return " ".join(words)

    def _build_prepositional_phrase(self):
        words = []

        words.append(choose_word(self.prepositions))
        words.append(self._build_noun(use_article_percentage=100))
        words.append(self._build_verb())
        words.append(self._build_noun(use_article_percentage=100))
        return " ".join(words)

    def _build_sentence(self):
        # Choose number of phrases in this sentence
        num_phrases = choose_from_range(1, 3)
        phrases = []
        for i in range(num_phrases):
            if use_percentage(60):
                phrases.append(self._build_standard_phrase())
            else:
                phrases.append(self._build_prepositional_phrase())
        
        if use_percentage(70):
            sentence = ", {} ".format(choose_word(self.conjunctions)).join(phrases)
        else:
            sentence = ", ".join(phrases)
        sentence += ". "
        sentence = sentence.capitalize()
        return sentence

    def build_paragraph(self, sentences_per_paragaph):
        return [self._build_sentence() for sentence in range(sentences_per_paragaph)]

def parse_args():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='''
    ./filter_log.py --noun-file <filename> --verb-file <filename> --adjective-file <filename> --paragraphs <int> --sentences-per-paragaph <int>
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--noun-file", default="./EssayMonkeyNouns.txt", help="Nouns to do use in the essay")
    parser.add_argument("--verb-file", default="./EssayMonkeyVerbs.txt", help="Verbs to do use in the essay")
    parser.add_argument("--adjective-file", default="./EssayMonkeyAdjectives.txt", help="Verbs to do use in the essay")
    parser.add_argument("--paragraphs", default=5, type=int, help="Number of paragraphs to generate")
    parser.add_argument("--sentences-per-paragraph", default=5, type=int, help="Number of sentences to generate")
    return parser.parse_args()

def main():
    args = parse_args()

    nouns = parse_wordfile(args.noun_file)
    verbs = parse_wordfile(args.verb_file)
    adjectives = parse_wordfile(args.adjective_file)

    paragraph_builder = ParagraphBuilder(nouns, verbs, adjectives, CONJUNCTIONS, ARTICLES, PREPOSITIONS, ADVERBS)
    paragraphs = [paragraph_builder.build_paragraph(args.sentences_per_paragraph) for paragraph in range(args.paragraphs)]
    for paragraph in paragraphs:
        print "\t" + "".join(paragraph)

if __name__ == "__main__":
    main()