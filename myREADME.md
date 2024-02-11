1、**wsl安装python环境**
```
conda create -n py310-qany python=3.10
conda activate py310-qany
setproxy
git clone https://github.com/zhlhaohao/QAnything.git

cd QAnything
pip_inst

# 下载模型文件，pull docker镜像并运行
bash run.sh
```



2、**编译运行前端**
```
cd QAnything/front_end

npm install
npm run build
npm run serve
```

3、**运行后端**
```
LLM_API_SERVE_PORT=7802 RERANK_PORT=9001 EMBED_PORT=9001 python3 -u qanything_kernel/qanything_server/sanic_api.py --mode "online"


LLM_API_SERVE_PORT=7802 RERANK_PORT=9001 EMBED_PORT=9001 python3 -u qanything_kernel/dependent_server/rerank_for_local_serve/rerank_server.py
```



http://127.0.0.1:5052/qanything/



bash ./run.sh -c cloud -i 0 -b default



instance_group [
  {
    name: "embed"
    count: 1
    kind: KIND_CPU
  }