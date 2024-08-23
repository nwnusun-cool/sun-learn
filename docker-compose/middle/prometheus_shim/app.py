import os
import shutil
import re
import requests
from flask import Flask, request, jsonify
# 导入日志
from loguru import logger

app = Flask(__name__)

# 获取环境变量 PROMETHEUS_URL 的值，如果不存在则使用默认值 http://localhost:9090
prometheus_url = os.environ.get('PROMETHEUS_URL', 'localhost:9090')


class ApiResponse:
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    def to_json(self):
        return {'message': self.message, 'code': self.status_code}


def flush():
    response = requests.post(f'http://{prometheus_url}/-/reload')
    if response.status_code == 200:
        return ApiResponse('Prometheus configuration reloaded successfully.', 200)
    else:
        return ApiResponse(f'Failed to reload Prometheus configuration. Status code: {response.status_code}', 500)


# 更新Prometheus配置文件并触发动态刷新配置
def update_prometheus_config(file, config):
    # 更新Prometheus配置文件
    if not file:
        logger.error('File name is required.')
        return ApiResponse('File name is required.', 400)

    if file == 'prometheus.yml':
        backup_file = os.path.join('/opt', f'{file}.bak')
        update_file = os.path.join('/opt', file)
    else:
        backup_file = os.path.join('/opt', 'alert_rules', f'{file}.bak')
        update_file = os.path.join('/opt', 'alert_rules', file)

    logger.info(f'Updating Prometheus configuration file: {update_file}')
    # 备份原始配置文件
    try:
        shutil.copy(update_file, backup_file)
    except Exception as backup_err:
        logger.error(f'Failed to backup Prometheus configuration: {backup_err}')
        return ApiResponse(f'Failed to backup Prometheus configuration: {backup_err}', 500)

    # 尝试更新配置文件
    try:
        if config:
            with open(update_file, 'w') as f:
                f.write(config)

        return flush()

    except Exception as write_err:
        # 如果更新失败，回滚备份文件
        try:
            shutil.copy(backup_file, update_file)
        except Exception as rollback_err:
            logger.error(f'Failed to rollback Prometheus configuration: {rollback_err}')
        return ApiResponse(f'Failed to update Prometheus configuration: {write_err}', 500)


# 获取当前Prometheus配置的API端点
@app.route('/get-config/<filename>', methods=['GET'])
def get_config(filename):
    try:
        if not filename:
            return jsonify(ApiResponse('Missing filename parameter', 400).to_json())

        if filename == 'prometheus.yml':
            filename = '/opt/prometheus.yml'
        else:
            filename = f'/opt/alert_rules/{filename}'

        with open(filename, 'r') as f:
            current_config = f.read()
        return jsonify(ApiResponse(current_config, 200).to_json())
    except FileNotFoundError:
        return ApiResponse('Prometheus configuration file not found.', 404).to_json()
    except Exception as e:
        return ApiResponse(f'Error occurred while fetching Prometheus configuration: {e}', 500).to_json()


# 定义一个用于接收配置更新的API端点
@app.route('/update-config', methods=['POST'])
def update_config():
    info = request.json
    if info.get('data', []):
        # 解析传入的配置信息
        data = request.json['data']
        data = re.sub(r'\\\\', '', data)
        # 调用更新Prometheus配置的函数
        response = update_prometheus_config(info.get('fileName', []), data)
    else:
        # 如果没有传入配置数据，则只执行刷新操作
        response = flush()

    return jsonify(response.to_json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
