import os

if __name__ == "__main__":
	dataset_path = "../data/fasttext/train.txt"

	lines = open(dataset_path, 'r', encoding='UTF-8').readlines()
	for line in lines:
		# if it is a methods section
		if "__label__8" in line and "click here for file" in line.lower():
			line = line.replace('__label__8', '__label_11')

	open(dataset_path, 'w', encoding='UTF-8').writelines(lines)