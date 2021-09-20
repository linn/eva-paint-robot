test = {'0001': {'left': 2, 'right': 1}, '0002': {'left': 3, 'right': 4}}

l_r = {'left': None, 'right': None}

test.update({'0003': {'left': 4, 'right': 5}})

print(test['0003'])