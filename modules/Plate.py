import cv2;
import numpy as np;
import logging;
from TrainingCharacters import *;
from matplotlib import pyplot as plt;
from copy import deepcopy, copy;
from logging.config import fileConfig;

# logger setup
fileConfig("logging_config.ini");
logger = logging.getLogger();

class Plate:
	""" Class for the license plates """
	def __init__(self, image):				### Plate Class Vars ###
		self.original_image = image;			# original image of analysis
		self.plate_located_image = deepcopy(image);	# original image with plate hilighted
		self.plate_image = None;			# license plate cropped
		self.plate_image_char = None;			# license plate cropped, chars outlined
		self.gray_image = None;				# original image - grayscale for analysis
		self.plate_number = "None found.";		# plate number
		self.roi = [];					# regions of interest for plates
		logger.info("New plate created.");

	""" Converts original image to grayscale for analysis """
	def grayImage(self, image):
		logger.info("Image converted to grayscale");
		return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY);

	""" Algorithm to find plate and read characters """
	def plateSearch(self):
		self.findContour();
		self.cropPlate();
		if self.plate_image is not None:
			self.readPlateNumber();
		self.showResults();
		return True;

	""" Searches for a contour that looks like a license plate
	in the image of a car """
	def findContour(self):
		self.gray_image = self.grayImage(deepcopy(self.original_image));
		self.gray_image = cv2.GaussianBlur(self.gray_image, (29,29), 0);

		ret, threshold = cv2.threshold(self.gray_image, 127, 255, 0);
		_,contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

		w,h,x,y = 0,0,0,0;

		for contour in contours:
			area = cv2.contourArea(contour);

			# rough range of areas of a license plate
			if area > 6000 and area < 40000:
				[x,y,w,h] = cv2.boundingRect(contour);

			# rough dimensions of a license plate
			if w > 100 and w < 200 and h > 60 and h < 100:
				self.roi.append([x,y,w,h]);
				cv2.rectangle(self.plate_located_image, (x,y), (x+w, y+h), (0,255,0), 10);

		logger.info("%s potential plates found.", str(len(self.roi)));
		return True;

	""" If a license plate contour has been found, crop
	out the contour and create a new image """
	def cropPlate(self):
		if len(self.roi) > 1:
			[x,y,w,h] = self.roi[0];
			self.plate_image = self.original_image[y:y+h,x:x+w];
			self.plate_image_char = deepcopy(self.plate_image);
		return True;

	""" Subalgorithm to read the license plate number using the
	cropped image of a license plate """
	def readPlateNumber(self):
		self.plate_number = "License plate #: None found";
		self.findCharacterContour();
		return True;

	""" Finds contours in the cropped image of a license plate
	that fit the dimension range of a letter or number """
	def findCharacterContour(self):
		gray_plate = self.grayImage(deepcopy(self.plate_image));
		gray_plate = cv2.GaussianBlur(gray_plate, (5,5), 0);

		_,threshold = cv2.threshold(gray_plate, 127, 255, 0);
		_,contours,_ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

		w,h,x,y = 0,0,0,0;

		logger.info("%s contours found.", str(len(contours)));
		for contour in contours:
			area = cv2.contourArea(contour);

			# rough range of areas of a plate number
			if area > 120 and area < 2000:
				[x,y,w,h] = cv2.boundingRect(contour);

			# rough dimensions of a character
			if h > 20 and h < 90 and w > 10 and w < 50:
				self.plate_characters.append([x,y,w,h]);
				cv2.rectangle(self.plate_image_char, (x,y), (x+w, y+h), (0,0,255), 1);

		logger.info("%s plate characters found", str(len(self.plate_characters)));
		return True;

	""" To read the characters in the plate, does a histogram
	comparison against the 35 characters in our `characters` folder
	to find a best match for the character """
	def histogramComparison(self):
		logger.info("Attempting to read %s characters.", str(len(self.plate_characters)));
		for character in self.plate_characters:

		return True;

	""" Subplot generator for images """
	def plot(self, figure, subplot, image, title):
		figure.subplot(subplot);
		figure.imshow(image);
		figure.xlabel(title);
		figure.xticks([]);
		figure.yticks([]);
		return True;

	""" Show our results """
	def showResults(self):
		plt.figure(self.plate_number);

		self.plot(plt, 321, self.original_image, "Original image");
		self.plot(plt, 322, self.gray_image, "Threshold image");
		self.plot(plt, 323, self.plate_located_image, "Plate located");

		if self.plate_image is not None:
			self.plot(plt, 324, self.plate_image, "License plate");
			self.plot(plt, 325, self.plate_image_char, "Characters outlined");

		plt.tight_layout();
		plt.show();
		return True;
