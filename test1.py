import re

with open(r'Photoface_dist\PhotofaceDB\1001\2008-02-23_12-21-31\LightSource.m', 'r') as f:
    data = f.read()
    numbers = re.findall(r'\d+\.\d+|\d+', data)
    new_data = ''
    for number in numbers[1::2]:
        new_data += number + ' '
    with open('LightSource.txt', 'w') as f:
        f.write(new_data[:-1])
