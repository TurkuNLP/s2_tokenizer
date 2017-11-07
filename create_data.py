import argparse
import sys
import re

CONLLU_COLCOUNT=10
ID,FORM,LEMMA,UPOS,XPOS,FEATS,HEAD,DEPREL,DEPS,MISC=range(CONLLU_COLCOUNT)

def trees(inp):
    """
    `inp` object yielding lines
    
    Yields the input a tree at a time.
    """
    comments=[] #List of comment lines to go with the current tree
    lines=[] #List of token/word lines of the current tree
    for line_counter, line in enumerate(inp):
        line=line.rstrip()
        if not line: #empty line
            if lines: #Sentence done, yield. Skip otherwise.
                yield comments, lines
                comments=[]
                lines=[]
        elif line[0]=="#":
            comments.append(line)
        else:
            cols=line.split("\t")
            assert len(cols)==CONLLU_COLCOUNT
            lines.append(cols)
    else: #end of file
        if comments or lines: #Looks like a forgotten empty line at the end of the file, well, okay...
            yield comments, lines

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='somestuff')
    parser.add_argument('OUTSRC',nargs=1,help="File name for src-side output")
    parser.add_argument('OUTTRG',nargs=1,help="File name for trg-side output")
    parser.add_argument('--max-seq-length',type=int,default=300,help="Max length")
    args = parser.parse_args()

    with open(args.OUTSRC[0],"w") as f_src, open(args.OUTTRG[0],"w") as f_trg:
        for comments,tree in trees(sys.stdin):
            text=[c for c in comments if c.startswith("# text =")][0]
            text=re.sub(r"^#\s*text\s*=\s*","",text)
            tokens=[cols[FORM] for cols in tree if cols[ID].isnumeric()]

            text=" ".join(c.replace(" ","<>") for c in text[:args.max_seq_length])
            tokens=[" ".join(t) for t in tokens][:args.max_seq_length]
            tokens=" <> ".join(tokens)
            if len(text)<2*args.max_seq_length and len(tokens)<2*args.max_seq_length:
                print(text,file=f_src)
                print(tokens,file=f_trg)
            
