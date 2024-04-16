# SOA-Backend

### superuser
username:user

email:123@edu.com

password:123

### 数据库结构

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

在SOA/database/db.sqlite3中保存有～60条目
