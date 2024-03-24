import sys
import base64
import os
import uuid
import random
import cv2
import shutil
from queue import Queue
import threading
import time
import datetime
from PIL import Image, ImageDraw, ImageFont
import aiofiles


RGB_COLORS = {"red": (255, 0, 0),
              "white": (255, 255, 255),
              "black": (0, 0, 0),
              "green": (0, 255, 0),
              "blue": (0, 0, 255)
              }


def get_binary_data(file_path):
    with open(file_path, "rb") as f:
        base64_str = base64.b64encode(f.read())
        return base64_str


def image_base64(image_path):
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


async def aio_image_base64(image_path):
    try:
        async with aiofiles.open(image_path, 'rb') as f:
            ib = await f.read()
            return base64.b64encode(ib).decode('utf-8')
    except Exception as e:
        print(e)
        ib = "None"
        return ib


def get_shape_size(image_path):
    """
    读取图片尺寸, 宽、高
    :param image_path: 图片路径
    :return: img_width, img_height
    """
    if not os.path.exists(image_path):
        return None, None

    image = cv2.imread(image_path)
    img_width = image.shape[1]
    img_height = image.shape[0]

    return img_width, img_height

def get_image_size(image_path):
    """
    读取图片尺寸, 宽、高,该方法性能更好
    :param image_path: 图片路径
    :return: img_width, img_height
    :param image_path:
    :return:
    """
    im = Image.open(image_path)  # 返回一个Image对象
    return im.size[0], im.size[1]

def process_path(image_path, image_size=None):
    """
        过滤出图片
    :param image_path: 路径
    :param image_size: 过滤出多少图片
    :return:
    """
    image = []
    for p, d, f in os.walk(image_path):
        for elem in f:
            if (str(elem.split('.')[-1])).lower() in ('jpg', 'png', 'jpeg', 'bmp'):
                image.append(os.path.join(p, elem))
                if image_size is not None and len(image) == image_size:
                    return image
    return image


def random_select_image(path):
    """从目录中随机选择一张图片的绝对地址返回

    :param path:
    :return:
    """
    temp = []
    for root, dirs, files in os.walk(path):
        for f in files:
            temp.append(os.path.join(root, f))
    return random.choice(temp)


def get_image_list(file_path):
    image_list = []
    for p, d, f in os.walk(file_path):
        for elem in f:
            if str.lower(str(elem.split('.')[-1])) in ('jpg', 'png', 'jpeg', 'bmp'):
                # print os.path.join(p, elem)
                image_list.append(os.path.join(p, elem))
    return image_list


def cut_save_image(src_image_file_path, dst_image_file_path, rectangle_vertices):
    """
     在原图中根据矩形框坐标截取小图后保存
    :param src_image_file_path: 原图绝对路径
    :param dst_image_file_path: 截取后保存图路径
    :param rectangle_vertices: [{"x": 0, "y":0},{"x": 0, "y":0}] 左上、右下坐标点
    :return:
    """
    if not os.path.exists(src_image_file_path):
        raise FileNotFoundError(f" {src_image_file_path} not exsit!")

    image = cv2.imread(src_image_file_path)
    # 同步提取到的目标坐标位置x,y轴,在抠图时位置要相反取值设置
    small_image_left_x = rectangle_vertices[0]["x"]
    small_image_left_y = rectangle_vertices[0]["y"]

    small_image_right_x = rectangle_vertices[1]["x"]
    small_image_right_y = rectangle_vertices[1]["y"]

    crop_image = image[small_image_left_y:small_image_right_y, small_image_left_x:small_image_right_x]
    cv2.imwrite(dst_image_file_path, crop_image)


# 画出文字
def draw_text(draw, center, str_):
    ttfront = ImageFont.truetype("simhei.ttf", 16)  # 字体大小
    draw.text(center, str_, fill=(255, 0, 0), font=ttfront)  # 文字位置，内容，字体


# 画矩形框
def draw_rectangle(out_path, out_file_name, coordinate, color=(255, 0, 0)):
    abs_out_file = os.path.join(out_path, out_file_name)
    im = Image.open(abs_out_file)
    draw = ImageDraw.Draw(im)
    draw.rectangle(coordinate, outline=color)
    im.save(abs_out_file)


def draw_polylines(image_path, pts, color=(255, 0, 0)):
    """
     在图片上绘制多边形区域框
    :param image_path:  图片绝对路径
    :param pts: 表示待绘制多边形的折线数组--多边形的顶点像素坐标点(按顺序)
                eg. [[150,50],[140,140],[200,170],[250,250]]
    :param color: 必选参数。用于设置多边形的颜色
    :return:
    """
    if not os.path.exists(image_path):
        raise Exception(f"{image_path}不存在！")
    import numpy as np
    image = cv2.imread(image_path)
    points = np.array([pts])
    image = cv2.polylines(image, points, True, color, thickness=2)
    try:
        cv2.imwrite(image_path, image)
    except Exception as ex:
        print(f"异步存图({image_path})异常 {ex}")


