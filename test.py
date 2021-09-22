test_list = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
numbered = []

for i, word in enumerate(test_list):
    numbered.append(f'{i+1}. {test_list[i]}')

print(numbered)
