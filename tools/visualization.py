import os
import os.path as osp
import cv2 as cv
import numpy as np
from glob import glob
import json


def read_json(path):
    with open(path, "r", encoding="utf8") as fp:
        json_data = json.load(fp)

    return json_data


def vis_label(image_dir, json_dir):
    json_list = sorted(glob(f"{json_dir}/*.json"))
    for json_path in json_list:
        json_data = read_json(json_path)
        image_path = osp.join(image_dir, osp.basename(json_path).replace(".json", ".jpg"))
        try:
            images = cv.imread(image_path)
        except:
            continue
        if not "keypoints" in json_data:
            continue
        keypoints = json_data["keypoints"]
        for cats, keypoint in keypoints.items():
            for cat, keys in keypoint.items():
                cv.circle(images, (int(keys[0]), int(keys[1])), 2, (255, 255, 0), -1)
        cv.imshow("image", images)
        if cv.waitKey(0) == "27":
            cv.destroyAllWindows()
            break
        if cv.waitKey(0) == ord("d"):
            cv.destroyAllWindows()
            continue


if __name__ == "__main__":
    image_dir = "data/test_images"
    json_dir = "data/test_labels"
    vis_label(image_dir, json_dir)
