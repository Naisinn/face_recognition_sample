# Face Recognition Sample Scripts Adapted for Debian:Bookworm on Raspberry Pi

七輝(Naisinn)による変更点の説明です。オリジナル版の説明はREADME_old.mdを参照してください。

このプロジェクトは、Raspberry Pi 4 (4GB) および Raspberry Pi Camera Module v3（imx708_wide）を用いて、Debian:Bookworm 環境で顔認識および顔特徴推定を実現するために、既存のスクリプトを適合させたものです。  
変更・追加したスクリプトは以下の3つです。

- **examples/facerec_from_webcam_faster.py**
- **examples/find_facial_features_in_webcam.py**
- **examples/focus_rightEye.py**

以下に各スクリプトの概要と変更点、ならびにセットアップ手順について説明します。

---

## 実行環境

- **ハードウェア:** Raspberry Pi 4 (4GB)
- **カメラ:** Raspberry Pi Camera Module v3 (imx708_wide)
- **OS:** Debian:Bookworm
- **ライブラリ:**
  - OpenCV (opencv-python, opencv-contrib-python)
  - dlib
  - face_recognition
  - Picamera2 (apt 経由でインストールされる python3-picamera2)
  - dispFps(examples/dispFps.py)
  - その他、必要な依存パッケージ（以下セットアップ手順参照）

---

## セットアップ手順

1. **依存パッケージのインストール**  
   以下のコマンドを用いて、システムに必要な依存パッケージとビルドツールをインストールしてください。

   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   sudo apt-get install build-essential \
       cmake \
       gfortran \
       git \
       wget \
       curl \
       graphicsmagick \
       libgraphicsmagick1-dev \
       libatlas-base-dev \
       libavcodec-dev \
       libavformat-dev \
       libboost-all-dev \
       libgtk2.0-dev \
       libjpeg-dev \
       liblapack-dev \
       libswscale-dev \
       pkg-config \
       python3-dev \
       python3-numpy \
       python3-pip \
       zip
   sudo apt-get clean
   ```

2. **OpenCV のインストール**  
   メモリ不足対策のため、一時的にスワップ領域を拡張し、pip で OpenCV をインストールします。

   ```bash
   sudo nano /etc/dphys-swapfile
   # (CONF_SWAPSIZE=100 を CONF_SWAPSIZE=1024 に変更)
   sudo /etc/init.d/dphys-swapfile restart

   # OpenCV のインストール
   pip3 install opencv-contrib-python opencv-python
   ```

3. **face_recognition のインストール**  
   dlib のカスタマイズビルド後、face_recognition をインストールします。

   ```bash
   cd
   mkdir -p dlib
   git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/
   cd dlib
   sudo python3 setup.py install --compiler-flags "-mfpu=neon"

   # face_recognition のインストール
   pip3 install face_recognition
   ```

4. **スクリプト実行**  
   下記の 3 つのスクリプトを使用してください。
   - `examples/facerec_from_webcam_faster.py`
   - `examples/find_facial_features_in_webcam.py`
   - `examples/focus_rightEye.py`

---

## 各スクリプトの概要と変更点

### 1. examples/facerec_from_webcam_faster.py

- **Picamera2 を使用するよう変更**
- **顔認識処理の維持**

### 2. examples/find_facial_features_in_webcam.py

- **顔の全要素を検出・描画する処理の追加**

### 3. examples/focus_rightEye.py

- **右目座標の抽出とコンソール出力**

---

## まとめ

このプロジェクトは、Raspberry Pi の Debian:Bookworm 環境に適応し、顔認識および顔特徴推定を行うスクリプト群を更新したものです。各スクリプトは、セットアップ手順に従ってインストールした後、期待通りに動作することを確認してください。

