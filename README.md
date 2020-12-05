# fintools
这是一个白银基金套利网站的后端代码。

## 环境需求
* Python 3.6 or above

## 使用
```
cd fintools/ # 进入到项目目录
python -m venv venv # 创建虚拟环境
pip install -r requirement.txt  # 安装依赖
flask run 
```

## 接口
1. ```http://localhost:5000/get_live_data_of_ag```

获取白银的实时数据

method： GET


2. ```http://localhost:5000/get_ag_history```

获取历史数据

method： GET

参数：limit  数据条数（可选）  默认为20

