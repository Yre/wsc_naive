import shlex, subprocess
from subprocess import call
#
# command_line = 'cd stanford-corenlp-full-2015-12-09'
# args = shlex.split(command_line)
# print(args)
# p = subprocess.Popen(args)
#
#
# command_line = 'cd stanford-corenlp-full-2015-12-09'
# args = shlex.split(command_line)
# print(args)
# call(args)
#
# command_line = 'ls'
# args = shlex.split(command_line)
# print(args)
# call(args)


def stanfordnlp_shell(input_name):
    # copy data/input.txt to stanford/input.txt
    command_line = 'cp data/'+input_name+' stanford-corenlp-full-2015-12-09'
    args = shlex.split(command_line)
    print(args)
    call(args)

    args = ['java', '-cp', '/Users/yre/Documents/_Yre_Boomshakalaka/2017_Fall/COMP_5211/wsc_naive/stanford-corenlp-full-2015-12-09/*', '-Xmx2g', 'edu.stanford.nlp.pipeline.StanfordCoreNLP', '-annotators', 'tokenize,ssplit,pos,lemma,ner,parse,dcoref', '-outputFormat', 'json', '-file', '/Users/yre/Documents/_Yre_Boomshakalaka/2017_Fall/COMP_5211/wsc_naive/data/'+input_name]
    print(args)
    call(args)

    command_line = 'mv '+input_name+'.json'+' data'
    args = shlex.split(command_line)
    print(args)
    call(args)
