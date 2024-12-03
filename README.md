# AdaptiveADS

### Run Carla Server
```shell
sudo docker pull carlasim/carla:0.9.10.1
sudo docker run -e SDL_VIDEODRIVER=offscreen -e SDL_HINT_CUDA_DEVICE=0 -p 2000-2002:2000-2002 -itd --name carla --rm --gpus all carlasim/carla:0.9.10.1 ./CarlaUE4.sh -world-port=2000 -opengl
```

### Setup Conda Env
```shell
git clone https://github.com/EunhoCho/AdaptiveADS
conda create -n adaptiveADS python=3.7
conda activate adaptiveADS
conda install cudatoolkit==11.3 -c pytorch
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
pip install tqdm==4.43.0 diskcache==5.3.0 timm==0.5.4 Shapely==1.7.0 mmdet==2.25.0 ujson==5.3.0 scikit-learn==0.22.2.post1 scikit-image==0.16.2 opencv-python==4.2.0.32 mmsegmentation==0.25.0 pygame==2.0.1 py-trees==0.8.3 xmlschema==1.0.18 tabulate==0.8.7 dictor==0.1.5
pip install torch-scatter==2.0.9 -f https://data.pyg.org/whl/torch-1.11.0+cu113.html
pip install mmcv-full==1.5.3 -f https://download.openmmlab.com/mmcv/dist/cu113/torch1.11.0/index.html
```

### Setup Carla
```shell
./setup_carla.sh
pip install setuptools==41
easy_install carla/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg
pip3 install setuptools==68
```

