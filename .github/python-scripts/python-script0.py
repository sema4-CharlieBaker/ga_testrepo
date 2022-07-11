# try other strategy: pickling
import os
import pickle

print('hello from python')

cmd = '''
echo "action_state=yellow" >> $GITHUB_ENV
'''

os.system(cmd)




