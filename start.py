import torch
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2  # 需要添加此导入

checkpoint = "./checkpoints/sam2.1_hiera_large.pt"
model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
predictor = SAM2ImagePredictor(build_sam2(model_cfg, checkpoint, device="cpu"))

# 使用PIL加载图片并转换为numpy数组
# image = Image.open("/Users/xmly/Desktop/pic3.png")
# image = np.array(image)
image = Image.open("/Users/xmly/Documents/shadow/sam2/notebooks/images/truck.jpg")
image = np.array(image.convert("RGB"))


def show_mask(mask, ax, random_color=False, borders=True):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask = mask.astype(np.uint8)
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    if borders:
        import cv2

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # Try to smooth contours
        contours = [
            cv2.approxPolyDP(contour, epsilon=0.01, closed=True) for contour in contours
        ]
        mask_image = cv2.drawContours(
            mask_image, contours, -1, (1, 1, 1, 0.5), thickness=2
        )
    ax.imshow(mask_image)


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(
        pos_points[:, 0],
        pos_points[:, 1],
        color="green",
        marker="*",
        s=marker_size,
        edgecolor="white",
        linewidth=1.25,
    )
    ax.scatter(
        neg_points[:, 0],
        neg_points[:, 1],
        color="red",
        marker="*",
        s=marker_size,
        edgecolor="white",
        linewidth=1.25,
    )


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(
        plt.Rectangle((x0, y0), w, h, edgecolor="green", facecolor=(0, 0, 0, 0), lw=2)
    )


def show_masks(
    image,
    masks,
    scores,
    point_coords=None,
    box_coords=None,
    input_labels=None,
    borders=True,
):
    for i, (mask, score) in enumerate(zip(masks, scores)):
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        show_mask(mask, plt.gca(), borders=borders)
        if point_coords is not None:
            assert input_labels is not None
            show_points(point_coords, input_labels, plt.gca())
        if box_coords is not None:
            # boxes
            show_box(box_coords, plt.gca())
        if len(scores) > 1:
            plt.title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
        plt.axis("off")
        plt.show()


# 单个输入点
input_point = np.array([[500, 375], [1125, 625]])
input_label = np.array([1, 1])

# plt.figure(figsize=(10, 10))
# plt.imshow(image)
# show_points(input_point, input_label, plt.gca())
# plt.axis("on")
# plt.show()
with torch.inference_mode(), torch.autocast("cpu", dtype=torch.bfloat16):
    predictor.set_image(image)
    masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        multimask_output=False,
    )
    sorted_ind = np.argsort(scores)[::-1]
    masks = masks[sorted_ind]
    scores = scores[sorted_ind]
    logits = logits[sorted_ind]

    # # 增加一个输入点
    # input_point = np.array([[500, 375], [1125, 625]])
    # input_label = np.array([1, 1])

    # mask_input = logits[np.argmax(scores), :, :]  # Choose the model's best mask

    # masks, scores, _ = predictor.predict(
    #     point_coords=input_point,
    #     point_labels=input_label,
    #     mask_input=mask_input[None, :, :],
    #     multimask_output=False,
    # )

    show_masks(
        image,
        masks,
        scores,
        point_coords=input_point,
        input_labels=input_label,
        borders=True,
    )


# with torch.inference_mode(), torch.autocast("cpu", dtype=torch.bfloat16):
#     predictor.set_image(image)
#     masks, scores, _ = predictor.predict(
#         point_coords=None,
#         point_labels=None,
#         multimask_output=True,  # 返回多个mask
#     )

#     # 按照分数排序masks
#     sorted_ind = np.argsort(scores)[::-1]
#     masks = masks[sorted_ind]
#     scores = scores[sorted_ind]

#     # 显示结果
#     show_masks(image, masks, scores)