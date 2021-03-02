from pytube import YouTube
import sys
import argparse


def __download_video(link: str) -> bool:
	"""
	Method to download the video from youtube
	:param link: Link to the video
	:return: True if downloaded or False is exception occurred
	"""
	try:
		video = YouTube(link)
		video.streams.first().download()
		print("Video was Downloaded in the current Directory - {}".format(video.title))
	except Exception as e:
		print("Failed: Exception occured: \n {}".format(e))
		return False

	return True


def __download_audio(link: str) -> bool:
	"""
	Method to download the audio from youtube
	:param link: str link for the video
	:return: True if downloaded or False is exception occurred
	"""
	try:
		video = YouTube(link)
		video.streams.filter(only_audio=True).first().download()
		print("Audio was Downloaded in the current Directory - {}".format(video.title))
	except Exception as e:
		print("Failed: Exception occured: \n {}".format(e))
		return False
	return True


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--audio_only", help="Dowloads only the audio", action="store_true")
	parser.add_argument("-l", "--link", help="Link for the video")

	args = parser.parse_args()

	if not args.link:
		print("Please enter the link in the following format -> -l <link/url>")
	elif args.audio_only:
		__download_audio(args.link)
	else:
		__download_video(args.link)
	sys.exit(0)
