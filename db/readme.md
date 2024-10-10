# PostgreSQL 数据库导入指南

本指南简要介绍如何在 **Windows** 操作系统上将 `app_sni.sql` 和 `app_protocol.sql` 两个 SQL 文件导入到 PostgreSQL 数据库中，并介绍这两个表的结构和用途。

## 表结构介绍

### 1. `app_sni` 表

该表用于存储服务器名称指示（SNI）与应用程序 ID (`app_id`) 之间的映射关系。

- **字段**：
  - `sni`：服务器名称指示，通常为域名（例如 `www.example.com`）。
  - `app_id`：对应的应用程序标识符，用于在 `app_protocol` 表中查找应用名称。

- **用途**：
  通过 SNI 信息，可以识别出流量所属的应用程序，实现流量分类和管理。

### 2. `app_protocol` 表

该表用于存储应用程序 ID (`app_id`) 与应用程序名称 (`app_name`) 之间的映射关系。

- **字段**：
  - `app_id`：应用程序标识符，与 `app_sni` 表中的 `app_id` 对应。
  - `app_name`：应用程序名称（例如 `HTTP`、`DNS`、`哔哩哔哩` 等）。

- **用途**：
  通过 `app_id`，将 SNI 信息映射到具体的应用程序名称，便于对网络流量进行分类和分析。

### 3. `unmatched_sni_record` 表

该表用于存储应用程序 ID (`app_id`) 与应用程序名称 (`unknow`) 之间的映射关系。

- **字段**：
  - `app_id`：应用程序标识符，与 `app_sni` 表中的 `app_id` 对应。
  - `app_name`：应用程序名称（unknow）。

- **用途**：
  记录未识别的sni，后续人工审查更新到app_sni表中。

## 导入 SQL 文件步骤（Windows）

### 前提条件

- **安装 PostgreSQL**：确保您的系统已安装 PostgreSQL，并且可以正常运行。
- **SQL 文件准备**：确保您已下载或获取了 `app_sni.sql` 和 `app_protocol.sql` 文件。

### 使用 `psql` 导入 SQL 文件

1. **打开命令提示符**：

   按下 `Win + R`，输入 `cmd`，然后按回车，打开命令提示符窗口。

2. **导航到 SQL 文件所在目录**：

   使用 `cd` 命令切换到存放 `app_sni.sql` 和 `app_protocol.sql` 文件的目录。例如：
   ```bash
   cd C:\path\to\sql\files
   ```

3. **连接到 PostgreSQL 数据库**：

   使用 `psql` 命令连接到目标数据库。如果尚未创建目标数据库，请先创建一个。例如，创建名为 `network_traffic_db` 的数据库：
   ```bash
   psql -U postgres
   ```
   在 `psql` 提示符下，输入以下命令创建数据库：
   ```sql
   CREATE DATABASE network_traffic_db;
   \q
   ```

4. **导入 `app_sni.sql` 文件**：

   在命令提示符中运行以下命令，将 `app_sni.sql` 文件导入到 `network_traffic_db` 数据库中：
   ```bash
   psql -U postgres -d network_traffic_db -f app_sni.sql
   ```

5. **导入 `app_protocol.sql` 文件**：

   类似地，运行以下命令将 `app_protocol.sql` 文件导入到同一数据库中：
   ```bash
   psql -U postgres -d network_traffic_db -f app_protocol.sql
   ```

   **注意**：如果您的 PostgreSQL 用户不是 `postgres`，请将 `-U postgres` 替换为您的用户名。

### 使用 pgAdmin 导入 SQL 文件（可选）

如果您更喜欢使用图形界面工具，可以使用 pgAdmin 来导入 SQL 文件。

1. **打开 pgAdmin**：

   启动 pgAdmin 并连接到您的 PostgreSQL 服务器。

2. **创建新数据库（如果尚未创建）**：

   - 右键点击 "Databases" 节点，选择 "Create" > "Database..."。
   - 输入数据库名称（例如 `network_traffic_db`），然后点击 "Save"。

3. **导入 SQL 文件**：

   - 在 pgAdmin 中，展开您刚创建的数据库。
   - 右键点击 "Schemas" 下的 "public"（或您使用的模式），选择 "Query Tool"。
   - 在查询编辑器中，点击工具栏上的 "Open File" 图标，选择 `app_sni.sql` 文件，然后点击 "Execute"（运行）。
   - 重复上述步骤导入 `app_protocol.sql` 文件。

## 验证导入结果

1. **连接到数据库**：

   使用 `psql` 或 pgAdmin 连接到 `network_traffic_db` 数据库。

2. **列出表**：

   在 `psql` 中运行：
   ```sql
   \dt
   ```
   应显示 `app_sni` 和 `app_protocol` 表。

3. **查看表结构**：

   - **`app_sni` 表**：
     ```sql
     \d app_sni
     ```
   - **`app_protocol` 表**：
     ```sql
     \d app_protocol
     ```

4. **预览数据**：

   - **`app_sni` 表**：
     ```sql
     SELECT * FROM app_sni LIMIT 5;
     ```
   - **`app_protocol` 表**：
     ```sql
     SELECT * FROM app_protocol LIMIT 5;
     ```

## 配置项目中的数据库连接

确保您的项目能够连接到刚导入数据的 PostgreSQL 数据库。编辑项目中的配置文件（例如 `db_classify_traffic.py`），更新数据库连接参数：

```python
# db_classify_traffic.py
db_config = {
    'dbname': 'network_traffic_db',
    'user': 'postgres',          # 替换为您的用户名
    'password': 'your_password', # 替换为您的密码
    'host': 'localhost',
    'port': '5432'
}
```

**注意**：确保密码和其他连接参数正确无误，以便项目能够成功连接到数据库。

---

*注：请将示例路径和用户名替换为您实际使用的值。*