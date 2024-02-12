**wsl安装python环境**
```
conda create -n py310-qany python=3.10
conda activate py310-qany
setproxy
git clone https://github.com/zhlhaohao/QAnything.git

cd QAnything
pip_inst

# 下载模型文件，pull docker镜像并运行
run.sh

修改embed/config.pbtxt 和 rerank/config.pbtxt 的最后几行：
instance_group [
  {
    name: "embed"
    count: 1
    kind: KIND_CPU
  }

编辑 /etc/hosts：
127.0.0.1       milvus-standalone-local
127.0.0.1       milvus-etcd-local
127.0.0.1       mysql-container-local
127.0.0.1       milvus-minio-local

```



**编译运行前端**
```
cd QAnything/front_end
npm install
npm run build
npm run serve
```


**生产方式独立运行**
将docker-compose-windows-prod.yaml内容拷贝到docker-compose-windows.yaml
```bash
run.sh -c cloud
```

**调试方式运行**
1. 将docker-compose-windows-prod.yaml内容拷贝到docker-compose-windows.yaml

2. 新开一个terminal，docker方式运行服务，向量数据库、embed、rerank等
```bash
run.sh -c cloud_dev
```


3. 新开一个terminal,运行前端
```bash
cd front_end && npm run build && npm run serve
```

4. ctrl+p 开始后台api的调试，launch.json为
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
```bash
LLM_API_SERVE_PORT=7802 RERANK_PORT=9001 EMBED_PORT=9001 python3 -u qanything_kernel/qanything_server/sanic_api.py --mode "online"
```


**前端地址**
http://127.0.0.1:5052/qanything/



