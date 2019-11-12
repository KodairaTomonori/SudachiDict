import MeCab

def include_alpha(w):
  return any(c.encode().isalnum() for c in w.replace(" ", ""))

def ja_to_en(w, hyokiyures):
  return (
    hyokiyures[0] == w or
    w.encode().isalnum()
  )


oyomip = MeCab.Tagger("-Oyomi").parse
def same_yomi(w, hyokiyures):
  return not include_alpha(w) and oyomip(hyokiyures[0]) == oyomip(w)


owakatip = MeCab.Tagger("-Owakati").parse
def one_word(w, hyokiyures):
  return not include_alpha(w) and owakatip(hyokiyures[0]).strip().count(" ") == 0

def ignore_english(w, hyokiyures):
  return not w.encode().isalnum()


def default_func(*arg):
  return True


def extract(key2hyokiyures, filter_func=default_func):
  output = list()
  for hyokiyures in key2hyokiyures.values():
    hyokiyures = [w for w in hyokiyures if filter_func(w, hyokiyures)]
    if len(hyokiyures) > 1:
      output.append(hyokiyures)
  return output


if __name__ == "__main__":
  import collections
  import os

  fname = "src/main/text/synonyms.txt"
  output_dir = os.path.dirname(fname)

  key2hyokiyures = collections.defaultdict(list)
  for line in open(fname):
     if not line.strip(): continue
     line = line.split(',')
     key = line[0], line[1], line[3]
     key2hyokiyures[key].append(line[-3])

  func2name = {
    "all": default_func,
    "no_en": ignore_english,
    "same_yomi": same_yomi,
    "ja_to_en": ja_to_en,
    "one_word": one_word
  }

  for name, func in func2name.items():
    output = extract(key2hyokiyures, filter_func=func)
    with open(os.path.join(output_dir, f"hyokiyure_{name}.csv"), 'w') as fout:
      fout.write("\n".join(sorted(",".join(hyokiyures) for hyokiyures in output)))
