import os
import sys
from iou_helper import get_iou

def get_best_matching_person(truth_person,pred_array):
    best_mapping_person = pred_array[0]
    highest_area = get_iou(truth_person,best_mapping_person)

    for i in range(1,len(pred_array)):
        tmp_area = get_iou(truth_person,pred_array[i])
        if tmp_area is None:
            continue
        if highest_area is None or tmp_area > highest_area:
            highest_area = tmp_area
            best_mapping_person = pred_array[i]

    return highest_area,best_mapping_person

ground_truth_content = open('TownCentre-groundtruth.csv')
pred_content = open("../output/1b.csv")

#Build ground_truth dict
ground_truth_dict = dict()
for index,line in enumerate(ground_truth_content):
    if index != 0:
        line = line.strip()
        personNumber, frameNumber, headValid, bodyValid, headLeft, headTop, headRight, headBottom, bodyLeft, bodyTop, bodyRight, bodyBottom = line.split(",")
        assert(bodyValid == "1")
        assert(headValid == "1")
        frameNumber = str(int(frameNumber) + 1)
        if frameNumber not in ground_truth_dict:
            ground_truth_dict[frameNumber] = [[personNumber,headLeft, headTop, headRight, headBottom, bodyLeft, bodyTop, bodyRight, bodyBottom]]
        else:
            ground_truth_dict[frameNumber].append([personNumber,headLeft, headTop, headRight, headBottom, bodyLeft, bodyTop, bodyRight, bodyBottom])

#Build pred_dict
pred_dict = dict()
factor = 1.5
for line in pred_content:
    line = line.strip()
    personNumber, frameNumber, bodyValid, bodyLeft, bodyTop, bodyRight, bodyBottom = line.split(",")
    bodyLeft, bodyTop, bodyRight, bodyBottom = float(bodyLeft)*factor, float(bodyTop)*factor, float(bodyRight)*factor, float(bodyBottom)*factor
    assert(bodyValid == "1")
    if frameNumber not in pred_dict:
        pred_dict[frameNumber] = [[personNumber, bodyValid, bodyLeft, bodyTop, bodyRight, bodyBottom]]
    else:
        pred_dict[frameNumber].append([personNumber, bodyValid, bodyLeft, bodyTop, bodyRight, bodyBottom])

total_number_of_correct_predict = 0
total_number_of_preict = 0
total_number_of_ground_truth = 0

for frameNumber in pred_dict:
    ground_truths = ground_truth_dict[frameNumber]
    preds = pred_dict[frameNumber]

    total_number_of_preict += len(preds)
    total_number_of_ground_truth += len(ground_truths)

    print(frameNumber)
    for truth in ground_truths:
        highest_area,best_mapping_person = get_best_matching_person(truth,preds)
        if highest_area >= 0.5:
            total_number_of_correct_predict += 1
            print("\t{} is similar to {} with score of {}".format(truth[-4:],best_mapping_person[-4:],highest_area))

print("precision:{}".format(total_number_of_correct_predict/total_number_of_ground_truth))
print("recall:{}".format(total_number_of_correct_predict/total_number_of_preict))
ground_truth_content.close()
pred_content.close()
