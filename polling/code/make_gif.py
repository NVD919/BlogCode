import imageio
images = []
for i in range(14)[::-1]:
    images.append(imageio.imread('hist_'+str(i)+'.png'))
imageio.mimsave('movie.gif', images,duration=1.0)
