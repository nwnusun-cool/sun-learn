import requests
from requests.auth import HTTPBasicAuth

# Harbor 实例信息
harbor_url = 'http://175.188.189.148:19999/'
username = 'xian-rd'
password = 'Hbis@123'

def get_projects(auth):
    url = f'{harbor_url}/api/v2.0/projects'
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

def get_repositories(project_name, auth):
    url = f'{harbor_url}/api/v2.0/projects/{project_name}/repositories'
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

def main():
    # 创建认证对象
    auth = HTTPBasicAuth(username, password)

    # 获取所有项目
    projects = get_projects(auth)

    for project in projects:
        project_name = project['name']
        print(f'项目: {project_name}')

        # 获取该项目中的所有镜像（仓库）
        repositories = get_repositories(project_name, auth)
        for repo in repositories:
            repo_name = repo['name']
            print(f'  仓库: {repo_name}')

            # 获取该仓库中的所有标签（即具体的镜像）
            tags_url = f'{harbor_url}/api/v2.0/projects/{project_name}/repositories/{repo_name}/artifacts'
            tags_response = requests.get(tags_url, auth=auth)
            tags_response.raise_for_status()
            tags = tags_response.json()
            for tag in tags:
                tag_name = tag['tags'][0]['name'] if tag['tags'] else 'unknown'
                print(f'    标签: {tag_name}')

if __name__ == '__main__':
    main()
