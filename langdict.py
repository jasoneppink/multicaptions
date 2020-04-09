#!/usr/bin/python3
# -*- coding: utf-8 -*-

#ISO 639-2B Python dict
#3-character language codes matched to native language names
#from https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

langdict = {
	'aar': 'Afaraf',
	'abk': 'aҧсуа бызшәа',
	'afr': 'Afrikaans',
	'aka': 'Akan',
	'alb': 'Shqip', #ISO 639-2T: 'sqi'
	'amh': 'አማርኛ',
	'ara': 'العربية',
	'arg': 'aragonés',
	'arm': 'Հայերեն', #ISO 639-2T: 'hye'
	'asm': 'অসমীয়া',
	'ava': 'авар мацӀ',
	'ave': 'avesta',
	'aym': 'aymar aru',
	'aze': 'azərbaycan dili',
	'bak': 'башҡорт теле',
	'bam': 'bamanankan',
	'baq': 'euskara', #ISO 639-2T: 'eus'
	'bel': 'беларуская мова',
	'ben': 'বাংলা',
	'bih': 'भोजपुरी',
	'bis': 'Bislama',
	'bos': 'bosanski jezik',
	'bre': 'brezhoneg',
	'bul': 'български език',
	'bur': 'ဗမာစာ', #ISO 639-2T: 'mya'
	'cat': 'català',
	'cha': 'Chamoru',
	'che': 'нохчийн мотт',
	'chi': '中文', #ISO 639-2T: 'zho'
	'chu': 'ѩзыкъ словѣньскъ',
	'chv': 'чӑваш чӗлхи',
	'cor': 'Kernewek',
	'cos': 'corsu',
	'cre': 'ᓀᐦᐃᔭᐍᐏᐣ',
	'cze': 'čeština', #ISO 639-2T: 'ces'
	'dan': 'dansk',
	#'div': '?????',
	'dut': 'Nederlands', #ISO 639-2T: 'nld'
	'dzo': 'རྫོང་ཁ',
	'eng': 'English',
	'epo': 'Esperanto',
	'est': 'eesti',
	'ewe': 'Eʋegbe',
	'fao': 'føroyskt',
	'fij': 'vosa Vakaviti',
	'fin': 'suomi',
	'fre': 'français', #ISO 639-2T: 'fra'
	'fry': 'Frysk',
	'ful': 'Fulfulde',
	'geo': 'ქართული', #ISO 639-2T: 'kat'
	'ger': 'Deutsch', #ISO 639-2T: 'deu'
	'gla': 'Gàidhlig',
	'gle': 'Gaeilge',
	'glg': 'galego',
	'glv': 'Gaelg',
	'gre': 'ελληνικά', #ISO 639-2T: 'ell'
	'grn': "Avañe'ẽ",
	'guj': 'ગુજરાતી',
	'hat': 'Kreyòl ayisyen',
	'hau': 'هَوُسَ',
	'heb': 'עברית',
	'her': 'Otjiherero',
	'hin': 'हिन्दी',
	'hmo': 'Hiri Motu',
	'hrv': 'hrvatski jezik',
	'hun': 'magyar',
	'ibo': 'Asụsụ Igbo',
	'ice': 'Íslenska', #ISO 639-2T: 'isl'
	'ido': 'Ido',
	'iii': 'ꆈꌠ꒿',
	'iku': 'ᐃᓄᒃᑎᑐᑦ',
	'ile': 'Interlingue',
	'ina': 'Interlingua',
	'ind': 'Bahasa Indonesia',
	'ipk': 'Iñupiaq',
	'ita': 'italiano',
	#'jav': '????',
	'jpn': '日本語',
	'kal': 'kalaallisut',
	'kan': 'ಕನ್ನಡ',
	'kas': 'कश्मीरी',
	'kau': 'Kanuri',
	'kaz': 'қазақ тілі',
	'khm': 'ខ្មែរ',
	'kik': 'Gĩkũyũ',
	'kin': 'Ikinyarwanda',
	'kir': 'Кыргызча',
	'kom': 'коми кыв',
	'kon': 'Kikongo',
	'kor': '한국어',
	'kua': 'Kuanyama',
	'kur': 'Kurdî',
	'lao': 'ພາສາລາວ',
	'lat': 'latine',
	'lav': 'latviešu valoda',
	'lim': 'Limburs',
	'lin': 'Lingála',
	'lit': 'lietuvių kalba',
	'ltz': 'Lëtzebuergesch',
	'lub': 'Tshiluba',
	'lug': 'Luganda',
	'mac': 'македонски јазик', #ISO 639-2T: 'mkd'
	'mah': 'Kajin M̧ajeļ',
	'mal': 'മലയാളം',
	'mao': 'te reo Māori', #ISO 639-2T: 'mri'
	'mar': 'मराठी',
	'may': 'bahasa Melayu', #ISO 639-2T: 'msa'
	'mlg': 'fiteny malagasy',
	'mlt': 'Malti',
	'mon': 'Монгол хэл',
	'nau': 'Dorerin Naoero',
	'nav': 'Diné bizaad',
	'nbl': 'isiNdebele',
	'nde': 'isiNdebele',
	'ndo': 'Owambo',
	'nep': 'नेपाली',
	'nno': 'Norsk nynorsk',
	'nob': 'Norsk bokmål',
	'nor': 'Norsk',
	'nya': 'chiCheŵa',
	'oci': 'occitan',
	'oji': 'ᐊᓂᔑᓈᐯᒧᐎᓐ',
	'ori': 'ଓଡ଼ିଆ',
	'orm': 'Afaan Oromoo',
	'oss': 'ирон æвзаг',
	'pan': 'ਪੰਜਾਬੀ',
	#'per': '????', #ISO 639-2T: 'fas'
	'pli': 'पाऴि',
	'pol': 'język polski',
	'por': 'português',
	'pus': 'پښتو',
	'que': 'Runa Simi',
	'rcf': 'Kréol Rénioné',
	'roh': 'rumantsch grischun',
	'rum': 'limba română', #ISO 639-2T: 'ron'
	'run': 'Ikirundi',
	'rus': 'Русский',
	'sag': 'yângâ tî sängö',
	'san': 'संस्कृतम्',
	'sin': 'සිංහල',
	'slo': 'slovenčina', #ISO 639-2T: 'slk'
	'slv': 'slovenski jezik',
	'sme': 'Davvisámegiella',
	#'smo': 'gagana fa'a Samoa'
	'sna': 'chiShona',
	'snd': 'सिन्धी',
	'som': 'Soomaaliga',
	'sot': 'Sesotho',
	'spa': 'español',
	'srd': 'sardu',
	'srp': 'српски језик',
	'ssw': 'SiSwati',
	'sun': 'Basa Sunda',
	'swa': 'Kiswahili',
	'swe': 'svenska',
	'tah': 'Reo Tahiti',
	'tam': 'தமிழ்',
	'tat': 'татар теле',
	'tel': 'తెలుగు',
	'tgk': 'тоҷикӣ',
	'tgl': 'Wikang Tagalog',
	'tha': 'ไทย',
	'tib': 'བོད་ཡིག', #ISO 639-2T: 'tib'
	'tir': 'ትግርኛ',
	'ton': 'faka Tonga',
	'tsn': 'Setswana',
	'tso': 'Xitsonga',
	'tuk': 'Türkmen',
	'tur': 'Türkçe',
	'twi': 'Twi',
	'uig': 'ئۇيغۇرچە‎',
	'ukr': 'Українська',
	'urd': 'اردو',
	'uzb': 'Oʻzbek',
	'ven': 'Tshivenḓa',
	'vie': 'Tiếng Việt',
	'vol': 'Volapük',
	'wel': 'Cymraeg', #ISO 639-2T: 'wel'
	'wln': 'walon',
	'wol': 'Wollof',
	'xho': 'isiXhosa',
	'yid': 'ייִדיש',
	'yor': 'Yorùbá',
	'zha': 'Saɯ cueŋƅ',
	'zul': 'isiZulu',
}
