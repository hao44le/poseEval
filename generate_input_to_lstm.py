import os

wav_file = "../TownCentreXVID.avi"


def generate_small_batch(start,duration):
    os.system("ffmpeg -i {} -ss {} -t {} -async 1 -c copy videos/{}.avi".format(wav_file,str(start),str(duration),str(start)+"_"+str(duration+start)))

duration = 20
for i in range(0,100,20):
    generate_small_batch(i,duration)
