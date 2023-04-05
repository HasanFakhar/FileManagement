from FileManager import *

fm = FileManager()

fm.create('file1')
fm.create('file2')
fm.mkdir('dir1')
fm.chdir('dir1')
fm.create('file3')

fo = fm.open('file1', 'w')
fo.write('hello')
fo.close()

fo = fm.open('file1', 'r')
print(fo.read())
fo.close()

fm.show_memory_map()
