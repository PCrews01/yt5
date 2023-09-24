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
@views.route('/', methods=['GET', 'POST'])
def home():
	video = ""
	title = ""
	thumb = ""
	videos = []
	titles = []
	links  = []

	def addVideo(vid):
		videos.append(vid)
		print(f"video count {len(videos)}")
		# print(f"video added {videos}")

	if request.method == 'POST':
		link = request.form.get('yt-link')
		if request.form.get('playlist') == "playlist":
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
						only_audio = yt_vid.streams.filter(only_audio=True)
						# audio_file = only_audio.get_audio_only().download(output_path=dl_folder)
						addVideo(yt_vid)
						print(f"Added {yt_vid.title}")
						links.append(audio_file)

					except exceptions.AgeRestrictedError:
						print(f" WOW {yt_vid.title} has an age restriction. ")

					except exceptions.VideoPrivate:
						print(f"Video is private")

				else:
					print(" No video found")
			# return render_template('home.html',kind="search", p_videos=enumerate(p_videos), v_count=len(p_videos))
		
		elif request.form.get('search') == "search":
			video_search = Search(link)
			print(f"Searcj {video_search.results}")
			search_result_links = video_search.results
			search_links = []
			search_videos = []
			
			try:
				if len(search_result_links) > 0:
					for vid in search_result_links:
						video = YouTube(vid.watch_url)
						title = video.title
						thumb = video.thumbnail_url
						video.streams.filter(only_audio=True)
						

						# SET DOWNLOAD FOLDER BASED ON OS
						if os.name == "nt":
							dl_folder = f"{os.getenv('USERPROFILE')}\\Downlads\yt5\{k.title}"
						else:
							dl_folder = f"{os.getenv('HOME')}/Downloads/yt5/{vid.title}"


						if search_result_links[0]:
							try:
								# yt_vid = YouTube(search_result_links[0].watch_url)
								only_audio = video.streams.filter(only_audio=True)
								if not videos.__contains__(video):
									addVideo(video)	
									print(f"Added {video.title}")

							except exceptions.AgeRestrictedError:
								print(f" WOW {video.title} has an age restriction. ")

							except exceptions.VideoPrivate:
								print(f"Video is private")

						else:
							print(" No video found")
					return render_template('home.html',kind="search", p_videos=enumerate(videos), v_count=len(videos))
			
			except exceptions.VideoUnavailable:
				print(f"Video unavailable")

		else:
			video = YouTube(link)
			title = video.title
			thumb = video.thumbnail_url
			video.streams.filter(only_audio=True)

			if video.age_restricted:
				print("Ager ")

			try:
				yt_vid = YouTube(video)

			except exceptions.AgeRestrictedError:
				
				print(f" WOW {yt_vid.title} has an age restriction. ")

			except exceptions.VideoPrivate:
				
				print(f"Video is private")

			if os.name == "nt":
				dl_folder = f"{os.getenv('USERPROFILE')}\\Downlads\yt5\{video.title}"
			else:
				dl_folder = f"{os.getenv('HOME')}/Downloads/yt5/{video.title}"

			only_audio = video.streams.filter(only_audio=True)
			audio_file = only_audio.get_audio_only().download(output_path=dl_folder)
			addVideo(video)
			
			links.append(audio_file)
			return render_template('home.html', kind="video", video=video, title=title, thumb=thumb)
	
	return render_template('home.html', kind="pre", video=video, videos=videos)
