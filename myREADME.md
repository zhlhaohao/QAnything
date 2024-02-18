此仓库是从QAnything（https://github.com/netease-youdao/QAnything） fork而来，并做出了以下几点调整和改进：
1. 取消了原系统对GPU的要求，现在可以在CPU上进行推理（embeding和rerank模型推理）
2. 由于取消了GPU，所以不能做LLM本地推理，只能采用cloud的llm服务（chatgpt3.5）
3. 把前端和后端代码从容器中分离出来，这样前后端可以在宿主机上进行开发、调试（例如通过vscode打断点、单步执行等）
4. 只支持wsl2环境，因为本人没有linux环境，所以只能在wsl2上进行开发

## 1. wsl2安装nodejs

```bash
wget https://nodejs.org/download/release/v18.19.0/node-v18.19.0-linux-x64.tar.gz
# 创建目录用于存放Node.js
sudo mkdir -p /usr/local/lib/nodejs
# 解压Node.js压缩包到指定目录
sudo tar -zxvf node-v18.19.0-linux-x64.tar.gz -C /usr/local/lib/nodejs
# 设置环境变量，将Node.js的bin目录加入到PATH中
ENV PATH="/usr/local/lib/nodejs/node-v18.19.0-linux-x64/bin:${PATH}"
rm node-v18.19.0-linux-x64.tar.gz
```

## 2. wsl2安装miniconda
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
~/miniconda3/bin/conda init bash
```

## 3. miniconda创建python 3.10环境，
```bash
conda create -n py310-qany python=3.10
conda activate py310-qany
git clone https://github.com/zhlhaohao/QAnything.git

cd QAnything
pip_inst  # 安装必要的库文件

# 下载模型文件，pull docker相关的镜像，运行不成功没关系，只要模型下载成功，镜像拉下来就好
bash run.sh -c cloud
```

## 4. 修改下载下来的模型配置文件: models/embed/config.pbtxt 和 models/rerank/config.pbtxt ,将最后的几行覆盖成下面的内容（目的是改用cpu进行推理，我没有GPU）：
```
  {
    name: "embed"
    count: 1
    kind: KIND_CPU
  }

  {
    name: "rerank"
    count: 1
    kind: KIND_CPU
  }  
```

## 5. wsl2上 sudo vi /etc/hosts，增加下面几行（将后端代码移出容器后，要让这些域名还能找得到）：
```
127.0.0.1       milvus-standalone-local
127.0.0.1       milvus-etcd-local
127.0.0.1       mysql-container-local
127.0.0.1       milvus-minio-local
```

## 6. 以生产方式独立运行后端(全部在容器运行，不能调试，就是qanything原来的模式)
1. 将docker-compose-windows-prod.yaml内容拷贝到docker-compose-windows.yaml
2. 新开terminal
```bash
run.sh -c cloud
```

## 7. 以开发调试方式运行
  1. 将docker-compose-windows-dev.yaml的内容拷贝到docker-compose-windows.yaml(**这个很重要**)
  2. 启动容器：新开一个terminal，以容器方式运行mysql，向量数据库、embed模型推理、rerank模型推理等 - 需要输入chatgpt的apikey（如果没有在淘宝上购买一个）,服务器选择"local"，如果openai api地址国内无法访问，那么就申请一个cloudflare的代理转发，然后把代理地址覆盖到.env文件的OPENAI_API_BASE项
  ```bash
  run.sh -c cloud
  ```


  3. 新开一个terminal,运行前端代码
  ```bash
  cd front_end 
  npm install --registry=https://registry.npmmirror.com && npm run build && npm run serve
  ```

  4. vscode以调试模式运行后端代码，首先.vscode/launch.json增加一个调试项目，然后点击“start debugging”：
  ```json
  {
    "name": "run api",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/qanything_kernel/qanything_server/sanic_api.py",
    "args": [
      "--mode",
      "online"
    ],
    "env": {
      "LLM_API_SERVE_PORT":"7802",
      "RERANK_PORT":"9001",
      "EMBED_PORT":"9001"
    },      
    "console": "integratedTerminal",
    "cwd": "${workspaceFolder}",
    "justMyCode": false
  }
  ```

  或者直接在terminal运行
  ```bash
  LLM_API_SERVE_PORT=7802 RERANK_PORT=9001 EMBED_PORT=9001 python3 -u qanything_kernel/qanything_server/sanic_api.py --mode "online"
  ```


## 8. 打开页面地址进行问答
http://127.0.0.1:5052/qanything/

