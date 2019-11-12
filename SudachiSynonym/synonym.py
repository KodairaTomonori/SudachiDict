import collections
from enum import IntEnum, auto

class Column(IntEnum):
  GROUP       = 0
  TYPE        = auto()
  STATUS      = auto()
  IDIOM_GROUP = auto()
  FORM        = auto()
  ABB_TYPE    = auto()
  STYLE       = auto()
  LABEL       = auto()
  LEMMA       = auto()
  EXT1        = auto()
  EXT2        = auto()

  
class Word():
  def __init__(self, line):
    columns = line.strip().split(",")
    self.group       = columns[Column.GROUP]
    self.type        = int(columns[Column.TYPE])
    self.status      = int(columns[Column.STATUS])
    self.idiom_group = set(map(int, columns[Column.IDIOM_GROUP].split("/")))
    self.form        = int(columns[Column.FORM])
    self.abb_type    = int(columns[Column.ABB_TYPE])
    self.style       = int(columns[Column.STYLE])
    self.label       = set(columns[Column.LABEL].strip("()").split("/"))
    self.lemma       = columns[Column.LEMMA]
    self.ext1        = columns[Column.EXT1]
    self.ext2        = columns[Column.EXT2]

  def __repr__(self):
    return f"<Word id={self.group} lemma={self.lemma}>"


class Synonym():
  def __init__(self, synonym_file=None):
    self.word2groups = collections.defaultdict(set)
    self.group2synonym = collections.defaultdict(set)
    if synonym_file is not None:
      self.load(synonym_file)
  
  def load(self, synonym_file):
    with open(synonym_file, 'r') as fin:
      for line in fin:
        if line.strip():
          word = Word(line)
          self.word2groups[word.lemma].add(word.group)
          self.group2synonym[word.group].add(word)

  def __getitem__(self, key):
    if isinstance(key, Word):
      key = key.lemma
    output = set()
    for group in self.word2groups[key]:
      output = output | self.group2synonym[group]
    return output
