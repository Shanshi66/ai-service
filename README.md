# AI Service

通用AI Service，支持通用AI任务，目前支持：

- 文章摘要

# 部署方法

1. 根据指导安装serverless-devs并配置阿里云密钥：https://docs.serverless-devs.com/serverless-devs/quick_start
2. 通过阿里云函数部署，在阿里云函数中使用requirements.txt创建自定义层，替换掉`s.yaml`中的python package
    ![image](./image/create-layer.png)

3. 更改环境变量：
   - `LLM_HOST`: https://api.openai.com/v1, 或者其他代理服务器 # proxy server for openai, default: https://api.openai.com/v1
   - `LLM_TOKENS`: api_token
   - `LLM_TYPE`: openai # 暂时只支持openai

4. 在项目目录运行`s deploy`即可

# 接口


