import matplotlib.pyplot as plt

paths = [[[25, 25], [40, 40], [45, 20], [25, 25]], [[25, 25], [10, 15], [20, 5], [15, 30], [25, 25]]]
tracks = [[0, 1, 2, 0], [0, 3, 1, 2, 0]]

plt.figure()
# for i in range(len(tracks[0]) - 1):
#     plt.plot(paths[0][tracks[0][i]], paths[0][tracks[0][i + 1]])
# plt.grid(True)
# plt.xlabel('x坐标')
# plt.ylabel('y坐标')
# plt.show()

a = [[25, 25], [40, 40], [45, 20], [25, 25]]
b = [0, 1, 2, 0]
x = []
y = []
color = ['r', 'g', 'b']
for i in range(len(tracks)):
    # x, y = [], []
    # for j in range(len(tracks[i])):
    #     x.append(paths[i][tracks[i][j]][0])
    #     y.append(paths[i][tracks[i][j]][1])
    # plt.plot(x, y)
    track = tracks[i]
    path = paths[i]
    for j in range(len(track) - 1):
        point1, point2 = path[track[j]], path[track[j + 1]]
        print(point1, point2)
        plt.arrow(point1[0], point1[1], point2[0] - point1[0], point2[1] - point1[1],
                  head_width = 1, length_includes_head = True, color = color[i])
# plt.arrow(0, 0, 10, 10, head_width=1)
plt.show()
