# Hand_landmark_torch
手部關節點訓練及測試

## 1. 環境及教學說明
安裝環境:
- 顯卡 2060
- torch == 1.10.1、CUDA = 11.3.1、cuDNN = 8.2.1.32

- [參考網站](https://towardsdatascience.com/gentle-introduction-to-2d-hand-pose-estimation-lets-code-it-6c82046d4acf)
- 使用資料庫 : [FreiHAND](https://lmb.informatik.uni-freiburg.de/resources/datasets/FreihandDataset.en.html)


## 2. 文件內容
- notebooks/Train Notebook.ipynb (訓練模型)
- notebooks/Inference Notebook.ipynb (驗證模型)
- utils/model.py (模型架構)
- utils/dataset.py (FreiHAND 資料庫載入)
- utils/trainer.py (訓練函式)
- utils/prep_utils.py (函式庫)
- weights/model_final (存權重位置)
- requirements.txt (安裝包)
