import fasttext
import os
import time

if __name__ == "__main__":
	test_path = "../data/fasttext/small_dataset.txt"
	clf = fasttext.load_model("../models/one_more_class.bin")

	lines = open(test_path, 'r', encoding='UTF-8').read().strip().split('\n')
	lines = list(map(lambda line: line[11:], lines))

	# Should give us label 8
	start_time = time.time()
	predicted_labels = clf.predict(lines)
	print("Predicted in {} seconds. ".format(time.time() - start_time))

	predicted_labels = [x[0] for x in predicted_labels]
	#print([l for l in predicted_labels if l != "__label__11"])
	print([lines[i] for i in range(len(predicted_labels)) if predicted_labels[i] == "__label__1"])
	#print(predicted_labels)