current_queue = {
    1: ('login1', 'name1'),
    2: ('login2', 'name2'),
    3: ('login3', 'name3')
}

number = len(current_queue)
current_queue[number + 1] = f'login{number+1}', f'name{number+1}'

print(current_queue)
