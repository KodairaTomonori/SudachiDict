import sys

from SudachiSynonym import Synonym


syn = Synonym("./src/main/text/synonyms.txt")
sys.argv.append("肝臓")
print(syn[sys.argv[1]])
