import numpy as np 

__all__ = ('Face')


class Face:
	def __init__(self, face, shape, beauty):
		self.face = face
		self.shape = shape
		self.beauty = beauty

	def _difference(self, a, b): 
		'''Percentage difference between two independent quantities'''
		return 100 * min(a, b) / max(a, b)

	def _get_line(self, p1, p2):
		'''Line coeff ax+by+c=0 (by 2 points)'''
		x1, y1 = p1
		x2, y2 = p2
		a = 0 if x1 == x2 else 1 / (x2 - x1)
		b = 0 if y1 == y2 else 1 / (y1 - y2)             
		c = b * y1 + a * x1
		return a, b, -c

	def _length(self, p1, p2):
		'''Segment length (by 2 points)'''
		x1, y1 = p1
		x2, y2 = p2
		return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

	def _distance(self, p0, p1, p2):
		'''Distance between a line (by 2 points) and a point'''
		x0, y0 = p0
		a, b, c = self._get_line(p1, p2)
		return abs(a * x0 + b * y0 + c) / np.sqrt(a ** 2 + b ** 2)

	def _angle(self, p1, p2, p3, p4):
		'''Angle between lines (by 2 points)'''
		a1, b1, c1 = self._get_line(p1, p2)
		a2, b2, c2 = self._get_line(p3, p4)
		return 180 * np.arccos(abs(a1 * a2 + b1 * b2) / (np.sqrt(a1 ** 2 + b1 ** 2) * np.sqrt(a2 ** 2 + b2 ** 2))) / np.pi

	def get_beauty_score(self, language):
		'''Beauty score in %'''
		output_text = ['Красота', 'Beauty Score', 'Schönheitsgrad']
		return f'{output_text[language]}: {round(self.beauty, 2)}%'

	def get_eyes_param(self, language):
		'''The ratio of the width of the eye to its openness'''
		param_lang = ['Глаза: ', 'Eyes: ', 'Augen: ']
		round_lang = ['круглые', 'round', 'rund']
		almond_lang = ['миндалевидные', 'almond-shaped', 'mandelförmig']
		narrow_lang = ['суженные', 'narrow', 'schmal']

		eyes_avg_width = (self._length(self.shape[36], self.shape[39]) + self._length(self.shape[42], self.shape[45])) / 2
		openness_left = (self._length(self.shape[37], self.shape[41]) + self._length(self.shape[38], self.shape[40])) / 2
		openness_right = (self._length(self.shape[43], self.shape[47]) + self._length(self.shape[44], self.shape[46])) / 2
		openness = (openness_left + openness_right) / 2
		result = eyes_avg_width / openness

		if result < 2.4:
			return param_lang[language] + round_lang[language]
		elif result < 3.4:
			return param_lang[language] + almond_lang[language]
		else:
			return param_lang[language] + narrow_lang[language]

	def get_brows_param(self, language):
		'''Average angles of curvature of the eyebrows'''
		param_lang = ['Брови: ', 'Eyebrows: ', 'Augenbrauen: ']
		horizontal_lang = ['горизонтальные', 'horizontal', 'waagerecht']
		ascending_lang = ['восходящие', 'ascending', 'aufsteigend']
		bow_lang = ['дугообразные', 'bow-shaped', 'bogenförmig']
 
		left_brow_angle = self._angle(self.shape[17], self.shape[19], self.shape[19], self.shape[21])
		right_brow_angle = self._angle(self.shape[22], self.shape[24], self.shape[24], self.shape[26])
		avg_brow_angle = (left_brow_angle + right_brow_angle) / 2

		if avg_brow_angle < 20:
			return param_lang[language] + horizontal_lang[language]
		elif avg_brow_angle < 43:
			return param_lang[language] + ascending_lang[language]
		else:
			return param_lang[language] + bow_lang[language]

	def get_nose_param(self, language):
		'''The ratio of the width of the nose to the width of the eye 
		and the ratio of the length of the face to the length of the nose'''
		param_lang = ['Нос: ', 'Nose: ', 'Nase: ']
		short_lang = ['короткий', 'short', 'kurz']
		medium_lang = ['средний', 'medium', 'mittellang']
		long_lang = ['длинный', 'long', 'lang']

		narrow_lang = ['узкий', 'narrow', 'schmal']
		constricted_lang = ['суженный', 'constricted', 'eingeengt']
		wide_lang = ['широкий', 'wide', 'breit']

		face_length = self._distance(self.shape[8], self.shape[19], self.shape[24])
		nose_length = self._length(self.shape[27], self.shape[33])
		length_result = face_length / nose_length
		eyes_avg_width = (self._length(self.shape[36], self.shape[39]) + self._length(self.shape[42], self.shape[45])) / 2
		nose_width = self._length(self.shape[31], self.shape[35])
		width_result = eyes_avg_width / nose_width

		result = param_lang[language]
		if length_result < 2.4: 
			result += long_lang[language]
		elif length_result < 3.0:
			result += medium_lang[language]
		else: 
			result += short_lang[language]
		result += ', '
		if width_result < 0.9: 
			result += wide_lang[language]
		elif width_result < 1.0:
			result += constricted_lang[language]
		else: 
			result += narrow_lang[language]
		return result

	def get_lips_param(self, language):
		'''The ratio of lips width to lips length'''
		param_lang = ['Губы: ', 'Lips: ', 'Lippen: ']
		thin_lang = ['тонкие', 'thin', 'dünn']
		natural_lang = ['естественные', 'natural', 'natürlich']
		full_lang = ['пухлые', 'full', 'üppig']
		
		lips_width = self._length(self.shape[48], self.shape[54])
		lips_length = self._length(self.shape[62], self.shape[51]) + self._length(self.shape[57], self.shape[66])
		result = lips_width / lips_length

		if result < 3.0:
			return param_lang[language] + full_lang[language]
		elif result < 5.0:
			return param_lang[language] + natural_lang[language]
		else:
			return param_lang[language] + thin_lang[language]
	
	def get_chin_param(self, language):
		'''Chin sharpness angle'''    
		param_lang = ['Подбородок: ', 'Chin: ', 'Kinn: ']
		sharp_lang = ['острый', 'sharp', 'spitz']
		rounded_lang = ['закруглённый', 'rounded', 'abgerundet']
		square_lang = ['квадратный', 'square', 'quadratisch']
		chin_angle = self._angle(self.shape[6], self.shape[8], self.shape[8], self.shape[10])

		if chin_angle < 35:
			return param_lang[language] + square_lang[language]
		elif chin_angle < 50:
			return param_lang[language] + rounded_lang[language]
		else:
			return param_lang[language] + sharp_lang[language]

	def get_face_param(self, language):
		'''Face size ratio'''
		param_lang = ['Форма лица: ', 'Face shape: ', 'Gesichtsform: ']
		round_lang = ['окрулгая', 'round', 'rund']
		long_lang = ['вытянутая', 'long', 'lang']

		face_width = self._length(self.shape[0], self.shape[16]) 
		face_length = self._distance(self.shape[8], self.shape[19], self.shape[24])

		if face_width / face_length < 1.15:
			return param_lang[language] + long_lang[language]
		else:
			return param_lang[language] + round_lang[language]

	def get_smile_param(self, language):
		'''The difference between the curves of the upper and lower lips'''
		param_lang = ['Улыбка:', 'Smile:', 'Lächeln:']
		lower_curve = self._angle(self.shape[60], self.shape[66], self.shape[66], self.shape[64])
		upper_curve = self._angle(self.shape[60], self.shape[62], self.shape[62], self.shape[64])
		return f'{param_lang[language]} {round(lower_curve + 0.1 * upper_curve, 2)}%'


	def get_ratio_param(self, language):
		'''The length of the face divided by its width equals phi
		The width of the mouth divided by the width of the nose equals phi
		The distance between the pupils divided by the distance between the eyebrows equals phi'''
		param_lang = ['Золотое сечение:', 'Golden ratio:', 'Goldener Schnitt:']
		face_width = self._length(self.shape[0], self.shape[16]) 
		face_length = self._distance(self.shape[8], self.shape[19], self.shape[24])
		mouth_width = self._length(self.shape[48], self.shape[54])
		nose_width = self._length(self.shape[31], self.shape[35])
		pupils_distance = (self._length(self.shape[36], self.shape[45]) + self._length(self.shape[39], self.shape[42])) / 2
		eyebrows_distance = self._length(self.shape[21], self.shape[22])

		phi = (1 + 5 ** 0.5) / 2
		golden_ratio1 = self._difference(face_length / face_length, phi)
		golden_ratio2 = self._difference(mouth_width / nose_width, phi)
		golden_ratio3 = self._difference(pupils_distance / eyebrows_distance, phi)
		result = (golden_ratio1 + golden_ratio2 + golden_ratio3) / 3
		return f'{param_lang[language]} {round(result, 2)}%'


	def get_symmetry_param(self, language):
		'''The distance between the eyes should be equal to the nose width
		The distance between the eyebrows should be equal to the nose width
		The distance from a horizontal line, touching all the eyebrow tips to the 
		nose tip should be equal to the distance from the chin bottom to the nose tip'''
		param_lang = ['Симметрия:', 'Symmetry:', 'Symmetrie:']
		eyebrows_distance = self._length(self.shape[21], self.shape[22])
		eyes_distance = self._length(self.shape[39], self.shape[42])
		nose_width = self._length(self.shape[31], self.shape[35])
		eyebrows_to_nose = self._distance(self.shape[33], self.shape[21], self.shape[22],)
		chin_to_nose = self._length(self.shape[8], self.shape[33])

		ratio1 = self._difference(eyes_distance, nose_width)
		ratio2 = self._difference(eyebrows_distance, nose_width)
		ratio3 = self._difference(eyebrows_to_nose, chin_to_nose)
		result = (ratio1 + ratio2 + ratio3) / 3
		return f'{param_lang[language]} {round(result, 2)}%'

	def get_rotation_param(self, language):
		'''The ratio of the distances from the right and left temples to the middle of the nose'''
		param_lang = ['Поворот лица:', 'Face rotation:', 'Gesichtswende:']
		left_distance = self._length(self.shape[0], self.shape[27])
		right_distance = self._length(self.shape[16], self.shape[27])
		return f'{param_lang[language]} {round(100 - self._difference(left_distance, right_distance), 2)}%'

	def get_character_param(self, language):
		'''Relations (45 characters): eyes + eyebrows + lips -> character1; nose + chin + face -> character2'''
		param_lang = ['Характер:', 'Character:', 'Character:']
		rus_characters = {
		'narrowhorizontalthin': 'самодостаточный','narrowhorizontalnatural': 'серьёзный','narrowhorizontalfull': 'харизматичный',
		'narrowascendingthin': 'общительный','narrowascendingnatural': 'сентиментальный','narrowascendingfull': 'эмоциональный',
		'narrowbow-shapedthin': 'вспыльчивый','narrowbow-shapednatural': 'замкнутый','narrowbow-shapedfull': 'энергичный',
		'almond-shapedhorizontalthin': 'коммуникабельный','almond-shapedhorizontalnatural': 'скромный','almond-shapedhorizontalfull': 'сдержанный',
		'almond-shapedascendingthin': 'весёлый','almond-shapedascendingnatural': 'жизнерадостный','almond-shapedascendingfull': 'активный',
		'almond-shapedbow-shapedthin': 'оптимистичный','almond-shapedbow-shapednatural': 'интеллигентный','almond-shapedbow-shapedfull': 'терпеливый',
		'roundhorizontalthin': 'вежливый','roundhorizontalnatural': 'тихий','roundhorizontalfull': 'усидчивый',
		'roundascendingthin': 'уравновешенный','roundascendingnatural': 'раскованный','roundascendingfull': 'кропотливый',
		'roundbow-shapedthin': 'остроумный','roundbow-shapednatural': 'вежливый','roundbow-shapedfull': 'приветливый',
		'shortsharplong': 'настойчивый','shortsharpround': 'жертвенный','shortroundedlong': 'альтруистичный',
		'shortroundedround': 'заботливый','shortsquarelong': 'принципиальный','shortsquareround': 'находчивый',
		'mediumsharplong': 'изобретательный','mediumsharpround': 'доверчивый','mediumroundedlong': 'любознательный',
		'mediumroundedround': 'чуткий','mediumsquarelong': 'категоричный','mediumsquareround': 'сознательный',
		'longsharplong': 'проницательный','longsharpround': 'догадливый','longroundedlong': 'собранный',
		'longroundedround': 'храбрый','longsquarelong': 'хитрый','longsquareround': 'бесстрашный'
		}
		eng_characters = {
		'narrowhorizontalthin': 'independent','narrowhorizontalnatural': 'serious','narrowhorizontalfull': 'charismatic',
		'narrowascendingthin': 'communicative','narrowascendingnatural': 'sentimental','narrowascendingfull': 'emotional',
		'narrowbow-shapedthin': 'hot-tempered','narrowbow-shapednatural': 'closed','narrowbow-shapedfull': 'energetic',
		'almond-shapedhorizontalthin': 'sociable','almond-shapedhorizontalnatural': 'modest','almond-shapedhorizontalfull': 'restrained',
		'almond-shapedascendingthin': 'funny','almond-shapedascendingnatural': 'cheerful','almond-shapedascendingfull': 'active',
		'almond-shapedbow-shapedthin': 'optimistic','almond-shapedbow-shapednatural': 'intelligent','almond-shapedbow-shapedfull': 'patient',
		'roundhorizontalthin': 'polite','roundhorizontalnatural': 'quiet','roundhorizontalfull': 'plodding',
		'roundascendingthin': 'balanced','roundascendingnatural': 'uninhibited','roundascendingfull': 'painstaking',
		'roundbow-shapedthin': 'witty','roundbow-shapednatural': 'polite','roundbow-shapedfull': 'friendly',
		'shortsharplong': 'persistent','shortsharpround': 'sacrificial','shortroundedlong': 'altruistic',
		'shortroundedround': 'caring','shortsquarelong': 'principled','shortsquareround': 'resourceful',
		'mediumsharplong': 'inventive','mediumsharpround': 'confiding','mediumroundedlong': 'curious',
		'mediumroundedround': 'sensitive','mediumsquarelong': 'straight-out','mediumsquareround': 'conscious',
		'longsharplong': 'discerning','longsharpround': 'shrewd','longroundedlong': 'assembled',
		'longroundedround': 'brave','longsquarelong': 'cunning','longsquareround': 'fearless'
		}
		deu_characters = {
		'narrowhorizontalthin': 'selbständig','narrowhorizontalnatural': 'ernst','narrowhorizontalfull': 'charismatisch',
		'narrowascendingthin': 'gesprächig','narrowascendingnatural': 'sentimental','narrowascendingfull': 'emotional',
		'narrowbow-shapedthin': 'feurig','narrowbow-shapednatural': 'geschlossen','narrowbow-shapedfull': 'kräftig',
		'almond-shapedhorizontalthin': 'übertragbar','almond-shapedhorizontalnatural': 'bescheiden','almond-shapedhorizontalfull': 'zurückhaltend',
		'almond-shapedascendingthin': 'spaß','almond-shapedascendingnatural': 'heiter','almond-shapedascendingfull': 'aktiv',
		'almond-shapedbow-shapedthin': 'optimistisch','almond-shapedbow-shapednatural': 'intelligent','almond-shapedbow-shapedfull': 'geduldig',
		'roundhorizontalthin': 'höflich','roundhorizontalnatural': 'ruhig','roundhorizontalfull': 'fleißig',
		'roundascendingthin': 'ausgewogen','roundascendingnatural': 'hemmungslos','roundascendingfull': 'sorgfältig',
		'roundbow-shapedthin': 'witzig','roundbow-shapednatural': 'höflich','roundbow-shapedfull': 'freundlich',
		'shortsharplong': 'hartnäckig','shortsharpround': 'selbstlos','shortroundedlong': 'altruistisch',
		'shortroundedround': 'fürsorglich','shortsquarelong': 'prinzipiell','shortsquareround': 'einfallsreich',
		'mediumsharplong': 'erfinderisch','mediumsharpround': 'zutraulich','mediumroundedlong': 'neugierig',
		'mediumroundedround': 'empfindlich','mediumsquarelong': 'rigoros','mediumsquareround': 'bewusst',
		'longsharplong': 'schlau','longsharpround': 'klug','longroundedlong': 'konzentriert',
		'longroundedround': 'mutig','longsquarelong': 'gerissen','longsquareround': 'furchtlos'
		}
		characters_lang = [rus_characters, eng_characters, deu_characters]

		eyes_result = self.get_eyes_param(1).split(': ')[1]
		brows_result = self.get_brows_param(1).split(': ')[1]
		lips_result = self.get_lips_param(1).split(': ')[1]
		nose_result = self.get_nose_param(1).split(': ')[1]
		chin_result = self.get_chin_param(1).split(': ')[1]
		face_result = self.get_face_param(1).split(': ')[1]
		character1 = eyes_result + brows_result + lips_result
		character2 = nose_result.split(',')[0] + chin_result + face_result
		return f'{param_lang[language]} {characters_lang[language][character1]}, {characters_lang[language][character2]}'

	def get_beauty_percentage(self, language, face_idx):
		'''Assessing beauty by an adjective and calculating the percentage of uniqueness of appearance'''
		rus_mapping = {
			0: 'хуже некуда', 5: 'отвратительное', 10: 'страшное', 15: 'отталкивающее', 20: 'ужасное', 
			25: 'некрасивое', 30: 'неприятное', 35: 'заурядное', 40: 'невыразительное', 45: 'обыкновенное', 
			50: 'симпатичное', 55: 'милое', 60: 'интересное', 65: 'обаятельное', 70: 'привлекательное', 
			75: 'очаровательное', 80: 'красивое', 85: 'восхитительное', 90: 'великолепное', 95: 'ослепительное', 100: 'идеальное'
		}
		eng_mapping = {
			0: 'the worst', 5: 'disgusting', 10: 'freaky', 15: 'repulsive', 20: 'terrible', 
			25: 'unpretty', 30: 'unpleasant', 35: 'mediocre', 40: 'inexpressive', 45: 'ordinary', 
			50: 'cute', 55: 'sweet', 60: 'interesting', 65: 'lovely', 70: 'attractive', 
			75: 'charming', 80: 'beautiful', 85: 'delightful', 90: 'magnificent', 95: 'dazzling', 100: 'perfect'
		}
		deu_mapping = {
			0: 'das Schlimmste', 5: 'hässlich', 10: 'schrecklich', 15: 'widerlich', 20: 'abscheulich', 
			25: 'abstoßend', 30: 'unangenehm', 35: 'mittelmäßig', 40: 'abweisend', 45: 'gewöhnlich', 
			50: 'nett', 55: 'süß', 60: 'interessant', 65: 'sympatisch', 70: 'attraktiv', 
			75: 'charmant', 80: 'schön', 85: 'entzückend', 90: 'prächtig', 95: 'blendend', 100: 'ideal'
		}

		percentage = lambda x: 14.255 * np.e ** -(((x - 56) ** 2) / 392) # mu = 56, sigma = 14
		score = round(percentage(self.beauty), 2)
		key = round(0.2 * self.beauty) * 5

		if language == 0:
			return f'Лицо №{face_idx+1} - {rus_mapping[key]}! \nВ мире всего {score}% таких лиц (± 0.5% красоты):'
		elif language == 1:
			return f'Face №{face_idx+1} is {eng_mapping[key]}! \nThere are only {score}% faces like that in the world (± 0.5% beauty score):'
		elif language == 2:
			return f'Gesicht №{face_idx+1} ist {deu_mapping[key]}! \nEs gibt nur {score}% solcher Gesichter in der Welt (± 0.5% Schönheitsgrad):'

	def get_piechart_items(self, language, face_idx):
		'''Data for the piechart of the ratio of world beauty'''
		percentage = lambda x: 14.255 * np.e ** -(((x - 56) ** 2) / 392) # mu = 56, sigma = 14
		score = int(round(percentage(self.beauty)))
		if language == 0:
			return [{f'Лицо №{face_idx + 1}': score, 'Другие': 100 - score}]
		elif language == 1:
			return [{f'Face №{face_idx + 1}': score, 'Others': 100 - score}]
		elif language == 2:
			return [{f'Gesicht №{face_idx + 1}': score, 'Übrigen': 100 - score}]