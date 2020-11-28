# inspired from classification_tsv, an example from the allennlp repository
from typing import Dict, Iterable, List

import logging
from overrides import overrides
import itertools
import re

from allennlp.common.file_utils import cached_path
from allennlp.data import DatasetReader, Instance
from allennlp.data.fields import LabelField, TextField, SequenceLabelField, ArrayField
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer
from allennlp.data.tokenizers import Token, Tokenizer, WhitespaceTokenizer

import pandas as pd

logger = logging.getLogger(__name__)

def _is_divider(line: str) -> bool:
    empty_line = line.strip() == ""
    if empty_line:
        return True
    else:
        first_token = line.split()[0]
        if first_token == "-DOCSTART-":
            return True
        else:
            return False

@DatasetReader.register('semeval-reader')
class SemevalReader(DatasetReader):
    def __init__(self,
                 tokenizer: Tokenizer = None,
                 token_indexers: Dict[str, TokenIndexer] = None,
                 max_tokens: int = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.tokenizer = tokenizer or WhitespaceTokenizer()
        self.token_indexers = token_indexers or {'tokens': SingleIdTokenIndexer()}
        self.max_tokens = max_tokens

    def text_to_instance(self,
                         tokens: List[Token],
                         lang: List[str] = None,
                         tid: int = None,
                         sentiment: int = None) -> Instance:
        '''
        initial steps required:
        1. collect the 3 types of resources and create a big array which contains the data
        2. add all this info to instance_fields
        3. return an instance
        what's left?

        input:
            a lot of small fields of data, question is do we process it or not?
        output:
            an instance of the same
        taking inspiration from the allennlp conll2003 dataset reader

        '''
        # text_tokens = self.tokenizer.tokenize(text)
        sequence = TextField(tokens, self.token_indexers)
        if self.max_tokens:
            sequence = sequence[:self.max_tokens]
            lang = lang[:self.max_tokens]
        instance_fields: Dict[str, Field] = {"tokens": sequence}
        if lang is None:
                raise ConfigurationError(
                    "Dataset reader was specified to use language tags as "
                    "features. Pass them to text_to_instance."
                )
        instance_fields["lang"] = SequenceLabelField(lang, sequence)
        if tid is not None:
            instance_fields['tid'] = LabelField(tid)
        if sentiment is not None:
            instance_fields['labels'] = LabelField(sentiment)
        return Instance(instance_fields)

    @overrides
    def _read(self, file_path: str) -> Iterable[Instance]:
        '''

        '''
        # if `file_path` is a URL, redirect to the cache
        file_path = cached_path(file_path)

        with open(file_path, "r") as data_file:
            logger.info("Reading instances from lines in file at: %s", file_path)

            
                yield self.text_to_instance(tokens, lang[1:], tid, sentiment)


    # def _read(self, file_path: str) -> Iterable[Instance]:
    #     '''
    #     need to rewrite this function since this shit ain't workin bruh
    #     I think I'll preprocess and create a modified dataset after working with the csnli library
    #     basically that'll help in extracting / creating a better model, which may be used to learn a gan
    #     so let's see where we go with it

    #     '''
    #     with open(file_path, 'r') as lines:
    #         for line in lines:
    #             label_id, sentiment, text = line.strip().split('\t')
    #             yield self.text_to_instance(label_id, sentiment, text)


@DatasetReader.register('semeval-reader-2')
class SemevalReader2(DatasetReader):
    def __init__(self,
                 tokenizer: Tokenizer = None,
                 token_indexers: Dict[str, TokenIndexer] = None,
                 max_tokens: int = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.tokenizer = tokenizer or WhitespaceTokenizer()
        self.token_indexers = token_indexers or {'tokens': SingleIdTokenIndexer()}
        self.max_tokens = max_tokens

    def regex_processor(self, word: str):
        reg = r'[,\.\'\"\!]'
        answer = re.split(reg, word)
        return answer

    def strempty(self, word: str):
        if word == '':
            return True
        return False

    def text_to_instance(self,
                         tokens: List[Token],
                         lang: List[str] = None,
                         tid: int = None,
                         sentiment: int = None) -> Instance:
        '''
        input:
            tokens: a List of tokens of our input tweet
            lang: a list of language markers for each token of our input tweet
        output:
            an instance of the same
        taking inspiration from the allennlp conll2003 dataset reader

        '''
        # text_tokens = self.tokenizer.tokenize(text)
        sequence = TextField(tokens, self.token_indexers)
        if self.max_tokens:
            sequence = sequence[:self.max_tokens]
            lang = lang[:self.max_tokens]
        instance_fields: Dict[str, Field] = {"tokens": sequence}
        if lang is None:
                raise ConfigurationError(
                    "Dataset reader was specified to use language tags as "
                    "features. Pass them to text_to_instance."
                )
        for idx, element in enumerate(lang):
            # these labels correspond to the mask we use for the highlish embedder
            # NOTE we haven't processed user tags, hastags, and urls separately
            # but put them in eng for now
            if element == '1':
                lang[idx] = False
            else:
                lang[idx] = True
        instance_fields["lang"] = SequenceLabelField(lang, sequence)
        # if tid is not None:
        #     instance_fields['tid'] = LabelField(tid)
        if sentiment is not None:
            instance_fields['label'] = LabelField(sentiment)
        return Instance(instance_fields)

    @overrides
    def _read(self, file_path: str) -> Iterable[Instance]:
        # if `file_path` is a URL, redirect to the cache
        file_path = cached_path(file_path)

        with open(file_path, "r") as data_file:
            logger.info("Reading instances from lines in file at: %s", file_path)

            # Group into alternative divider / sentence chunks.
            for is_divider, lines in itertools.groupby(data_file, _is_divider):
                # Ignore the divider chunks, so that `lines` corresponds to the words
                # of a single sentence.
                if not is_divider:
                    fields = [line.strip().split() for line in lines]
                    # print(fields)
                    # at this point we need to do stuff to process user tags
                    # especially since the guys at semeval decided to not even process tweets
                    # properly

                    # user tag processing section
                    current_uid = None
                    current_user:str = None
                    bad_indexes = []
                    for idx, field in enumerate(fields):
                        # print(current_user)
                        if len(field) != 2:
                            bad_indexes.append(idx)
                            current_uid = None
                            current_user = None
                            # print(0)
                            continue
                        if field[1] == "User":
                            current_uid = idx
                            current_user = field[0]
                            # print(1)
                            continue
                        if current_user is not None:
                            # print(str("current_user: ") + current_user)
                            if field[0] == '_': # usernames having underscores have been separated sadly
                                current_user = current_user + "_"
                                bad_indexes.append(idx) #  removed the underscore
                                # print(1.5)
                                # print(current_user[-1])
                                continue
                            elif current_user[-1] == "_":
                                # print("YOLO")
                                current_user = current_user + field[0]
                                # print(current_user)
                                bad_indexes.append(idx) # removed the current word
                                if len(fields) > idx + 1:
                                    if fields[idx + 1][0] == '_':
                                        # basically our username has more underscores
                                        # print(2)
                                        continue
                                    else:
                                        fields[current_uid] = [current_user, "User"]
                                        current_uid = None
                                        current_user = None
                                        # print(3)
                                        continue
                                else:
                                    fields[current_uid] = [current_user, "User"]
                                    current_uid = None
                                    current_user = None
                                    # print(4)
                            else:
                                # print(current_user[-1])
                                current_uid = None
                                current_user = None
                    bad_indexes = [ele for ele in reversed(bad_indexes)]
                    for idx in bad_indexes:
                        fields.pop(idx)
                    # section for user tags over

                    # processing extra ... commas, quotation marks, exclamations etc
                    
                    # test_list = [[40, 1], ['hum', 0], ['dono...jaisa', 1], ['hai,', 1], ['...kaun', 0], ['yahan', 0], ['.', 2]]
                    # # print(fields)
                    # temp_list = test_list[1:]
                    # print(temp_list)
                    # replacement_list = []

                    # for idx, wordpair in enumerate(temp_list):
                    #     word, lang = wordpair
                    #     processed_words = self.regex_processor(word)
                    #     processed_words = [[x, lang] for x in processed_words if not self.strempty(x)]

                    #     replacement_list.append((idx, processed_words))
                    
                    # replacement_list = [ele for ele in reversed(replacement_list)]
                    # for idx, words in replacement_list:
                    #     test_list = test_list[:idx] + words + test_list[idx+1:]
                    # print(test_list)

                    mark = fields[0]
                    fields = fields[1:]
                    replacement_list = []
                    for idx, wordpair in enumerate(fields):
                        word, lang = wordpair
                        processed_words = self.regex_processor(word)
                        processed_words = [[x, lang] for x in processed_words if not self.strempty(x)]

                        replacement_list.append((idx, processed_words))
                    
                    replacement_list = [ele for ele in reversed(replacement_list)]
                    for idx, words in replacement_list:
                        fields = fields[:idx] + words + fields[idx+1:]
                    
                    fields.insert(0, mark)
                    # print(fields)
                    # unzipping trick returns tuples, but our Fields need lists
                    fields = [list(field) for field in zip(*fields)]
                    # print(fields)
                    try:
                        tokens_, lang = fields
                    except:
                        print(str(fields))
                    tid = tokens_[0]
                    sentiment = lang[0]
                    # TextField requires `Token` objects
                    tokens = [Token(token) for token in tokens_[1:]]

                    yield self.text_to_instance(tokens, lang[1:], tid, sentiment)
