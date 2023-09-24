from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import *
from website import DB
from base64 import b64encode
from pytube import YouTube, Playlist, Search, exceptions
from pytube.cli import on_progress
import sys
import os
import json
import random
views = Blueprint('views', __name__)
sys.setrecursionlimit(300)

title = ""
thumb = ""
videos = []
titles = []
links  = []

def addVideo(vid):
	# Add video to the video array
	videos.insert(0,vid)

@views.route('/', methods=['GET', 'POST'])
def home():
	# Check if the page load method is post
	if request.method == 'POST':

		# Create a variable using the value from the form input field
		link = request.form.get('yt-link')
		
		if request.form.get('kind') == "playlist":
			dl_folder = ""
			v_group = []
			k = Playlist(link)
			p_videos = k.videos
			for vid in p_videos:
				ln = YouTube(vid.watch_url)
				ld = ln.streams.filter(only_audio=True)
				titles.append(vid.title)
				if os.name == "nt":
					dl_folder = f"{os.getenv('USERPROFILE')}\\Downlads\yt5\{k.title}"
				else:
					dl_folder = f"{os.getenv('HOME')}/Downloads/yt5/{k.title}"

				yts = Search(f'{vid.title.replace("Video", "audio").replace("video", "audio")} official audio')
				
				if yts.results[0]:
					try:
						yt_vid = YouTube(yts.results[0].watch_url)

					except exceptions.AgeRestrictedError:
						print(f" WOW {yt_vid.title} has an age restriction. ")

					except exceptions.VideoPrivate:
						print(f"Video is private")

					else:
						only_audio = yt_vid.streams.filter(only_audio=True)
						audio_file = only_audio.get_audio_only().download(output_path=dl_folder)
						addVideo(yt_vid)
						print(f"Added {yt_vid.title}")
						links.append(audio_file)
				else:
					print(" No video found")
			return render_template('home.html',kind="playlist", p_videos=enumerate(p_videos), v_count=len(p_videos))
		
		elif request.form.get('kind') == "search":
			search_params = request.form.get("yt-link")
			yt_search = Search(search_params)
			search_results = yt_search.results
			
			# reverse the search results to display results in order
			reverse_search_results = search_results.__reversed__()

			# Iterate through the list of reversed search results 
			for video_result in reverse_search_results:

				# Try to add the video result to the videos array
				try:

					# Add video to videos array
					addVideo(video_result)
					
				# Throw exception if there is an error adding the video
				except exceptions.VideoUnavailable:
					print(f"there's been an error adding {video_result.title}")
					
				# If there is no error print a success message
				else:
					print(f"video success: {video_result.title}")
			
			# Return home view after adding videos to the videos array
			return render_template("home.html", kind="search", videos=enumerate(videos), video_count=len(videos))

		else:
			video = YouTube(link)
			title = video.title
			thumb = video.thumbnail_url
			video.streams.filter(only_audio=True)

			if video.age_restricted:
				print("Ager ")

			print(f"this is the video {video}")
			try:
			# 	yt_vid = YouTube(video)
				if os.name == "nt":
					dl_folder = f"{os.getenv('USERPROFILE')}\\Downlads\yt5\{video.title}"
				else:
					dl_folder = f"{os.getenv('HOME')}/Downloads/yt5/{video.title}"

				only_audio = video.streams.filter(only_audio=True)
				audio_file = only_audio.get_audio_only().download(output_path=dl_folder)
				addVideo(video)
				
				links.append(audio_file)

			except exceptions.AgeRestrictedError:
				
				print(f" WOW {yt_vid.title} has an age restriction. ")

			except exceptions.VideoPrivate:
				
				print(f"Video is private")

			return render_template('home.html', kind="video", video=video, title=title, thumb=thumb)
	
	return render_template('home.html', kind="pre")

@views.route("/songs/<id>")
def downloadSong(id):
	video = YouTube(f"https://youtube.com/watch?v={id}")
	title = video.title
	thumb = video.thumbnail_url
	video.streams.filter(only_audio=True)

	# Create download folder based on the user's operating system
	if os.name == "nt":
		dl_folder = f"{os.getenv('USERPROFILE')}\\Downlads\yt5\{video.title}"
	else:
		dl_folder = f"{os.getenv('HOME')}/Downloads/yt5/{video.title}"

	# Try to convert the video to audio 
	# then download the audio
	# add the video to the vidoes array
	try:
		only_audio = video.streams.filter(only_audio=True)
		audio_file = only_audio.get_audio_only().download(output_path=dl_folder)

		# Check if video is not already in video array
		if not videos.__contains__(video):
			# if video is not in the vidoe array add it
			addVideo(video)
	# Check for errores
	except:
		print(f"Error downloading {title}")
		return "Error"
	
	# If there are no errors add audio link to link array
	else:
		links.append(audio_file)
	
	return render_template("home.html", kind="search", videos=enumerate(videos))
