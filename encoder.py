import cv2
import argparse
import tempfile
import os
import subprocess
import time
import zipfile
from multiprocessing import Pool

def encode(input_file, output_file):

	# clear the encode directory
	command = 'rm -rf encode/*'
	os.system(command)

	start = time.time()

	# get necessary video details
	vidcap = cv2.VideoCapture(input_file)
	frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
	fps = float(vidcap.get(cv2.CAP_PROP_FPS))
	vidcap.release()

	# create an archive
	zf = zipfile.ZipFile(output_file, mode='w')
	#open filewriting
	f = open('encode/encode.inf', 'w+')


	command = ['ffprobe', '-i', input_file, '-show_streams', '-select_streams', 'a', '-loglevel', 'error']
	p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	retval, _ = p.communicate()

	# extract video frames
	command = ['ffmpeg', '-loglevel', 'panic', '-i', input_file, '-codec:v', 'copy', 'encode/frame%d.jpg']
	subprocess.call(command)

	for i in range(1, (frame_count+1)):

		command = ['./lepton', 'encode/frame{}.jpg'.format(i), 'encode/frame{}.lep'.format(i)]
		subprocess.call(command)
		os.remove('encode/frame{}.jpg'.format(i))

		# put lepton frame into the archive
		zf.write('encode/frame{}.lep'.format(i), 'frame{}.lep'.format(i))
		os.remove('encode/frame{}.lep'.format(i))

	f.write('{}\n{}'.format(frame_count, fps))
	f.close()
	# store frames into archive
	zf.write('encode/encode.inf', 'encode.inf')
	os.remove('encode/encode.inf')

	# close the archive
	zf.close()

	end = time.time()

	return (end-start), fps, frame_count

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('input', help='path to the input file')
	parser.add_argument('output', help='path to the output file')
	args = parser.parse_args()

	input_file = args.input
	output_file = args.output
	encode(input_file, output_file)

if __name__ == "__main__":
    main()