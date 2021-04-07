from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.app import platform
from kivy.clock import mainthread
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, ILeftBodyTouch
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
from kivymd.color_definitions import colors, palette
from akivymd.uix.piechart import AKPieChart
from akivymd.uix.imageview import AKImageViewer, AKImageViewerItem
from plyer import storagepath, filechooser

import os
import cv2
import webbrowser
import numpy as np
from threading import Thread
from requests.exceptions import ConnectionError
from app_languages import languages
from image_processing import Image


Window.size = (1080 / 3, 2280 / 3.5)
Window.fullscreen = False


class MainInterface(ScreenManager):
	'''Contains all screens and their settings as a ScreenManager'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.toolbar.md_bg_color = 1, 1, 1, 1
		self.toolbar.specific_text_color = 1, 1, 1, 1
		self.bottom_panel.panel_color = .27, .84, 1, 1

	def set_toolbar_color(self, color):
		self.toolbar.md_bg_color = color

	def set_toolbar_text_color(self, color):
		self.toolbar.specific_text_color = color

	def set_bottom_panel_color(self, color):
		self.bottom_panel.panel_color = color


class MenuScreen(BoxLayout):
	'''Contains Toolbars, HomeScreen, ImageScreen, SettingsScreen as vertical BoxLayout'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		

class HomeScreen(MDBottomNavigationItem):
	'''Contains HomeScreen content: titles, texts and icons which are displayed as a ScrollView'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.titles = None
		self.texts = None
		self.icons = [
			'rocket-home.png', 
			'phone-home.png', 
			'cog-home.png', 
			'beauty-home.png', 
			'face-home.png', 
			'photo-home.png'
		]

	def add_content(self, lang):
		'''Adds main content in the specified language to the HomeScreen'''
		self.home_content.clear_widgets()
		self.titles = languages[lang]['home_titles']
		self.texts = languages[lang]['home_texts']

		for tls, txs, ics in zip(self.titles, self.texts, self.icons):
			content = MDBoxLayout(
				adaptive_height=True, 
				orientation='vertical', 
				padding=[dp(25), dp(100)]
			)
			content.add_widget(
				MDLabel(
					text=txs, 
					size_hint=(1, None),
					height=dp(Window.height * .1),
					theme_text_color='Secondary'
				)
			)
			self.home_content.add_widget(
				MDExpansionPanel(
					icon='images/' + ics,
					content=content,
					panel_cls=MDExpansionPanelOneLine(text=tls)
				)
			)


class ImageScreen(MDBottomNavigationItem):
	'''Contains ImageScreen content: button for opening a file manager'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


class SettingsScreen(MDBottomNavigationItem):
	'''Contains content for choosing a theme and interface language'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.theme_colors = {}
		for name_theme in palette:
			self.theme_colors[name_theme] = get_color_from_hex(colors[name_theme]['500'])
		self.language_menu = None
		self.languages = [
			{'icon': 'images/rus.png', 'text': 'Русский'},
			{'icon': 'images/eng.png', 'text': 'English'},
			{'icon': 'images/deu.png', 'text': 'Deutsch'}
		]
		self.app = MDApp.get_running_app()

	def create_language_menu(self):
		'''Creates a language selection menu'''
		self.language_menu = MDDropdownMenu(
			caller=self.lang_chooser,
			items=self.languages,
			width_mult=4
		)
		self.language_menu.bind(on_release=self.set_language)

	def set_language(self, menu_instance, item_instance):
		'''Sets the selected interface language'''
		if item_instance.text == 'Русский':
			self.app.change_language(0)
		elif item_instance.text == 'English':
			self.app.change_language(1)
		elif item_instance.text == 'Deutsch':
			self.app.change_language(2)
		self.lang_chooser.set_item(item_instance.text)
		menu_instance.dismiss()

	def create_dev_dialog(self):
		'''Opens developer dialog by clicking developer button'''
		dialog = DeveloperDialog()
		dialog.dialog_title.text = languages[self.app.language]['developer']
		dialog.developer_name.text = languages[self.app.language]['kirill']
		dialog.open()

	def feedback(self, link):
		'''Opens feedback link by clicking feedback button'''
		webbrowser.open(link)

	def create_share_dialog(self):
		'''TODO: release in Play Market'''
		toast('Coming soon in Play Market')

	def create_rate_dialog(self):
		'''TODO: release in Play Market'''
		toast('Coming soon in Play Market')


class DeveloperDialog(ModalView):
	'''Developer dialog on the SettingsScreen'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def web_reference(self, link):
		'''Follows the specified link'''
		webbrowser.open(link)


