# imports
import datetime as dt
import curriculum_getter as getter

# open the base.html and extract its content
file = open('base.html')
base_html = file.readlines()
file.close()

# get curriculum data
cv = {
	'personal_info': getter.personal_info,
	'lang': getter.lang,
	'academic': getter.academic,
	'certs': getter.certs,
	'xp': getter.xp,
	'hobby': getter.hobby
}
cv_sorting = getter.cv_sort_index

# get icons
file = open('cv_icons.txt')
icons = file.readlines()
file.close()

for x in range(0, len(icons)):
	icons[x] = icons[x].split(' = ')
	icons[x] = icons[x][1]

# create personal info section
# head
head = [
	'\t<div class="head">\n',
	'\t\t<img src="{}">\n'.format(cv['personal_info']['profile_pic']),
	'\t\t<h1>{}</h1>\n'.format(cv['personal_info']['name']),
	'\t</div>\n'
]
# info
birth = cv['personal_info']['dob'].split('/')
birth = dt.date(int(birth[2]), int(birth[1]), int(birth[0]))
today = dt.date.today()
age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

link_button = '<button class="link-button" onclick="window.open(\'{}\')">{}</button>'
linkedin_link = link_button.format(
	cv['personal_info']['linkedin'],
	icons[0].replace('\n', '') + ' LinkedIn'
)
github_link = link_button.format(
	cv['personal_info']['github'],
	icons[1].replace('\n', '') + ' GitHub'
)

info = [
	'\t<div class="info">\n',
	'\t\t<p>{} years old</p>\n'.format(str(age)),
	'\t\t<p>Natural from {}, {}</p>\n'.format(cv['personal_info']['birthplace'], cv['personal_info']['nationality']),
	'\t\t<p>Lives in {}</p>\n'.format(cv['personal_info']['lives']),
	'\t\t<p>E-mail: {}</p>\n'.format(cv['personal_info']['email']),
	'\t\t<p>Mobile phone: {}</p>\n'.format(cv['personal_info']['mobile']),
	'\t\t<div class="print-link">\n',
	'\t\t\t<p>LinkedIn: {}</p>\n'.format(cv['personal_info']['linkedin']),
	'\t\t\t<p>GitHub: {}</p>\n'.format(cv['personal_info']['github']),
	'\t\t</div>\n',
	'\t\t{}\n\t\t{}\n'.format(linkedin_link, github_link),
	'\t</div>\n'
]

# create academic section
academic = ['\t<h2 id="academic-title">EDUCATION</h2>\n']
for x in range(0, len(cv_sorting['academic_order'])):
	index = cv_sorting['academic_order'][x]
	which = cv['academic']['academic_{}'.format(index)]
	content = '\t<div class="academic">\n'
	content += '\t\t<p>Degree: {}</p>\n'.format(which['what'])
	content += '\t\t<p>University: {}</p>\n'.format(which['institution'])
	content += '\t\t<p>From {} to {}</p>\n'.format(which['init'], which['end'])
	content += '\t</div>\n'
	academic.append(content)

# create certs section
certs = ['\t<h2 id="cert-title">CERTIFICATES</h2>\n']
for x in range(0, len(cv_sorting['certificate_order'])):
	index = cv_sorting['certificate_order'][x]
	which = cv['certs']['cert_{}'.format(index)]
	content = '\t<div class="cert">\n'
	content += '\t\t<p>Certificate: {}</p>\n'.format(which['title'])
	content += '\t\t<p>Institution: {}</p>\n'.format(which['org'])
	content += '\t\t<p>Emission: {}</p>\n'.format(which['date'])
	if bool(which['link']):
		link = 'window.open(\'' + which['link'] + '\')'
		content += '\t\t<button class="check-cert" onclick="{}">Check certificate</button>\n'.format(link)
	content += '\t</div>\n'
	certs.append(content)

# create xp section
xp = ['\t<h2 id="xp-title">EXPERIENCE</h2>\n']
for x in range(0, len(cv_sorting['xp_order'])):
	index = cv_sorting['xp_order'][x]
	which = cv['xp']['xp_{}'.format(index)]
	content = '\t<div class="xp">\n'
	content += '\t\t<p>Position: {}</p>\n'.format(which['what'])
	content += '\t\t<p>Company/Institution: {}</p>\n'.format(which['where'])
	if which['end'] is True:
		content += '\t\t<p>Currently working on (since {})</p>\n'.format(which['init'])
	else:
		content += '\t\t<p>From {} to {}</p>\n'.format(which['init'], which['end'])
	content += '\t\t<p>Description: {}</p>\n'.format(which['desc'])
	content += '\t</div>\n'
	xp.append(content)

# create lang section
lang = ['\t<h2 id="lang-title">LANGUAGES</h2>\n']
for x in range(0, len(cv_sorting['lang_order'])):
	index = cv_sorting['lang_order'][x]
	which = cv['lang']['lang_{}'.format(index)]
	content = '\t<div class="lang">\n'
	content += '\t\t<p>Language: {}</p>\n'.format(which['language'])
	content += '\t\t<p>Reading: {}</p>\n'.format(which['read'])
	content += '\t\t<p>Writing: {}</p>\n'.format(which['write'])
	content += '\t\t<p>Speaking: {}</p>\n'.format(which['speak'])
	content += '\t</div>\n'
	lang.append(content)

# create hobby section
hobby = ['\t<div class="hobby">\n', '\t\t<h2 id="hobby-title">HOBBIES</h2>\n']
for x in range(0, len(cv['hobby'])):
	hobby.append('\t\t<p>• {}</p>\n'.format(cv['hobby'][x]))
hobby.append('\t</div>\n')

# generate cv html
cv_html = []
for x in range(0, len(base_html)):
	if '$title' in base_html[x]:
		title = 'Curriculum - ' + cv['personal_info']['name']
		base_html[x] = base_html[x].replace('$title', title)
	elif '$body' in base_html[x]:
		cv_html.append('\t<div class="personal-section">\n')
		for y in range(0, len(head)):
			cv_html.append(head[y].replace('\t<', '\t\t<'))
		for y in range(0, len(info)):
			cv_html.append(info[y].replace('\t<', '\t\t<'))
		cv_html.append('\t</div>\n')
		cv_html.append('\t<div class="academic-section">\n')
		for y in range(0, len(academic)):
			cv_html.append(academic[y].replace('\t<', '\t\t<'))
		cv_html.append('\t</div>\n')
		cv_html.append('\t<div class="certs-section">\n')
		for y in range(0, len(certs)):
			cv_html.append(certs[y].replace('\t<', '\t\t<'))
		cv_html.append('\t</div>\n')
		cv_html.append('\t<div class="xp-section">\n')
		for y in range(0, len(xp)):
			cv_html.append(xp[y].replace('\t<', '\t\t<'))
		cv_html.append('\t</div>\n')
		cv_html.append('\t<div class="lang-section">\n')
		for y in range(0, len(lang)):
			cv_html.append(lang[y].replace('\t<', '\t\t<'))
		cv_html.append('\t</div>\n')
		cv_html.append('\t<div class="hobby-section">\n')
		for y in range(0, len(hobby)):
			cv_html.append(hobby[y].replace('\t<', '\t\t<'))
		cv_html.append('\t</div>\n')
	else:
		cv_html.append(base_html[x])

# create cv file
file_name = cv['personal_info']['name'].split(' ')
file_name = file_name[0].lower() + '_' + file_name[len(file_name) - 1].lower()
file = open('cv_{}.html'.format(file_name), 'w', encoding='utf-8')
file.writelines(cv_html)
file.close()
