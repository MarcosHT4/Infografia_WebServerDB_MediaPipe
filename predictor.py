import cv2
import mediapipe as mp
import numpy as np
from PIL import Image


class SelfiePredictor:
    def __init__(self, bg_color=(192, 192, 192)):
        self.bg_color = bg_color
        self.mp_draw = mp.solutions.drawing_utils
        self.selfie_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0)
        self.holistic = mp.solutions.holistic.Holistic(
            static_image_mode=True,
            model_complexity=2,
            min_detection_confidence=0.4
        )


    def predict_file(self, file):
        img = np.array(Image.open(file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.selfie_segmentation.process(img)
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(img.shape, dtype=np.uint8)
        bg_image[:] = self.bg_color
        output_image = np.where(condition, img, bg_image)
        return output_image

    def extract_pose_landmarks(self, landmarks):
        pose = [
            landmarks.landmark[11],
            landmarks.landmark[12],
            landmarks.landmark[13],
            landmarks.landmark[14],
            landmarks.landmark[15],
            landmarks.landmark[16], 
            landmarks.landmark[17], 
            landmarks.landmark[18],
            landmarks.landmark[19], 
            landmarks.landmark[20],
            landmarks.landmark[21],
            landmarks.landmark[22],
            landmarks.landmark[23],
            landmarks.landmark[24],
            landmarks.landmark[25],
            landmarks.landmark[26],
            landmarks.landmark[27],
            landmarks.landmark[28],
            landmarks.landmark[29],
            landmarks.landmark[30],
            landmarks.landmark[31],
            landmarks.landmark[32],
            
            
        ]

        pose_dict = {}
        for i, landmark in enumerate(pose):
            pose_dict[i+11] = [{"x":landmark.x}, {"y":landmark.y}]
            

        return pose_dict  

    def predict_skeleton(self, file):
        img = np.array(Image.open(file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(img)
        new_img = np.zeros(img.shape)
        p_points = self.extract_pose_landmarks(results.pose_landmarks)
        mp.solutions.drawing_utils.draw_landmarks(
            new_img,
            results.pose_landmarks,
            mp.solutions.holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp.solutions.drawing_styles.get_default_pose_landmarks_style()
        )
        mp.solutions.drawing_utils.draw_landmarks(
            new_img,
            results.face_landmarks,
            mp.solutions.holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style()
        )
        return new_img, p_points