import os

data_path = "./data/body"
name_to_label = {
	"Abbreviations": 1,
	"Authors Contributions": 2,
	"Case": 3,
	"Competing interests": 4,
	"Conclusion": 5,
	"Discussion": 6,
	"Introduction": 7,
	"Methods": 8,
	"Publication History": 9,
	"Supporting Information": 10
}

def get_section_names():
	return name_to_label.keys()


def read_data(section, max_samples=-1):
	print("Loading: ", section)
	section_data = []
	with open(os.path.join(data_path, section), encoding='UTF-8') as f: 
		for index, line in enumerate(f):
			if line == '\n':
				continue
			if max_samples > -1 and (max_samples-1)*2 < index:
				break

			section_data.append(line)
			#print("New section data", len(section_data))

	return section_data


def load_dataset(section_names, max_samples=-1):
	data = []
	labels = []
	for section in section_names:
		section_data = read_data(section, max_samples=max_samples)
		data.extend(section_data)
		labels.extend([name_to_label[section] for x in range(len(section_data))])

	print(len(data), len(labels))
	assert len(data) == len(labels)
	return data, labels
