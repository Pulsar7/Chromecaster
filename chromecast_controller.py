"""
> Pulsar
> Python 3.8.2
"""
import pychromecast,os,sys
from pychromecast.controllers.youtube import YouTubeController
from time import sleep

command_seperator = ":"
commands = [
	"play-youtube",
	"forward",
	"pause",
	"play",
	"volume",
	"chromecast-info"
]

class YOUTUBE:
	def __init__(self,chromecast):
		self.yt = YouTubeController()
		chromecast.register_handler(self.yt)

	def play_video(self,ID):
		self.yt.play_video(ID)
		print(f'[+] Streaming video with the ID: {ID}')

def talk_with_chromecast(chromecast):
	state = True
	chromecast_controller = chromecast.media_controller
	while (state == True):
		try:
			command = input("Command> ")
			if (command_seperator in command):
				argumente = command.split(command_seperator)
				this_command = argumente[0].lower()
				if (this_command in commands):
					if (this_command == commands[0]):
						this_youtube = YOUTUBE(chromecast)
						this_youtube.play_video(argumente[1])
					if (this_command == commands[1]):
						try:
							anzahl = int(argumente[1])
							video_vorspulen(chromecast,anzahl)
						except Exception as error:
							pass
					if (this_command == commands[4]):
						try:
							requested_volume = float(argumente[1])
							chromecast.set_volume(requested_volume)
							sleep(1.1)
							print(f'[+] Volume-Level {chromecast.status.volume_level}')
						except Exception as error:
							pass
			elif (command == "close" or command == "exit"):
				raise KeyboardInterrupt
			elif (command.lower() == commands[2]):
				chromecast_controller.pause()
				print(f'[+] Stopped streaming.')
			elif (command.lower() == commands[3]):
				chromecast_controller.play()
				print(f'[+] Continued streaming.')
			elif (command.lower() == "clear" or command.lower() == "cls"):
				os.system("clear") #Linux
			elif (command.lower() == "help"):
				string_commands = ", ".join(commands)
				print(f'{string_commands}')
			elif (command.lower() == commands[5]):
				show_chromecast_info(chromecast)
		except KeyboardInterrupt:
			state = False

def video_vorspulen(chromecast,anzahl):
	chromecast.media_controller.seek(anzahl)
	print(f'[+] The video was fast-forwarded by {anzahl} seconds.')

def connect_to_chromecast(IP):
	status = True
	try:
		chromecast = pychromecast.Chromecast(IP)
		chromecast.wait()
	except Exception as error:
		chromecast = error
		status = False
	return (chromecast,status)

def suche():
	print(f'[*] Searching for Chromecasts in the area...')

	services, browser = pychromecast.discovery.discover_chromecasts()
	pychromecast.discovery.stop_discovery(browser)

	print(f'[+] The search is complete.')
	if (len(services) != 0):
		print(f'{services}')
	else:
		print(f'[!] Found no chromecast in your area [{services}]')

def show_chromecast_info(chromecast):
	print(f'''
		   ~* {chromecast.device.friendly_name} *~

		> [state]          %s
		> [host]            {chromecast_ip}
		> [manufacturer]      {chromecast.device.manufacturer}
		> [model]           {chromecast.device.model_name}
		> [Cast-Type]        {chromecast.device.cast_type}
		> [Volume-Level]      {chromecast.status.volume_level}
		> [Stand-By-State] {chromecast.status.is_stand_by}
		> [Display-Name]    {chromecast.status.display_name}
	'''%(chromecast.media_controller.status.player_state))

if (__name__ == '__main__'):
	os.system("clear") #Linux
	suche()
	chromecast_ip = input('Which chromecast to control?')
	if (chromecast_ip == "" or chromecast_ip == " "):
		chromecast_ip = '' #YOUR-IP
	(chromecast,status) = connect_to_chromecast(chromecast_ip)
	if (status == True):
		#print(chromecast)
		print(f'[+] Controlling chromecast with the IP {chromecast_ip}')
		#print(f'[+] Chromecast => {chromecast}')
		show_chromecast_info(chromecast)
		talk_with_chromecast(chromecast)
		print(f'\n[+] Streaming to {chromecast_ip} ({chromecast.device.friendly_name}) has stopped.')
	else:
		print(f'[!] Chromecast {chromecast_ip} is unreachable')
		answ = input("Looking for Chromecasts in the area?[y,n] ").lower()
		if (answ == "y"):
			suche()
		else:
			pass
	sys.exit()
