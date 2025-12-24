# 学业预警系统

<div align="center">

![Spring Boot](https://img.shields.io/badge/Spring%20Boot-2.7.18-brightgreen)
![Vue](https://img.shields.io/badge/Vue-3.0-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

一个基于 Spring Boot + Vue3 的学业预警管理系统，适合大学生学习和参考

[功能介绍](#功能特性) · [快速开始](#快速开始) · [项目结构](#项目结构) · [API文档](#api文档)

</div>

---

## 📖 项目简介

学业预警系统是一个面向高校的学生学业管理平台，旨在帮助学生和教师及时发现和解决学业问题。系统提供学生信息管理、学业预警、登录日志追踪、系统资源监控等功能，并集成了Hadoop文件存储。

本项目适合作为大学生学习 Spring Boot + Vue3 全栈开发的参考项目，代码结构清晰，注释完善，易于理解和扩展。

## ✨ 功能特性

### 🔐 用户管理
- 用户登录/登出（JWT认证）
- 用户CRUD操作
- 角色权限管理（管理员/学生）

### 👨‍🎓 学生管理
- 学生信息CRUD
- 学业预警等级（正常/预警/严重）
- 学生信息搜索（学号/姓名/专业）
- Excel数据导出

### 📊 预警统计
- 预警等级统计
- 预警原因分析
- 建议措施推荐

### 📝 登录日志
- 登录记录追踪
- 日志分页查询
- 批量删除功能
- Excel数据导出

### 💾 Hadoop文件管理
- HDFS文件上传
- HDFS文件下载
- HDFS文件列表查看
- HDFS文件删除

### 🖥️ 系统资源监控
- CPU使用率监控
- 内存使用情况
- 磁盘空间监控
- 实时数据展示

### 📈 仪表盘
- 数据可视化展示
- 统计图表
- 快速导航

---

## 🛠 技术栈

### 后端技术
| 技术 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 2.7.18 | 核心框架 |
| MyBatis-Plus | 3.5.3.1 | ORM框架 |
| MySQL | 8.0 | 数据库 |
| Hadoop | 3.3.4 | 分布式文件系统 |
| JWT | 0.9.1 | 身份认证 |
| Lombok | 1.18.30 | 简化代码 |
| EasyExcel | 3.2.1 | Excel处理 |
| Validation | - | 参数校验 |

### 前端技术
| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.x | 渐进式框架 |
| TypeScript | - | 类型系统 |
| Element Plus | - | UI组件库 |
| Axios | - | HTTP客户端 |
| Vue Router | - | 路由管理 |

---

## 📁 项目结构

```
xueyeproject/
├── xueyeWarn-backend/          # 后端项目
│   ├── src/
│   │   └── main/
│   │       ├── java/com/xueye/xueyeWarn/
│   │       │   ├── bean/       # 实体类
│   │       │   │   ├── User.java
│   │       │   │   ├── Student.java
│   │       │   │   ├── LoginLog.java
│   │       │   │   ├── StudentExcel.java
│   │       │   │   └── LoginLogExcel.java
│   │       │   ├── controller/ # 控制器
│   │       │   │   ├── UserController.java
│   │       │   │   ├── StudentController.java
│   │       │   │   ├── LoginLogController.java
│   │       │   │   ├── HadoopController.java
│   │       │   │   ├── SystemResourceController.java
│   │       │   │   └── DashboardController.java
│   │       │   ├── service/    # 服务层
│   │       │   │   ├── UserService.java
│   │       │   │   ├── StudentService.java
│   │       │   │   └── LoginLogService.java
│   │       │   ├── mapper/     # 数据访问层
│   │       │   │   ├── UserMapper.java
│   │       │   │   └── StudentMapper.java
│   │       │   ├── exception/  # 异常处理
│   │       │   │   ├── BusinessException.java
│   │       │   │   └── GlobalExceptionHandler.java
│   │       │   ├── util/       # 工具类
│   │       │   │   ├── JwtUtil.java
│   │       │   │   └── ExcelUtil.java
│   │       │   └── XueyeWarnApplication.java
│   │       └── resources/
│   │           ├── application.yml      # 配置文件
│   │           └── mapper/              # MyBatis映射文件
│   └── pom.xml
│
└── xueye-warn-frontend/         # 前端项目
    ├── public/
    ├── src/
    │   ├── api/               # API接口
    │   │   ├── login.ts
    │   │   ├── student.ts
    │   │   ├── loginLog.ts
    │   │   ├── hadoop.ts
    │   │   ├── systemResource.ts
    │   │   └── user.ts
    │   ├── views/             # 页面组件
    │   │   ├── Login.vue
    │   │   ├── Dashboard.vue
    │   │   ├── Student.vue
    │   │   ├── LoginLog.vue
    │   │   ├── Hadoop.vue
    │   │   ├── SystemResource.vue
    │   │   └── User.vue
    │   ├── layout/            # 布局组件
    │   ├── router/            # 路由配置
    │   ├── store/             # 状态管理
    │   ├── utils/             # 工具函数
    │   ├── types/             # 类型定义
    │   ├── App.vue
    │   └── main.ts
    └── package.json
```

---

## 🚀 快速开始

### 环境要求

- JDK 1.8+
- Node.js 14+
- MySQL 8.0+
- Maven 3.6+
- Hadoop 3.3.4（可选，用于文件存储功能）

### 数据库初始化

1. 创建数据库
```sql
CREATE DATABASE xueye_warn CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 创建数据表

**用户表**
```sql
CREATE TABLE `user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
  `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
  `password` VARCHAR(100) NOT NULL COMMENT '密码',
  `role` VARCHAR(20) NOT NULL COMMENT '角色(admin/student)',
  INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 插入默认管理员账号（密码: admin123）
INSERT INTO `user` (username, password, role) VALUES ('admin', 'admin123', 'admin');
```

**学生表**
```sql
CREATE TABLE `student` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
  `student_id` VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
  `name` VARCHAR(50) NOT NULL COMMENT '姓名',
  `gender` VARCHAR(10) NOT NULL COMMENT '性别',
  `major` VARCHAR(100) NOT NULL COMMENT '专业',
  `grade` DECIMAL(5,2) COMMENT '平均绩点',
  `warning_level` VARCHAR(20) DEFAULT 'normal' COMMENT '预警等级(normal/warning/serious)',
  INDEX idx_student_id (student_id),
  INDEX idx_warning_level (warning_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生表';
```

**登录日志表**
```sql
CREATE TABLE `login_log` (
  `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `role` VARCHAR(20) NOT NULL COMMENT '角色(admin/student)',
  `login_time` DATETIME NOT NULL COMMENT '登录时间',
  INDEX idx_username (username),
  INDEX idx_role (role),
  INDEX idx_login_time (login_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='登录日志表';
```

### 后端启动

1. 修改配置文件
```yaml
# xueyeWarn-backend/src/main/resources/application.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/xueye_warn?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=utf8
    username: root
    password: 你的MySQL密码  # 修改为你的MySQL密码
```

2. 安装依赖
```bash
cd xueyeWarn-backend
mvn clean install
```

3. 启动应用
```bash
mvn spring-boot:run
```

或使用IDE直接运行 `XueyeWarnApplication.java`

后端服务将在 `http://localhost:8081/api` 启动

### 前端启动

1. 安装依赖
```bash
cd xueye-warn-frontend
npm install
```

2. 启动开发服务器
```bash
npm run serve
```

前端服务将在 `http://localhost:8080` 启动

3. 访问应用
打开浏览器访问 `http://localhost:8080`，使用默认管理员账号登录：
- 用户名：`admin`
- 密码：`admin123`

---

## 📊 数据库表结构

### user（用户表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INT | 主键ID | PRIMARY KEY, AUTO_INCREMENT |
| username | VARCHAR(50) | 用户名 | NOT NULL, UNIQUE |
| password | VARCHAR(100) | 密码 | NOT NULL |
| role | VARCHAR(20) | 角色 | NOT NULL |

### student（学生表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INT | 主键ID | PRIMARY KEY, AUTO_INCREMENT |
| student_id | VARCHAR(20) | 学号 | NOT NULL, UNIQUE |
| name | VARCHAR(50) | 姓名 | NOT NULL |
| gender | VARCHAR(10) | 性别 | NOT NULL |
| major | VARCHAR(100) | 专业 | NOT NULL |
| grade | DECIMAL(5,2) | 平均绩点 | - |
| warning_level | VARCHAR(20) | 预警等级 | DEFAULT 'normal' |

### login_log（登录日志表）
| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | INT | 主键ID | PRIMARY KEY, AUTO_INCREMENT |
| username | VARCHAR(50) | 用户名 | NOT NULL |
| role | VARCHAR(20) | 角色 | NOT NULL |
| login_time | DATETIME | 登录时间 | NOT NULL |

---

## 📡 API文档

### 认证相关
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/login` | POST | 用户登录 |
| `/api/user/info` | GET | 获取当前用户信息 |

### 学生管理
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/student/list` | GET | 获取所有学生 |
| `/api/student/{id}` | GET | 根据ID查询学生 |
| `/api/student/add` | POST | 添加学生 |
| `/api/student/update` | PUT | 修改学生 |
| `/api/student/delete/{id}` | DELETE | 删除学生 |
| `/api/student/export` | GET | 导出学生信息Excel |
| `/api/student/stats` | GET | 预警统计 |

### 登录日志
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/loginLog/page` | GET | 分页查询日志 |
| `/api/loginLog/{id}` | DELETE | 删除日志 |
| `/api/loginLog/batch` | DELETE | 批量删除日志 |
| `/api/loginLog/export` | GET | 导出日志Excel |

### Hadoop文件管理
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/hadoop/upload` | POST | 上传文件到HDFS |
| `/api/hadoop/download` | GET | 从HDFS下载文件 |
| `/api/hadoop/list` | GET | 获取HDFS文件列表 |
| `/api/hadoop/delete` | DELETE | 删除HDFS文件 |

### 系统资源监控
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/systemResource/info` | GET | 获取系统资源信息 |

---

## 🎯 核心功能讲解

### 1. 全局异常处理

系统采用全局异常处理机制，统一处理各种异常，返回友好的错误信息。

**实现方式：**
- 创建自定义异常类 `BusinessException`
- 使用 `@RestControllerAdvice` 注解创建全局异常处理器
- 处理业务异常、参数校验异常、系统异常等

**优势：**
- 统一错误响应格式
- 减少重复的try-catch代码
- 便于日志记录和错误追踪

### 2. 参数校验

使用 `javax.validation` 注解进行参数校验，避免手动判断参数是否为空。

**常用注解：**
- `@NotBlank` - 字符串不能为空
- `@NotNull` - 对象不能为null
- `@Min` / `@Max` - 数值范围
- `@Email` - 邮箱格式
- `@Pattern` - 正则表达式

**使用示例：**
```java
public class User {
    @NotBlank(message = "用户名不能为空")
    private String username;

    @NotBlank(message = "密码不能为空")
    private String password;
}
```

### 3. Excel导入导出

使用阿里巴巴的 EasyExcel 库实现Excel导入导出功能。

**优势：**
- 内存占用低，支持百万级数据
- API简单易用
- 支持注解方式定义Excel格式

**使用示例：**
```java
@ExcelProperty(value = "学号", index = 0)
private String studentId;

@ExcelProperty(value = "姓名", index = 1)
private String name;
```

### 4. JWT身份认证

使用JWT（JSON Web Token）进行用户身份认证。

**流程：**
1. 用户登录成功后，后端生成JWT令牌
2. 前端将令牌存储在localStorage
3. 后续请求携带令牌进行身份验证
4. 后端解析令牌验证用户身份

**优势：**
- 无状态，易于扩展
- 跨域支持好
- 性能优于Session

### 5. MyBatis-Plus

使用MyBatis-Plus简化数据库操作。

**优势：**
- 内置通用Mapper，无需编写XML
- 支持代码生成器
- 分页插件简单易用
- 条件构造器灵活强大

---

## 📸 项目截图

### 登录页面
![登录页面](docs/images/login.png)

### 仪表盘
![仪表盘](docs/images/dashboard.png)

### 学生管理
![学生管理](docs/images/student.png)

### 登录日志
![登录日志](docs/images/loginlog.png)

---

## ❓ 常见问题

### 1. 后端启动失败

**问题：** 端口被占用
```bash
# 查找占用8081端口的进程
netstat -ano | findstr 8081

# 结束进程
taskkill /PID 进程ID /F
```

**问题：** 数据库连接失败
- 检查MySQL服务是否启动
- 检查application.yml中的数据库配置
- 确认数据库已创建

### 2. 前端启动失败

**问题：** 依赖安装失败
```bash
# 清除缓存重新安装
npm cache clean --force
npm install
```

**问题：** 端口被占用
```bash
# 修改vue.config.js中的端口配置
devServer: {
  port: 8080  // 修改为其他端口
}
```

### 3. Excel导出失败

**问题：** 文件下载失败
- 检查后端接口是否正常返回
- 检查浏览器是否阻止下载
- 查看浏览器控制台错误信息

### 4. Hadoop功能不可用

**问题：** Hadoop连接失败
- 确认Hadoop服务已启动
- 检查Hadoop配置文件
- 确认Hadoop版本兼容性

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 👨‍💻 作者

- 作者：para341
- 邮箱：19903128077@163.com
- GitHub：https://github.com/para341/school

---

## 🙏 致谢

感谢以下开源项目：

- [Spring Boot](https://spring.io/projects/spring-boot)
- [Vue.js](https://vuejs.org/)
- [Element Plus](https://element-plus.org/)
- [MyBatis-Plus](https://baomidou.com/)
- [EasyExcel](https://github.com/alibaba/easyexcel)

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 邮箱：19903128077@163.com
- 🔗 GitHub：https://github.com/para341/school
- 📝 提交 Issue

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by xueye

</div>
