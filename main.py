import os
import time
import keyboard
import json
import subprocess

from tkinter import *
from tkinter.filedialog import askopenfilename

from pynimeapi import PyNime
api = PyNime()

if os.path.isfile("app.json") == False:
	print("Hai, ini pertama kalinya kamu buka aplikasi ini.")
	print("Saat dialog file picker muncul, silakan pilih lokasi media favorit kamu!")
	print("\n[Direkomendasikan menggunakan mpv atau vlc.]")
	print("Press enter to continue...")
	keyboard.wait("enter")

	with open("app.json", "w") as appjson:
		Tk().withdraw()
		media_player_filename = askopenfilename(
			title="Pilih lokasi media player (app.exe)",
			filetypes=[("Executable (*.exe)","*.exe")])
		
		json_dict = {
			'app_name' : f"{os.path.basename(media_player_filename)}",
			'app_location' : f"{media_player_filename}",
		}
		json_obj = json.dumps(json_dict)
		appjson.write(json_obj)
		appjson.close()

app_config = open("app.json")
app_json = json.load(app_config)
player_location = app_json['app_location']
app_config.close()

def recent_anime():
	os.system('cls')
	print("==========================.-=PyNime=-.============================")
	current_datetime = time.strftime(
		"%a, %d %b %Y %H:%M:%S",
		time.gmtime(1627987508.6496193)
		)
	print(f"      [{current_datetime}] - [20 Baru saja diuplad]\n")

	# print anime yang baru aja diupload
	recent_anime = api.get_recent_release(page=1)
	for anime in recent_anime:
		print(f"=> {anime.title} [EP: {anime.latest_episode}]")

	print("==========================.-=PyNime=-.============================")


def cari_anime(anime_title: str):
	anime_result_list = list()

	print(f"\n[*] Hasil pencarian dari '{anime_title}'")
	print("==================================================================")
	anime_result_list = api.search_anime(anime_title)

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

	anime_details = api.get_anime_details(anime_result_list[anime_choice].category_url)
	print("\n[Info Anime] =====================================================")
	print(f"Title \t: {anime_details.title}")
	print(f"Genres \t: {anime_details.genres}")
	print(f"Year \t: {anime_details.released}")
	print(f"Status \t: {anime_details.status}\n")
	print("[Pilih Episode] ==================================================")

	episodes = api.get_episode_urls(anime_result_list[anime_choice].category_url)

	for i, episode in enumerate(episodes):
	    print(f"[{i+1}] {episode}")

	while True:
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
	resolution = str(input("[>] Pilih resolusi video: "))
	print("Playing media...")
	subprocess.run("{} {}".format(player_location, stream_urls[resolution]))

	print("Ending seasion...")
	time.sleep(3)

while True:
	try:
		recent_anime()

		try:
			print("\n   Ketik 'search (judul anime)' untuk cari anime.")
			print("   Ketik 'schedule' untuk menampilkan jadwal minggu ini.")
			print("   Catatan: Di setiap input, ketik 'q' untuk kembali ke menu utama.")
			choice = input("\n[>] ")

			if choice[:6] == "search":
				cari_anime(choice[7:])
			
			if choice == "schedule":
				api.get_schedule(int(time.time()))
				print("Press enter to continue...")
				keyboard.wait("enter")

			if choice == "q":
				break

		except Exception as e:
			print("[ERROR] GOBLOG!")
			print(e)

			time.sleep(5)
			continue

	except Exception as e:
		print("Upss.. error kenapa nih?")
		print(e)

		time.sleep(5)
		raise SystemExit(0)
