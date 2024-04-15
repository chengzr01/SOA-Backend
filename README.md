# SOA-Backend

## 接口设计

- 在`main.py`里设计顶层Django接口，用于前后端通信。
- 目前需要实现的顶层接口对应的第二层接口：
    - `src/query.py`


## 模块文档

- src
    - `api.py`: 定义`FrontEndAgent`和`BackEndAgent`类，实例化后用于一个用户的输入流 LLM 理解。
    - `config.py`: 配置、宏定义
    - `query.py`: `FrontEndAgent`和`BackEndAgent`接口

- test
    - `test.py`: 单元测试

- `main.py`: 后端顶层接口定义