# SOA-Backend

### superuser
username:user

email:123@edu.com

password:123

### 数据库结构

| location     | Text                     |
| ------------ | ------------------------ |
| job_title    | Text (max length  = 100) |
| level        | Text                     |
| corporate    | Text                     |
| requirements | Text(json format)        |

example:

```json
id: 1
location: Mountain View, CA, USA
job_title: Software Engineer
level: Entry level
corporate: Google
requirements: ["BS in Computer Science or equivalent", "Experience in software development", "Experience with Python, Java, or C++"]
```

在SOA/database/db.sqlite3中保存有～60条目
