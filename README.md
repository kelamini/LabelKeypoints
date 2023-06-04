# 人体关键点标注工具

## 人体关键点

- Nose
- Left Eye
- Right Eye
- Left Mouth
- Right Mouth
- Left Ear
- Right Ear
- Left Shoulder
- Right Shoulder
- Left Elbow
- Right Elbow
- Left Wrist
- Right Wrist
- Left Hip
- Right Hip
- Left Knee
- Right Knee
- Left Ankle
- Right Ankle


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
        "nose": [float, float, 0 or 1],
        ...
    },
    "category_2": {
        "nose": [float, float, 0 or 1],
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


## 安装 && 打开

```bash
conda create -n labelkeys python=3.7    # conda 创建环境
conda activate labelkeys    # 激活环境
pip install .   # 安装

labelkeys   # 打开软件
```


## 使用步骤

1. 打开 image 文件夹
2. 打开 json 文件夹
3. 开始标注
    - 左键表示可见
    - 右键表示不可见
4. 单击 "Label List" 栏标注点标签则该点在图像上高亮显示
5. 双击 "Label List" 栏标注点标签可直接删除该点
6. 单击 "Image List" 栏内图像名称可跳转到该图像

说明：
- image 和 json 分别设置打开路径，方便管理。该工具加载两个文件夹时会检查 image 和 json 的对应关系，若 image 存在 json 不存在，只会在加载到该 image 时才生成 json 文件。
- 切换图像时将自动保存标注结果。

## 快捷键

- 打开图像文件夹 -> i
- 打开 json 文件夹 -> j
- 保存 json 结果 -> Ctrl+s
- 切换到上一张 -> a
- 切换到下一张 -> d
