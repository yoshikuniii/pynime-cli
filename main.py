import os
import time
import json
import keyboard
import subprocess

from tkinter import *
from tkinter.filedialog import askopenfilename

from pynimeapi import PyNime
api = PyNime()


def app_configuration():
	''' Ini function untuk membuat file konfigurasi
		atau bisa juga untuk melakukan reset konfigurasi
	''' 
	print("Hai, ini pertama kalinya kamu buka aplikasi ini (atau me - reset settingan aplikasi).")
	print("Saat dialog file picker muncul, silakan pilih lokasi media favorit kamu!")
	print("\n[Direkomendasikan menggunakan mpv atau vlc.]")

	time.sleep(5)

	# nama file konfigurasinya adalah "app.json"
	with open("app.json", "w") as appjson:
		print("[~] Pilih lokasi media player...")

		Tk().withdraw()
		media_player_filename = askopenfilename(
			title="Pilih lokasi media player (app.exe)",
			filetypes=[("Executable (*.exe)","*.exe")])
		print(f"[!] Media player dipilih!\n    New location : {media_player_filename}")
		
		print("\n[~] Pilih default resolusi video.")
		print("[Very high: 1080, High: 720, Medium: 480, Low: 360]")
		video_res = input(" Very high, High, medium, or low? ")
		video_res = video_res.lower()

		json_dict = {
			'app_name' : f"{os.path.basename(media_player_filename)}",
			'app_location' : f"{media_player_filename}",
			'app_default_resolution' : f"{video_res}",
		}
		json_obj = json.dumps(json_dict)
		appjson.write(json_obj)
		appjson.close()


def recent_anime():
	''' Ini function untuk menampilkan anime yang baru saja diupload
		Simpelnya, ini menampilkan anime di halaman utama gogoanime.
		Cek dokumentasi library PyNime.
	''' 
	os.system('cls')
	print("==========================.-=PyNime=-.============================")
	current_datetime = time.strftime(
		"%a, %d %b %Y %H:%M:%S",
		time.localtime()
		)
	print(f"      [{current_datetime}] - [20 Baru saja diupload]\n")

	# print anime yang baru aja diupload
	recent_anime = api.get_recent_release(page=1)
	for anime in recent_anime:
		print(f"=> {anime.title} [EP: {anime.latest_episode}]")

	print("==========================.-=PyNime=-.============================")


