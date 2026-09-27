import os, sys

if __name__=='__main__':
    for filename in os.listdir('.'):
        if filename.endswith('.sok'):
            dir = filename[:-4]
            if not os.path.isdir(dir):
                os.mkdir(dir)
            levelno = 0
            with open( filename ) as f:
                levels = f.read().split('\n\n')
                for level in levels:
                    level = level.split('\nID:')[0].replace('-',' ')
                    lines = level.split('\n')
                    if lines[0].count('###'):
                        levelno +=1
                        with open( f'{dir}/level{levelno:03}.txt','w') as outf:
                            outf.write('\n'.join(lines) + '\n')
        elif filename.endswith('.ban'):
            dir = filename[:-4]
            if not os.path.isdir(dir):
                os.mkdir(dir)
            levelno = 0
            with open( filename ) as f:
                levels = f.read().split('\n\n')
                for level in levels[1:]:
                    if level[0] == ';':
                        continue
                    lines = level.split('\n')
                    levelno += 1
                    with open(f'{dir}/level{levelno:03}.txt', 'w') as outf:
                        outf.write('\n'.join(lines) + '\n')







