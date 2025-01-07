## 启动记录

1. git clone https://github.com/facebookresearch/sam2.git
2. cd sam2
3. 安装 python3.10(M1 芯片使用 pyenv 安装 3.10 报错，所以使用下面方式)
   - brew install python@3.10
   - 确认安装成功：python3.10 --version
   - 安装目录：/opt/homebrew/bin/python3.10
4. 创建&激活虚拟环境(可用 vscode 拓展去创建)
   - python3.10 -m venv venv
   - source venv/bin/activate
5. 下载检查点：
   cd checkpoints && \
   ./download_ckpts.sh && \
   cd ..
6. 安装项目依赖
   - pip install -e .
   - pip install -e ".[demo]"
   - 运行 demo 项目的话，要根据 demo/README.md 进行操作,目前 M1 芯片启动起来，会显示不支持，可能也是要切换 cpu 模型来进行推理
7. 创建 start.py 文件&运行文件
   - `/Users/xmly/Documents/shadow/sam2/.venv
/bin/python /Users/xmly/Documents/shadow/sam2/start_two_point.py`
