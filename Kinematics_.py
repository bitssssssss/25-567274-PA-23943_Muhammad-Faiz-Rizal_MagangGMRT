import numpy as np
import math
import matplotlib.pyplot as plt

def HEAD():
    print("\n0. Keluar")
    print("1. Kinematik DoF 2")
    print("2. Kinematik DoF ke-N")
    print("3. Kerangka DoF ke-N")
    print("4. Invers Kinematik DoF 2")

def Dof2():
    def kinematics(l1, l2, x, y):
        a = l1 * math.cos(x) + l2 * math.cos(x + y) 
        b = l1 * math.sin(x) + l2 * math.sin(x + y) 
        return a, b

    lengan1 = int(input("Masukkan l1 : "))
    lengan2 = int(input("Masukkan l2 : "))
    tetha1 = float(input("Masukkan sudut tetha 1: "))
    tetha2 = float(input("Masukkan sudut tetha 2: "))
    tetha1 = math.radians(tetha1)
    tetha2 = math.radians(tetha2)

    print(kinematics(lengan1, lengan2, tetha1, tetha2))




def Dofken():
    print("Masukkan berapa banyak DoF : ")
    a = int(input())

    rad = []
    deg = []
    leng = []

    for i in range(a):
        print(f"Masukkan sudut ke {i + 1}: ")
        deg.append(float(input()))
        print(f"Masukkan lengan ke {i + 1}")
        leng.append(float(input()))

    rad = [math.radians(r) for r in deg]

    def kinematics(x, y):
        h0 = np.matrix([
            [math.cos(x), -math.sin(x), 0],
            [math.sin(x),  math.cos(x), 0],
            [0, 0, 1]
        ])
        h1 = np.matrix([
            [1, 0, y],
            [0, 1, 0],
            [0, 0, 1]
        ])
        return h0 * h1

    sum = kinematics(rad[0], leng[0])
    for i in range(1, a):
        sum = sum * kinematics(rad[i], leng[i])

    return sum


def kerangkaDofkeN():
    print("Masukkan berapa banyak DoF : ")
    a = int(input())

    deg = []
    rad = []
    leng = []

    for i in range(a):
        print(f"Masukkan sudut ke {i + 1}: ")
        deg.append(float(input()))
        print(f"Masukkan lengan ke {i + 1}")
        leng.append(float(input()))

    rad = [math.radians(r) for r in deg]

    def Dofn():

        def kinematics(x, y):
            h0 = np.matrix([
                [math.cos(x), -math.sin(x), 0],
                [math.sin(x),  math.cos(x), 0],
                [0, 0, 1]
            ])
            h1 = np.matrix([
                [1, 0, y],
                [0, 1, 0],
                [0, 0, 1]
            ])
            return h0 * h1

        sum = kinematics(rad[0], leng[0])
        for i in range(1, a):
            sum = sum * kinematics(rad[i], leng[i])

        return sum

    print(Dofn())

    x = [0]
    y = [0]
    Radiant = 0

    for i in range(a):
        Radiant += rad[i]
        x.append(x[-1] + leng[i] * np.cos(Radiant))
        y.append(y[-1] + leng[i] * np.sin(Radiant))


    print("\nKoordinat Tiap Joint:")
    for i in range(len(x)):
        print(f"Joint {i}: ({x[i]:.2f}, {y[i]:.2f})")

    print(f"\nEnd Effector berada di: ({x[-1]:.2f}, {y[-1]:.2f})")

    plt.figure(figsize=(9, 9))
    colors = plt.cm.jet(np.linspace(0, 1, a)) 

    for i in range(a):
        plt.plot(
            [x[i], x[i+1]], [y[i], y[i+1]], 
            '-o', linewidth=6, color=colors[i],
            label=f'Link {i+1}'
        )

    for i in range(len(x)):
        label = 'Base' if i == 0 else (f'Joint {i}' if i < a else 'End Effector')
        plt.text(x[i], y[i], label, fontsize=10, ha='right')

    plt.show()

def inversdof2():
    x = float(input("Masukkan titik X akhir : "))
    y = float(input("Masukkan titik Y akhir : "))
    l1 = float(input("Masukkan lengan 1 : "))
    l2 = float(input("Masukkan lengan 2 : "))

    if((l1 < 0) or (l2 < 0)):
        print("Input nilai l1 dan l2 harus lebih besar dari 0")
        return

    r = math.sqrt((x**2 + y**2))
    if((r > (l1 + l2)) or r < (abs(l1 - l2))):
        print(f"Titik pada ({x}, {y}) tidak dapat dijangkau")
        return
    
    theta2 = math.acos((r - l1**2 - l2**2) / (2 * l1 * l2))
    theta1 = math.atan2(y, x) - math.atan2((l2*math.sin(theta2)), (l1 + l2 * math.cos(theta2)))

    print(f"sudut pertama adalah {math.degrees(theta1)} dengan panjang lengan {l1}")
    print(f"sudut pertama adalah {math.degrees(theta2)} dengan panjang lengan {l2}")    \
    

while True:
    HEAD()

    x = input("Masukkan pilihan : ")
    in_x = int(x)

    match in_x:
        case 0:
            break
        case 1:
            Dof2()
        case 2:
            Dofken()
        case 3:
            kerangkaDofkeN()
        case 4:
            inversdof2()