def cari_anime(anime_title: str):
	''' Ini function untuk mencari anime
		Di akhir baris kode function ini, akan memutar video/streaming
		dari anime yang dicari.
	'''
	anime_result_list = list() # buat menyimpan list anime yang ditemukan

	print(f"[~] Hasil pencarian dari '{anime_title}'")
	print("==================================================================")
	anime_result_list = api.search_anime(anime_title)

	# jika tidak menemukan anime yang dicari, keluar dari fungsi
	if len(anime_result_list) == 0:
		print(f"[!] Anime '{anime_title}' gak ketemu!")
		print("Press enter to continue...")
		keyboard.wait("enter")
		return
	else:
		# print anime yang ditemukan
		for i, result in enumerate(anime_result_list):
			print(f"[{i}] {result.title}")

	while True:
		''' Ini loop untuk menerima input,
			menggunakan try except untuk handle error
		'''
		try:
			anime_choice = input(f"\n[>] Pilih anime [0-{len(anime_result_list)-1}]: ")

			if anime_choice == "q":
				return
			else:
				anime_choice = int(anime_choice)

			if (anime_choice > len(anime_result_list)-1) or (anime_choice < 0):
				print(f"[ERROR] Input diluar index! Pilih angka 0-{len(anime_result_list)-1}")
				continue
			else:
				break
		except:
			print("[ERROR] Input hanya menerima angka!")
			continue

	os.system("cls")
	anime_details = api.get_anime_details(anime_result_list[anime_choice].category_url)
	print("[Info Anime] =====================================================")
	print(f"Title \t: {anime_details.title}")
	print(f"Genres \t: {anime_details.genres}")
	print(f"Year \t: {anime_details.released}")
	print(f"Status \t: {anime_details.status}\n")
	print("[Pilih Episode] ==================================================")

	episodes = api.get_episode_urls(anime_result_list[anime_choice].category_url)

	for i, episode in enumerate(episodes):
	    print(f"[{i+1}] {episode}")

	while True:
		''' Ini loop untuk menerima input,
			menggunakan try except untuk handle error
		'''
		try:
			episode_choice = input(f"\n[>] Pilih episode [1-{len(episodes)}]: ")

			if episode_choice == "q":
				return
			else:
				episode_choice = int(episode_choice)

			if (episode_choice > len(episodes)) or (episode_choice < 1):
				print(f"[ERROR] Input diluar index! Pilih angka 1-{len(episodes)}")
				continue
			else:
				break
		except:
			print("[ERROR] Input hanya menerima angka!")
			continue

	os.system("cls")
	print(f"[~] Anime dipilih => {anime_details.title} - Episode {episode_choice}")
	stream_urls = api.get_stream_urls(anime_episode_url = episodes[episode_choice - 1])
	print(f"[?] Resolusi video tersedia {list(stream_urls.keys())}")

	key_list = list(stream_urls.keys())

	if len(key_list) == 3:
		key_list.append(max(key_list))

	sorted_key_list = [int(i) for i in key_list]
	sorted_key_list = sorted(sorted_key_list)

	if video_res == "very high":
		resolution = str(max(sorted_key_list))

	if video_res == "high":
		resolution = str(sorted_key_list[len(sorted_key_list)-2])

	if video_res == "medium":
		resolution = str(sorted_key_list[len(sorted_key_list)-3])

	if video_res == "low":
		resolution = str(sorted_key_list[len(sorted_key_list)-4])

	if video_res == "very low":
		resolution = str(min(sorted_key_list))

	print("Playing media...")
	subprocess.run("{} {}".format(player_location, stream_urls[resolution]))

	print("Closing media player...")
	time.sleep(3)

# check apakah file konfigurasi ada apa nggak
# kalo udah ada, load file konfigurasinya
# kalo gaada, buat konfigurasi baru
if os.path.isfile("app.json") == True:
	app_config = open("app.json")
	app_json = json.load(app_config)
	player_location = app_json['app_location']
	video_res = app_json['app_default_resolution']
	app_config.close()
else:
	app_configuration()
	app_config = open("app.json")
	app_json = json.load(app_config)
	player_location = app_json['app_location']
	video_res = app_json['app_default_resolution']
	app_config.close()

while True:
	''' Loop di sini bertindak sebagai menu aplikasi
	'''
	try:
		# print anime yang baru aja diupload
		recent_anime()

		try:
			print("\n   Ketik 'search (judul anime)' untuk cari anime.")
			print("   Ketik 'schedule' untuk menampilkan jadwal minggu ini.")
			print("   Ketik 'reset' untuk me-reset konfigurasi aplikasi.")
			print("   Catatan: Di setiap input, ketik 'q' untuk kembali ke menu utama.")
			choice = input("\n[>] ")
			choice = choice.lower()

			if choice[:6] == "search":
				cari_anime(choice[7:])
			
			if choice == "schedule":
				api.get_schedule()
				print("Press enter to continue...")
				keyboard.wait("enter")

			if choice == "reset":
				os.system("cls")
				app_configuration()

				# load kembali konfigurasi yang baru
				app_config = open("app.json")
				app_json = json.load(app_config)
				player_location = app_json['app_location']
				video_res = app_json['app_default_resolution']
				app_config.close()

			if choice == "q":
				break

		except Exception as e:
			print("Upss.. error kenapa nih?")
			print(e)

			time.sleep(5)
			continue

	except Exception as e:
		print("Upss.. error kenapa nih?")
		print(e)

		time.sleep(5)
		raise SystemExit(0)
