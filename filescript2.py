import csv
import shutil
from pathlib import Path

	
import tensorflow as tf
import sys

with open('test_data.csv', newline='') as csvfile:
	count=0;
	paths=[];
	csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in csvreader:
		csvstrings=(row[0].split(","));
		my_file = Path("images/"+csvstrings[0]+".jpg");
		if my_file.is_file():
			count+=1;
			paths.append("images/"+csvstrings[0]+".jpg");

	print(count);

	# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
       		in tf.gfile.GFile("training/retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("training/retrained_graph.pb", 'rb') as f:
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())
	_ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
	# Feed the image_data as input to the graph and get first prediction
	softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')


	with open('results.csv', 'a', newline='') as csvfile:
		csvwriter = csv.DictWriter(csvfile, fieldnames=["EXT_ID", "WalmartReceipt", "PredictionScore"])
		csvwriter.writeheader();
	for image_path in paths :

		# Read in the image_data
		image_data = tf.gfile.FastGFile(image_path, 'rb').read()
		predictions = sess.run(softmax_tensor, \
			{'DecodeJpeg/contents:0': image_data})

		# Sort to show labels of first prediction in order of confidence
		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
		print (top_k);

		with open('results.csv', 'a', newline='') as csvfile:
			csvwriter = csv.DictWriter(csvfile, fieldnames=["EXT_ID", "WalmartReceipt", "PredictionScore"])
			
			if(top_k[0]==1):
				csvwriter.writerow({"EXT_ID":image_path[7:-4],"WalmartReceipt":'TRUE', "PredictionScore":str(predictions[0][top_k[0]])})
			else:
				csvwriter.writerow({"EXT_ID":image_path[7:-4],"WalmartReceipt":'FALSE', "PredictionScore":str(predictions[0][top_k[1]])})
			