with open(r'Photoface_dist\PhotofaceDB\1001\2008-02-23_12-21-31\LightSource.m', 'r') as f:
    data = f.read()
    info_light = data.split("[")[-1].split("]")[0].split(';')
    print((info_light))

