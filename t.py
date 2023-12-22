import client_con as cn

n = cn.Network('localhost', 48878)

while True:
    try:
        data = n.recv_data()
        print(data)
        if data == 'quit':
            break
    except KeyboardInterrupt:
        break

n.close()