class SpinnerScreen(BoxLayout):
	'''Contains SpinnerScreen content: spinner and text'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)


class BeautyScreen(Screen):
	'''Contains BeautyScreen content: 
	toolbar, image with detected faces, 
	appbar with face beauty params, 
	piechart and buttons 
	(zoom, select faces, manupulate mask, save results)'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.image_path = None
		self.input_image= None
		self.faces = None
		self.face_selection_icons = [
			'emoticon-outline', 'emoticon-cool-outline',
			'emoticon-excited-outline', 'emoticon-wink-outline',
			'emoticon-tongue-outline', 'emoticon-kiss-outline',
			'emoticon-lol-outline', 'emoticon-devil-outline',
			'emoticon-neutral-outline', 'baby-face-outline',
			'face-outline', 'face-woman-outline',
			'alien-outline', 'guy-fawkes-mask'
		] * 10
		self.image_viewer = None
		self.app = MDApp.get_running_app()

	def add_content(self):
		'''Adds main content to the BeautyScreen, called in builder'''
		self.piechart = AKPieChart(
			items=[{'0-100% \n~': 100}],
			order=False,
			pos_hint={'center_x': .5, 'center_y': .5}, 
			size_hint=[None, None],
			size=(dp(300), dp(300))
		)
		self.piechart_box.add_widget(self.piechart)
		self.piechart_box.add_widget(
			MDLabel(
				text='Powered by BeautyDeep', 
				halign='center', 
				theme_text_color='Secondary', 
				font_style='Caption'
			)
		)

	def create_face_menu(self):
		'''Creates a menu for selecting the current face to view its beauty params'''
		face_lang = languages[self.app.language]['face']
		face_menu_items = [{
			'icon': 'emoticon-happy-outline', 
			'text': f'{face_lang} № 1'
		}]
		faces_num = len(self.faces)
		if faces_num > 1:
			for i in range(faces_num - 1):
				face_menu_items.append({
					'icon': self.face_selection_icons[i], 
					'text': f'{face_lang} № {i+2}'
				})

		self.face_menu = MDDropdownMenu(
			caller=self.face_selection_button,
			items=face_menu_items,
			width_mult=4,
			max_height=300
		)
		self.face_menu.bind(on_release=self.close_face_menu)

	def close_face_menu(self, menu_instance, item_instance):
		'''Closes the menu, displays which face was selected and resets beauty params'''
		selected_face_idx = int(item_instance.text[-2:]) - 1
		selected_face = self.faces[selected_face_idx]
		self.set_beauty_params(selected_face, selected_face_idx)
		menu_instance.dismiss()
		if self.app.language == 0:
			toast(f'Выбрано лицо №{selected_face_idx + 1}')
		elif self.app.language == 1:
			toast(f'Face №{selected_face_idx + 1} selected')
		elif self.app.language == 2:
			toast(f'Gesicht №{selected_face_idx + 1} ausgewählt')
		
	def watermarking(self, original, watermark):
		'''Makes watermark on image'''
		(originalHeight, originalWidth) = original.shape[:2]
		original = np.dstack([original, np.ones((originalHeight, originalWidth), dtype="uint8") * 255])

		scale = 10
		rw = int(watermark.shape[1] * scale / 100)
		rh = int(watermark.shape[0] * scale / 100)
		dim = (rw, rh)
		watermarked = cv2.resize(watermark, dim, interpolation=cv2.INTER_AREA)
		(wH, wW) = watermarked.shape[:2]

		overlay = np.zeros((originalHeight, originalWidth, 4), dtype="uint8")
		overlay[10:10 + wH, 10:10 + wW] = watermarked
		final = original.copy()
		return cv2.addWeighted(overlay, 0.5, final, 1.0, 0, final)

	def save_results(self):
		'''Saves watermarked results into gallery'''
		logo = cv2.imread(self.app.APP_ROOT + '/images/logo-bg.png', cv2.IMREAD_UNCHANGED)
		im = self.input_image
		for obj in self.faces:
			cv2.rectangle(im, (obj.face[0], obj.face[1]),
				(obj.face[2], obj.face[3]), (0, 255, 0), 3)
			cv2.putText(im, f'Beauty: {round(obj.beauty, 2)}%',
				(obj.face[0], obj.face[3] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

			for (x, y) in obj.shape:
				cv2.circle(im, (x, y), 1, (255, 0, 0), 2)

		result = self.watermarking(im, logo)
		saving_path = self.app.DCIM + '/BeautyDeep/'
		if not os.path.exists(saving_path):
			os.mkdir(saving_path)
		cv2.imwrite(saving_path + os.path.basename(self.image_path), result)
		toast(languages[self.app.language]['results_saved'])

	def display_mask(self):
		'''Callback for button which shows or hides the mask on the image'''
		if self.mask_button.text == languages[self.app.language]['hide_mask']:
			self.set_image('output.jpg')
			self.mask_button.text = languages[self.app.language]['show_mask']
		else:
			self.set_image('mask-output.jpg')
			self.mask_button.text = languages[self.app.language]['hide_mask']
	
	@mainthread # image.reload() works only in mainthread
	def set_image(self, image_path):
		'''Replaces the current image with the specified'''
		self.image.source = image_path
		self.image.reload()
		self.image_viewer = ImageViewer(image_path)

	def set_beauty_params(self, face, face_idx):
		'''Replaces all beauty params of the current face with the specified one'''
		self.score.title = face.get_beauty_score(self.app.language)
		self.eyes_param.text = face.get_eyes_param(self.app.language)
		self.brows_param.text = face.get_brows_param(self.app.language)
		self.nose_param.text = face.get_nose_param(self.app.language)
		self.lips_param.text = face.get_lips_param(self.app.language)
		self.chin_param.text = face.get_chin_param(self.app.language)
		self.face_param.text = face.get_face_param(self.app.language)
		self.smile_param.text = face.get_smile_param(self.app.language)
		self.ratio_param.text = face.get_ratio_param(self.app.language)
		self.symmetry_param.text = face.get_symmetry_param(self.app.language)
		self.rotation_param.text = face.get_rotation_param(self.app.language)
		self.character_param.text = face.get_character_param(self.app.language)
		self.beauty_peacenatge.text = face.get_beauty_percentage(self.app.language, face_idx)
		self.piechart.items = face.get_piechart_items(self.app.language, face_idx)
		

class ImageViewer(Screen):
	'''Widget for enlarge the image on the BeautyScreen'''
	def __init__(self, image, **kwargs):
		super().__init__(**kwargs)
		self.viewer= AKImageViewer()
		self.viewer.add_widget(AKImageViewerItem(source=image))

	def open(self):
		'''Opens ImageViewer with current image on the BeautyScreen'''
		self.viewer.open()


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
	'''Widget with icon to the left'''
	pass


class BeautyDeepApp(MDApp):
	'''Contains main interface and application logic'''
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.store = JsonStore('config.json')
		if not self.store:
			self.store['user_config'] = {
				'theme_style': 'Light', 
				'theme_color': 'Pink', 
				'app_language': 1,
				'public_ip': 'http://192.168.0.102:5000'
			}
		self.language = self.store['user_config']['app_language']
		self.server_ip = self.store['user_config']['public_ip']
		self.APP_ROOT = os.path.abspath('')
		self.DCIM = self.get_dcim_path()

	def build(self):
		'''Prepares the application configurations and adds all content to the screens'''
		Builder.load_file('beauty_deep.kv')
		self.theme_cls.theme_style = self.store['user_config']['theme_style']
		self.theme_cls.primary_palette = self.store['user_config']['theme_color']
		self.main_interface = MainInterface()
		self.main_interface.set_toolbar_color(self.theme_cls.primary_color)
		self.change_language(self.language)
		self.main_interface.beauty_screen.add_content()
		self.main_interface.settings_screen.create_language_menu()
		return self.main_interface

	def on_start(self):
		'''Called when the app starts'''
		# self.fps_monitor_start()
		if platform == 'android':
			from android.permissions import request_permissions, Permission
			request_permissions([
				Permission.INTERNET,
				Permission.READ_EXTERNAL_STORAGE, 
				Permission.WRITE_EXTERNAL_STORAGE
			])

	def on_pause(self):
		'''Called when the app is on pause'''
		return True

	def on_resume(self):
		'''Called when the app is resume'''
		pass

	def on_stop(self):
		'''Called when the app is stopped'''
		try:
			os.remove('output.jpg')
			os.remove('mask-output.jpg')
		except:
			pass

	def get_dcim_path(self):
		'''Gets gallery directory path'''
		if platform == 'android':
			return storagepath.get_pictures_dir()  
		else: 
			return self.APP_ROOT

	def switch_theme_style(self):
		'''Changes the theme style of the application'''
		if self.theme_cls.theme_style == 'Dark':
			self.theme_cls.theme_style = 'Light'
			self.store.put(
				'user_config', 
				theme_style='Light',
				theme_color=self.theme_cls.primary_palette,
				app_language=self.language,
				public_ip=self.server_ip
			)
		else: 
			self.theme_cls.theme_style = 'Dark'
			self.store.put(
				'user_config', 
				theme_style='Dark', 
				theme_color=self.theme_cls.primary_palette,
				app_language=self.language,
				public_ip=self.server_ip
			)

	def switch_theme_color(self, color_name):
		'''Changes the theme color of the application'''
		self.theme_cls.primary_palette = color_name
		self.store.put(
			'user_config', 
			theme_style=self.theme_cls.theme_style, 
			theme_color=color_name, 
			app_language=self.language,
			public_ip=self.server_ip
		)

	def change_language(self, language):
		'''Changes the interface language of the entire app'''
		self.language = language
		self.store.put(
			'user_config', 
			theme_style=self.theme_cls.theme_style,
			theme_color=self.theme_cls.primary_palette,
			app_language=language,
			public_ip=self.server_ip
		)
		self.main_interface.home_screen.add_content(self.language)
		self.main_interface.settings_screen.light_label.text = languages[self.language]['light']
		self.main_interface.settings_screen.dark_label.text = languages[self.language]['dark']
		self.main_interface.settings_screen.style_label.text = languages[self.language]['theme_style']
		self.main_interface.settings_screen.color_label.text = languages[self.language]['theme_color']
		self.main_interface.settings_screen.language_label.text = languages[self.language]['choose_language']
		self.main_interface.settings_screen.lang_chooser.text = languages[self.language]['lang']
		self.main_interface.settings_screen.server_label.text = languages[self.language]['server']
		self.main_interface.settings_screen.about_label.text = languages[self.language]['about_us']
		self.main_interface.settings_screen.developer_label.text = languages[self.language]['developer']
		self.main_interface.settings_screen.feedback_label.text = languages[self.language]['feedback']
		self.main_interface.settings_screen.social_label.text = languages[self.language]['social']
		self.main_interface.settings_screen.share_label.text = languages[self.language]['share']
		self.main_interface.settings_screen.rate_label.text = languages[self.language]['rate']
		self.main_interface.spinner_screen.processing_label1.text = languages[self.language]['image_processing1']
		self.main_interface.spinner_screen.processing_label2.text = languages[self.language]['image_processing2']
		self.main_interface.beauty_screen.save_button.text = languages[self.language]['save_results']
		self.main_interface.beauty_screen.mask_button.text = languages[self.language]['hide_mask']

	def change_server_ip(self, ip):
		'''Changes server public ip (http://ip:port)'''
		self.server_ip = ip
		self.store.put(
			'user_config', 
			theme_style=self.theme_cls.theme_style,
			theme_color=self.theme_cls.primary_palette,
			app_language=self.language,
			public_ip=ip
		)

	def file_manager_open(self):
		'''Call plyer filechooser API to run a filechooser activity in given directory'''
		filechooser.open_file(
			path=self.DCIM,
			preview=True, 
			filters=[('Images', '*.jpg', '*.png', '*.svg', '*.bmp', '*.eps', '*.eic')],
			on_selection=self.select_path
		)

	def select_path(self, selection):
		'''Callback function for handling the selection response from activity.
		Selects a file, launch a spinner and starts image processing in a separate thread'''
		if selection:
			path = selection[0]
			if path[-3:].lower() not in ['jpg', 'png', 'svg', 'bmp', 'eps', 'eic']:
				toast(languages[self.language]['unsupported_format'])
			else:
				self.main_interface.current = 'spinner_screen'
				self.main_interface.beauty_screen.image_path = path
				Thread(target=self.get_faces).start()

	def set_current_screen(self, screen, *, with_reset=True):
		'''Goes to the specified screen. 
		Param with_reset resets BeautyScreen by default and deletes temporary images'''
		self.main_interface.current = screen
		if with_reset and self.main_interface.beauty_screen.image_path:
			try:
				os.remove('output.jpg')
				os.remove('mask-output.jpg')
			except: 
				pass
			self.main_interface.beauty_screen.image_path = None
			self.main_interface.beauty_screen.input_image = None
			self.main_interface.beauty_screen.image_viewer = None
			self.main_interface.beauty_screen.mask_button.text = languages[self.language]['hide_mask']

	def get_faces(self):
		'''Recognizes and processes the image with a neural network and goes to the BeautyScreen'''
		try:
			im = Image(self.main_interface.beauty_screen.image_path)
			self.main_interface.beauty_screen.input_image = im.image.copy()
			im.send_request(self.server_ip)
			im.create_output(mask=False)
			im.create_output(mask=True)
			self.main_interface.beauty_screen.set_image('mask-output.jpg')
			self.main_interface.beauty_screen.set_beauty_params(im.faces[0], 0)
			self.main_interface.beauty_screen.faces = im.faces
			self.main_interface.beauty_screen.create_face_menu()
			self.main_interface.current = 'beauty_screen'
		except ValueError:
			toast(languages[self.language]['small_resolution'])
			self.set_current_screen('menu_screen')
		except ConnectionError:
			toast(languages[self.language]['server_off'])
			self.set_current_screen('menu_screen')
		except Exception as e:
			print(e)
			toast(languages[self.language]['not_recognized'])
			self.set_current_screen('menu_screen')



if __name__ == '__main__':
	BeautyDeepApp().run()