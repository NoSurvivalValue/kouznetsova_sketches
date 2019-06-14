import os
import time
import ufal.udpipe
from ufal.udpipe import Model, Pipeline

# Класс модели для синтаксического парсера UDPipe

class Model:
    def __init__(self, path):
        """Load given model."""
        self.model = ufal.udpipe.Model.load(path)
        if not self.model:
            raise Exception("Cannot load UDPipe model from file '%s'" % path)

    def tokenize(self, text):
        """Tokenize the text and return list of ufal.udpipe.Sentence-s."""
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer")
        return self._read(text, tokenizer)

    def read(self, text, in_format):
        """Load text in the given format (conllu|horizontal|vertical) and return list of ufal.udpipe.Sentence-s."""
        input_format = ufal.udpipe.InputFormat.newInputFormat(in_format)
        if not input_format:
            raise Exception("Cannot create input format '%s'" % in_format)
        return self._read(text, input_format)

    def _read(self, text, input_format):
        input_format.setText(text)
        error = ufal.udpipe.ProcessingError()
        sentences = []

        sentence = ufal.udpipe.Sentence()
        while input_format.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)

        return sentences

    def tag(self, sentence):
        """Tag the given ufal.udpipe.Sentence (inplace)."""
        self.model.tag(sentence, self.model.DEFAULT)

    def parse(self, sentence):
        """Parse the given ufal.udpipe.Sentence (inplace)."""
        self.model.parse(sentence, self.model.DEFAULT)

    def write(self, sentences, out_format):
        """Write given ufal.udpipe.Sentence-s in the required format (conllu|horizontal|vertical)."""

        output_format = ufal.udpipe.OutputFormat.newOutputFormat(out_format)
        output = ''
        for sentence in sentences:
            output += output_format.writeSentence(sentence)
        output += output_format.finishDocument()

        return output

# Загрузка выбранной модели из файла

russian = Model('./models/russian-syntagrus-ud-2.0-170801.udpipe') 

# Функция для прогона одного файла через синтаксический парсер UDPipe без проведения морфологического анализа

def synt_parse(file, folder, new_folder):
    f = open(folder + file, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    result = russian.read(text, 'conllu')
    for r in result:
        #russian.tag(r)
        russian.parse(r)
    g = open(new_folder + file, 'w', encoding = 'utf-8')
    g.write(russian.write(result, 'conllu'))
    g.close()

# Функция для прогона одного файла через синтаксический парсер UDPipe с проведением морфологического анализа

def synt_parse_w_morph(file, folder, new_folder):
    f = open(folder + file, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    result = russian.read(text, 'conllu')
    for r in result:
        russian.tag(r)
        russian.parse(r)
    g = open(new_folder + file, 'w', encoding = 'utf-8')
    g.write(russian.write(result, 'conllu'))
    g.close()

# Функция для прогона всего корпуса через синтаксический парсер UDPipe без проведения морфологического анализа

def synt_parse_corpora(folder, new_folder):
    
    files = os.listdir(folder)
    for file in files:
        synt_parse(file, folder, new_folder)

# Функция для прогона всего корпуса через синтаксический парсер UDPipe с проведением морфологического анализа

def synt_parse_corpora_w_morph(folder, new_folder):
    
    files = os.listdir(folder)
    for file in files:
        synt_parse_w_morph(file, folder, new_folder)
