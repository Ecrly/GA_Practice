import matplotlib.pyplot as plt

def show_track(paths, tracks):
    color = ['r', 'g', 'b']
    for i in range(len(tracks)):
        track = tracks[i]
        path = paths[i]
        for j in range(len(track) - 1):
            point1, point2 = path[track[j]], path[track[j + 1]]
            plt.arrow(point1[0], point1[1], point2[0] - point1[0], point2[1] - point1[1],
                      head_width=1, length_includes_head=True, color=color[i])
    plt.show()
