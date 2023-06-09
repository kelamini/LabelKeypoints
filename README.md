# 人体关键点标注工具

## 版本差异记录

- v0.3.0
    - 在标注时添加了 水平/垂直 辅助线
    - 通过单击选中 `Label List` 某一类标签，再按下 `Ctrl+a` 可删除该类别的所有已标注关键点
    - 增加了针对某一目标物体必须标注完全才能切换到下一张或关闭程序的弹窗提示
    - 增加了矩形框标注的顺序（先左上角后右下角）检查弹窗提示
- v0.2.0
    - 去掉了弹窗标注的方式，并通过配置 `config.yaml` 文件自定义标注关键点及可视化时的 `RGB` 颜色值 
- v0.1.0
    - 点击鼠标标注关键点将会弹窗，通过编辑输入当前目标标签和点击候选关键点实现标注


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

# --config 用于配置关键点与标注颜色的对应表
labelkeys --config /path/to/config.yaml
# 若没有该参数则保持默认配置
labelkeys
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

默认配置文件 `default_config.yaml` 内容：

```yaml
colormap:
  rectangle: [0, 255, 0]
  nose: [3, 168, 158]
  lefteye: [3, 168, 158]
  righteye: [3, 168, 158]
  leftear: [3, 168, 158]
  rightear: [3, 168, 158]
  leftshoulder: [0, 255, 127]
  rightshoulder: [0, 255, 127]
  leftelbow: [0, 255, 127]
  rightelbow: [0, 255, 127]
  leftwrist: [0, 255, 127]
  rightwrist: [0, 255, 127]
  lefthip: [138, 43, 255]
  righthip: [138, 43, 255]
  leftknee: [138, 43, 255]
  rightknee: [138, 43, 255]
  leftankle: [138, 43, 255]
  rightankle: [138, 43, 255]
```

说明：
- 自定义标注点，只需要在 `colormap` 下添加相应的关键点名称与标注颜色值
- 若 `colormap` 下包含 `rectangle` 键，则可以标注矩形框


## 快捷键

- 打开图像文件夹 -> i
- 打开 json 文件夹 -> j
- 保存 json 结果 -> Ctrl+s
- 切换到上一张 -> a
- 切换到下一张 -> d
- 撤销当前一个标注关键点 -> Ctrl+z
- 删除选中的某一类已标注的关键点 -> Ctrl+a
