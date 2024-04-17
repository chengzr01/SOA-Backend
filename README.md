# SOA-Backend

## 接口设计

- 在`main.py`里设计顶层Django接口，用于前后端通信。
- 目前需要实现的顶层接口对应的第二层接口：
    - `src/query.py`
- 给到后端数据库用于查询的数据结构：
    ``` python
    {
        "company name": "Google", 
        "job title": "Research Intern"
    }
    ```

## 模块文档

- src
    - `api.py`: 定义`FrontEndAgent`和`BackEndAgent`类，实例化后用于一个用户的输入流 LLM 理解。
    - `config.py`: 配置、宏定义
    - `query.py`: `FrontEndAgent`和`BackEndAgent`接口

- test
    - `test.py`: 单元测试

- `main.py`: 后端顶层接口定义


## superuser
username:user

email:123@edu.com

password:123

## 数据库结构

| Key          | Field                    |
| ------------ | ------------------------ |
| location     | Text                     |
| job_title    | Text (max length  = 100) |
| level        | Text                     |
| corporate    | Text                     |
| requirements | Text                     |
| id           | Int (django db默认的primary key） |

example:

```json
{
  	"id": 2,
	"location": "Chicago, IL, USA",
	"job_title": "Technical Delivery Executive, State and Local Government",
	"level": "Advanced",
	"corporate": "Google",
	"requirements": '["Bachelor's degree in a technical field, or equivalent practical experience.", "8 years of experience in program management.", "Successful candidates will be required to possess or obtain US Government Top Secret/Sensitive Compartmentalized Information (TS/SCI) security clearance, as this is an essential requirement for this role."]',
}
```

现在在SOA/database/db.sqlite3中保存有～2500条目
