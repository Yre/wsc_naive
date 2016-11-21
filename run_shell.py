import shlex, subprocess
from subprocess import call
import os
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
    # command_line = 'cp data/'+input_name+' stanford-corenlp-full-2015-12-09'
    # args = shlex.split(command_line)
    # print(args)
    # call(args)

    #args = ['java', '-cp', '"/csproject/comp5211/stanford-corenlp-full-2015-12-09/*"', '-Xmx2g',
    #        'edu.stanford.nlp.pipeline.StanfordCoreNLP', '-annotators', 'tokenize,ssplit,pos,lemma,ner,parse,dcoref',
    #        '-outputFormat', 'json', '-file', './data/' + input_name, '-outputDirectory', './data/']
    #print(args)
    #call(args)
    f = open("data/"+input_name,'r')
    print '************'
    for line in f:
        print line
        
    os.system("/csproject/comp5211/stanford-corenlp-full-2015-12-09/corenlp.sh -annotators tokenize,ssplit,pos,lemma,ner,parse, dcoref -outputFormat json -file data/"+input_name+" -outputDirectory data/")
    print "/csproject/comp5211/stanford-corenlp-full-2015-12-09/corenlp.sh -annotators tokenize,ssplit,pos,lemma,ner,parse, dcoref -outputFormat json -fi\
le data/"+input_name+" -outputDirectory data/" 
    #
    # command_line = 'mv '+input_name+'.json'+' data'
    # args = shlex.split(command_line)
    # print(args)
    # call(args)

#
# def install_Google_Scraper_shell():
#     command_line = 'virtualenv --python python3 env'
#     args = shlex.split(command_line)
#     print(args)
#     call(args)
#
#     command_line = 'source env/bin/activate'
#     args = shlex.split(command_line)
#     print(args)
#     call(args)
#     # pip install GoogleScraper ???
#
#
# def run_Google_Scraper_shell(word):
#     command_line = 'source env/bin/activate'
#     args = shlex.split(command_line)
#     print(args)
#     call(args)
