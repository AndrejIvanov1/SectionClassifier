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

def load_dataset(section_names):
	data = []
	labels = []
	for section in section_names:
		section_data = open(os.path.join(data_path, section), encoding='UTF-8').read().split('\n\n')[:-1]
		print(section, len(section_data))
		print(section_data[0], section_data[-1])
		data.extend(section_data)
		labels.extend([name_to_label[section] for x in range(len(section_data))])

	assert len(data) == len(labels)
	return data, labels