def draw_ponit(image_path, point, color=(255, 0, 0)):
    """
     在图片上绘制点
    :param image_path:  图片绝对路径
    :param point: (60, 60)
    :param color: 必选参数。用于设置多边形的颜色
    :return:
    """
    if not os.path.exists(image_path):
        raise Exception(f"{image_path}不存在！")
    image = cv2.imread(image_path)
    image = cv2.circle(image, point, 10, color, -1)
    cv2.imwrite(image_path, image)


# 画矩形框和文字
def draw_rectangle_attribute(out_path, out_file_name, coordinate, attribute_list, color=(255, 0, 0)):
    abs_out_file = os.path.join(out_path, out_file_name)
    im = Image.open(abs_out_file)
    draw = ImageDraw.Draw(im)
    draw.rectangle(coordinate, outline=color)
    draw_text(draw, (coordinate[0], coordinate[1]), attribute_list)
    im.save(abs_out_file)


def add_watermark(source_image, watermark, target_path):
    image = Image.open(source_image)

    draw = ImageDraw.Draw(image)
    draw.text((16, 16), watermark, (255, 0, 0), font=ImageFont.truetype("simhei.ttf", 32))
    ImageDraw.Draw(image)

    image.save(os.path.join(target_path, os.path.basename(source_image)))


def draw_rectangle_any_vertices(src_pic_path, out_put_dir, vertices, add_txt_list=None):
    """
     同时在指定图片上绘制多个矩形框
    :param src_pic_path: 源图文件绝对路径,不可包含中文
    :param out_put_dir:  输出路径， 必须已经存在
    :param vertices: 多个矩形框  [[{'x': 963, 'y': 197}, {'x': 1035, 'y': 271}],...]
    :return:
    """
    print(f"开始在大图上绘制目标框")
    if not os.path.exists(src_pic_path):
        raise FileNotFoundError(f" src_pic_path not exsit! ")

    new_image = os.path.join(out_put_dir, os.path.basename(src_pic_path))
    img = cv2.imread(src_pic_path)
    text_loc_index = 0
    text_step_index = 0
    for i, vertice in enumerate(vertices):
        text_step_index += 1
        cv2.rectangle(img, (vertice[0]['x'], vertice[0]['y']), (vertice[1]['x'], vertice[1]['y']),
                      (0, 255, 0), 1)
        if text_step_index >= 5:
            text_step_index = 0
        if add_txt_list:
            cv2.putText(img, add_txt_list[i], (vertice[text_loc_index]['x']+2*text_step_index, vertice[text_loc_index]['y']+40*text_step_index), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)
    cv2.imwrite(new_image, img)
    print(f"大图上绘制目标框结束")


def image_queue(image_path:str, q:object, image_num:int=None, flag:int=0):
  """将image_path目录及子目录下的所有图片或指定数量的图片路径推送到q队列

  Args:
      image_path (string): 图片所在目录路径
      q (queue): 队列对象
      image_num (int): 指定的图片数量. Defaults to None.
  """
  for p, d, f in os.walk(image_path):
    if f:
      for elem in f:
        if (str(elem.split('.')[-1])).lower() in ('jpg', 'png', 'jpeg', 'bmp'):
          q.put(os.path.join(p, elem))
          flag +=1
          if image_num is not None and flag == image_num:
            break
    if d:
      for el in d:
        image_queue(el, q, image_num, flag)


# 视频时长读取
def get_video_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        rate = cap.get(5)
        FrameNumber = cap.get(7)
        duration = FrameNumber/rate
        return duration

# 视频抽帧
def video_images(Video_Dir, interval, out_path):
    """
    :param Video_Dir:视频素材所在路径
    :param interval:抽帧间隔，例如10，就是每隔10帧抽一帧
    :param out_path:图片输出位置
    :return:
    """
    cap = cv2.VideoCapture(Video_Dir)
    c = 1  # 帧数起点
    index = 1  # 图片命名起点，如1.jpg

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # 逐帧捕获
        ret, frame = cap.read()
        # 如果正确读取帧，ret为True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        if c % interval == 0:
            cv2.imwrite( os.path.join(out_path, str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S_"))+str(index)+'.jpg'), frame)
            index += 1
        c += 1
        cv2.waitKey(1)
        # 按键停止
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()

# 批量视频抽帧，线性处理
def dir_video_images(dir_path,interval,out_path):
    """
    :param dir_path:
    :param out_path:
    :return:
    """
    for path in os.listdir(dir_path):
        path_ = os.path.join(dir_path, path)
        _path = os.path.join(out_path, path.split(".")[0])
        if not os.path.exists(_path):
            os.makedirs(_path)
        video_images(path_, interval, _path)