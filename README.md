# COCO 人体关键点标注工具

## 人体关键点

Nose
Left Eye
Right Eye
Left Ear
Right Ear
Left Shoulder
Right Shoulder
Left Elbow
Right Elbow
Left Wrist
Right Wrist
Left Hip
Right Hip
Left Knee
Right Knee
Left Ankle
Right Ankle

说明：
包括但不限于以上 17 点，由于保存的 json 结果都是以字典键值对存储的，可随意更改。


## 数据结构

```json
{
    "imagePath": str,
    "imageWidth": int,
    "imageHeight": int,
    "keypoints": {},
}

"keypoints": {
    "category_1": {
        "nose": [int, int, 0 or 1],
        ...
    },
    "category_2": {
        "nose": [int, int, 0 or 1],
        ...
    },
    ...
}
```

说明：
- "imagePath": 图像路径
- "imageWidth": 图像的宽
- "imageHeight": 图像的高
- "keypoints": 标注的关键点


## 安装 && 使用

```bash
conda create -n labelcoco python=3.7
conda activate labelcoco
pip install -r requirements.txt

python main.py
```


## 使用步骤

1. 打开 image 文件夹
2. 打开 json 文件夹
3. 开始标注
    - 左键表示可见，标注点颜色为红色
    - 右键表示不可见，标注点颜色为绿色
4. 双击右栏标注点标签可直接删除该点

说明：
image 和 json 分别设置打开路径，方便管理。
该工具加载两个文件夹时会检查 image 和 json 的对应关系，若 image 存在 json 不存在，
只会在加载到该 image 时才生成 json 文件。


## 快捷键

打开图像文件夹 -> i
打开 json 文件夹 -> j
保存 json 结果 -> Ctrl+s
切换到上一张 -> a
切换到下一张 -> d
