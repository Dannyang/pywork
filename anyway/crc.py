def crc(data1, data2):
    original = data2
    # data1是根据多项式获得的除数，data2是元数据
    for i in range(len(data1) - 1):
        data2 = data2 + '0'
    print(data2)
    index = data2.find('1')
    # 被除数
    s = data2[index:]
    length = len(data1)
    while s.find('1') != -1 and len(s) >= length:
        a1 = s[:length]
        # 将结果转换回二进制字符串，并去掉前面的 '0b'
        temp = bin(int(a1, 2) ^ int(data1, 2))[2:]
        s = temp + s[length:]
    # zfill向左填充0,ljust向右填充0
    # 冗余码需要填充到长度为多项式阶数，没有则往左补0
    s = s[s.find('1'):].zfill(length - 1)
    print(original + s)


crc('10011', '1101')
