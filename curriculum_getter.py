import datetime as dt

# open personal info file and extract its content
file = open('cv_personal.txt', encoding='utf-8')
personal_info = file.readlines()
file.close()

# handling personal info
personal_info_dict = {}
for x in range(0, len(personal_info)):
	personal_info[x] = personal_info[x].replace('\n', '')
	personal_info[x] = personal_info[x].split(' = ')
	if personal_info[x][0] == 'lives' and personal_info[x][1] == '':
		personal_info[x][1] = personal_info[x - 1][1] + ', ' + personal_info[x - 2][1]
	personal_info_dict.update({personal_info[x][0]: personal_info[x][1]})
personal_info = personal_info_dict

# open language file, extract and handle its content
file = open('cv_lang.txt', encoding='utf-8')
lang = file.readlines()
file.close()

lang.append('\n')
lang_dict = {}
temp_dict = {}
l = 1
for x in range(0, len(lang)):
	if lang[x] != '\n':
		lang[x] = lang[x].replace('\n', '').split(' = ')
		if lang[x][0] != 'language':
			lang[x][1] = float(lang[x][1])
			if lang[x][1] <= 0.25:
				lang[x][1] = 'Basic'
			elif 0.25 < lang[x][1] <= 0.5:
				lang[x][1] = 'Intermediate'
			elif 0.5 < lang[x][1] <= 0.75:
				lang[x][1] = 'Advanced'
			else:
				lang[x][1] = 'Fluent'
		temp_dict.update({lang[x][0]: lang[x][1]})
	else:
		lang_dict.update({'lang_{}'.format(l): {}})
		lang_dict['lang_{}'.format(l)].update(temp_dict)
		temp_dict.clear()
		l += 1
lang = lang_dict

# open academic file, extract and handle its content
file = open('cv_academic.txt', encoding='utf-8')
academic = file.readlines()
file.close()

# separate into as many 'academics' as needed and return content
academic.append('\n')
academic_dict = {}
temp_dict.clear()
a = 0  # academic_0 will return the max degree type, if that makes any sense
for x in range(0, len(academic)):
	if academic[x] != '\n':
		academic[x] = academic[x].replace('\n', '').split(' = ')
		temp_dict.update({academic[x][0]: academic[x][1]})
	else:
		academic_dict.update({'academic_{}'.format(a): {}})
		academic_dict['academic_{}'.format(a)].update(temp_dict)
		temp_dict.clear()
		a += 1
academic = academic_dict

# open certificates file, extract and handle its content
file = open('cv_certificates.txt', encoding='utf-8')
certs = file.readlines()
file.close()

certs.append('\n')
certs_dict = {}
temp_dict.clear()
c = 1
for x in range(0, len(certs)):
	if certs[x] != '\n':
		certs[x] = certs[x].replace('\n', '').split(' = ')
		temp_dict.update({certs[x][0]: certs[x][1]})
	else:
		certs_dict.update({'cert_{}'.format(c): {}})
		certs_dict['cert_{}'.format(c)].update(temp_dict)
		temp_dict.clear()
		c +=1
certs = certs_dict

# open experience file, extract and handle its content
file = open('cv_xp.txt', encoding='utf-8')
xp = file.readlines()
file.close()

xp.append('\n')
xp_dict = {}
temp_dict.clear()
exp = 1
for x in range(0, len(xp)):
	if xp[x] != '\n':
		xp[x] = xp[x].replace('\n', '').split(' = ')
		if xp[x][0] == 'end' and xp[x][1] == '':
			xp[x][1] = True
		elif xp[x][0] == 'salary':
			xp[x][1] = float(xp[x][1])
		temp_dict.update({xp[x][0]: xp[x][1]})
	else:
		xp_dict.update({'xp_{}'.format(exp): {}})
		xp_dict['xp_{}'.format(exp)].update(temp_dict)
		temp_dict.clear()
		exp += 1
xp = xp_dict

# open hobbies file, extract and handle its content
file = open('cv_hobby.txt', encoding='utf-8')
hobby = file.readlines()
file.close()
for x in range(0, len(hobby)):
	hobby[x] = hobby[x].replace('\n', '')
hobby.sort()

# sorting cv information
# creates 'cv_sort_index', a dict of lists that keeps the sorting order of indexes
cv_sort_index = {'lang_order': [], 'academic_order': [], 'certificate_order': [], 'xp_order': []}
temp_sort = []
dict_sort = {}

# lang: alphabetical order
for x in range(0, len(lang)):
	dict_sort.update({lang['lang_{}'.format(x + 1)]['language']: x + 1})
	temp_sort.append(lang['lang_{}'.format(x + 1)]['language'])
temp_sort.sort()
for x in range(0, len(temp_sort)):
	cv_sort_index['lang_order'].append(dict_sort[temp_sort[x]])

# academic: graduation date sorting
temp_sort.clear()
dict_sort.clear()
for x in range(0, len(academic) - 1):
	dict_sort.update({academic['academic_{}'.format(x + 1)]['end']: x + 1})
	temp_date = academic['academic_{}'.format(x + 1)]['end'].split('/')
	temp_sort.append(dt.date(int(temp_date[1]), int(temp_date[0]), 1))
temp_sort.sort(reverse=True)
for x in range(0, len(temp_sort)):
	temp_sort[x] = temp_sort[x].strftime('%m/%Y')
	cv_sort_index['academic_order'].append(dict_sort[temp_sort[x]])

# certificate: date sorting
temp_sort.clear()
dict_sort.clear()
for x in range(0, len(certs)):
	dict_sort.update({certs['cert_{}'.format(x + 1)]['date']: x + 1})
	temp_date = certs['cert_{}'.format(x + 1)]['date'].split('/')
	temp_sort.append(dt.date(int(temp_date[2]), int(temp_date[1]), int(temp_date[0])))
temp_sort.sort(reverse=True)
for x in range(0, len(temp_sort)):
	temp_sort[x] = temp_sort[x].strftime('%d/%m/%Y')
	cv_sort_index['certificate_order'].append(dict_sort[temp_sort[x]])

# xp: end date sorting
temp_sort.clear()
dict_sort.clear()
xp_current = 0
for x in range(0, len(xp)):
	if xp['xp_{}'.format(x + 1)]['end'] is True: xp_current = x + 1
	else:
		dict_sort.update({xp['xp_{}'.format(x + 1)]['end']: x + 1})
		temp_date = xp['xp_{}'.format(x + 1)]['end'].split('/')
		temp_sort.append(dt.date(int(temp_date[1]), int(temp_date[0]), 1))
if xp_current > 0: cv_sort_index['xp_order'].append(xp_current)
temp_sort.sort(reverse=True)
for x in range(0, len(temp_sort)):
	temp_sort[x] = temp_sort[x].strftime('%m/%Y')
	cv_sort_index['xp_order'].append(dict_sort[temp_sort[x]])
