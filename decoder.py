import cv2
import argparse
import tempfile
import os
import subprocess
import time
import zipfile

def decode(input_file, output_file):

	# clear the decode directory
	command = "rm -rf decode/*"
	os.system(command)

	start = time.time()

	fname, fext = os.path.splitext(input_file)

	# open the mlep archive
	zf = zipfile.ZipFile(input_file)

	# get the necessary video details
	data = zf.read('encode.inf').decode("utf-8").split()
	frame_count = int(data[0])
	fps = float(data[1])

	for i in range(1, (frame_count+1)):

		# extract lepton frame
		zf.extract('frame{}.lep'.format(i), 'decode')

		# convert lepton frame to jpeg
		command = "./lepton decode/frame{}.lep decode/frame{}.jpg".format(i, i)
		os.system(command)
		os.remove("decode/frame{}.lep".format(i))

	command = ['ffmpeg', '-loglevel', 'panic', '-y', '-framerate', str(fps), '-i', 'decode/frame%d.jpg', '-an', '-codec:v', 'copy', str(output_file)]
	subprocess.call(command)

	# destroy jpeg frames
	command = 'rm -rf decode/*.jpg'
	os.system(command)

	# close the archive
	zf.close()

	end = time.time()

	return (end-start), fps, frame_count


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help="path to the input image")
	parser.add_argument("output", help="path to the output file")
	args = parser.parse_args()

	input_file = args.input
	output_file = args.output
	decode(input_file, output_file)


if __name__ == "__main__":
    main()