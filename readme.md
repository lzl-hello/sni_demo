# 网络流量SNI捕获与分类工具

## 目录
- [简介](#简介)
- [功能](#功能)
  - [已实现的功能](#已实现的功能)
  - [待实现的功能](#待实现的功能)
- [已解决的Bug](#已解决的bug)
- [安装指南](#安装指南)
- [使用方法](#使用方法)
- [项目结构](#项目结构)
- [日志记录](#日志记录)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 简介

**网络流量SNI捕获与分类工具** 是一个基于Python的工具，旨在实时监控和分析网络流量。该工具专注于从TLS/SSL数据包中提取服务器名称指示（SNI）信息，并通过查询PostgreSQL数据库对流量进行分类和存储，以便后续分析。

该工具特别适用于网络管理员、网络安全专业人士和研究人员，他们需要了解网络中访问的应用程序和服务类型。

## 功能

### 已实现的功能

1. **实时网络流量捕获**
   - 使用 `pyshark` 从指定的网络接口实时捕获TCP和UDP流量。

2. **SNI提取**
   - 从TLS/SSL数据包中提取SNI信息，以识别客户端在TLS握手期间请求的服务器名称。

3. **流量分类**
   - 通过查询PostgreSQL数据库，根据提取的SNI和协议（TCP/UDP）对网络流量进行分类。

4. **多线程处理**
   - 使用工作线程（Worker Threads）实现多线程架构，确保不同类别的流量能够并发处理，提高处理效率。

5. **日志记录**
   - 使用Python的 `logging` 模块记录事件、错误和调试信息。日志存储在专用日志文件中，便于监控和故障排除。

6. **数据存储**
   - 将处理后的流量数据保存到CSV文件中，便于持久存储和后续分析。

7. **前端展示**
   - 完成了简单的统计信息展示，从csv中提取数据展示在页面中

### 待实现的功能

重要功能：
1. **前端页面美化**
   - 前端页面初步展示已完成，需要美化页面样式和布局，增加更多交互功能。

2. **数据库集成增强**
   - 支持更多数据库和更复杂的分类逻辑；支持更多应用的sni分类。人工标记和自动分类的结合。

3. **子线程流量包统计处理**
   - 目前只是写了简单的数量统计，后续需要加更多功能。

其他功能：
4. **警报系统**
   - 实现警报机制，通知管理员可疑或高优先级的流量模式。

5. **配置文件**
   - 引入配置文件（如YAML或JSON），更高效地管理设置。

6. **Docker支持**
   - 使用Docker容器化应用，便于部署和扩展。

7. **异步处理**
   - 过渡到异步处理，提高性能和可扩展性，特别是在高流量负载下。

## 已解决的Bug

1. **SNI提取问题**
   - **问题**：启用 `use_json=True` 和 `include_raw=True` 时，SNI被错误解析为 `None`。
   - **解决方案**：移除了 `use_json` 和 `include_raw` 参数，确保SNI的正确提取。更新了数据包处理逻辑以在不使用这些参数的情况下进行SNI提取。

2. **协议层访问错误**
   - **问题**：访问不存在的协议层（如缺失IP层或传输层）时出现 `AttributeError`。
   - **解决方案**：添加了检查以验证所需协议层（`IP`、`TCP`、`UDP`、`TLS`、`SSL`）的存在性，避免访问不存在的层。增强了异常处理，记录并跳过不符合条件的数据包。

3. **未处理的 `KeyboardInterrupt` 异常**
   - **问题**：收到 `KeyboardInterrupt`（如Ctrl+C）导致程序非优雅终止，数据保存不完整。
   - **解决方案**：实现了信号处理，捕获 `SIGINT` 并确保所有捕获的数据被保存，资源在退出前正确释放。

4. **日志记录问题**
   - **问题**：日志文件重复记录或不同模块的日志混淆不清。
   - **解决方案**：为每个模块（`network_capture`、`worker_thread`、`db_classify_traffic`）配置独立的日志记录器，确保日志的分离和清晰。

5. **flask_socketio主动调用emit/send发送消息失败解决（伪同步flask上下文）**
   - **问题**：前端页面接收不到传来的数据。
   - **解决方案**：采用 flask_socketio 提供的 background 运行 + 队列 flush 法。
   - **参考**：https://blog.csdn.net/qq_21567385/article/details/120803123

## 安装指南

### 前提条件

- **Python 3.10 或更高版本**
- **Tshark**（Wireshark套件的一部分）
  - 确保已安装 `tshark` 并添加到系统的PATH中。
  
- **PostgreSQL数据库**
  - 需要一个运行中的PostgreSQL实例，并创建必要的表（`app_sni` 、 `app_protocol`、 `unmatched_sni_record`）用于流量分类。


## 项目结构

```
network-traffic-sni-capture/
├── db_classify_traffic.py      # 用于通过数据库分类流量的模块
├── worker_thread.py            # 管理工作线程处理流量的模块
├── network_capture.py          # 主脚本，用于捕获和处理网络流量
├── monitoring_server.py        # flask主程序
├── requirements.txt            # Python依赖包
├── README.md                   # 项目文档
├── templates/                  # 前端页面
│   └── index.html
├── log/                        # 日志文件目录
│   ├── network_capture.log
│   ├── worker_threads.log
│   ├── db_classification.log
│   └── monitoring.log
├── output/                     # 输出CSV文件目录
│   ├── network_traffic.csv
│   ├── HTTP_statistics.csv
│   └── Unclassified_statistics.csv
├── db/                         # 数据库相关目录
│   ├── app_sni.sql
│   ├── app_protocol.sql
│   └── readme.md
├── back/                       # 简单的备份代码
└── pcap/                       # （已移除）之前用于存储PCAP文件的目录
```

## 日志记录

- **日志文件位置：** `./log/`
  - `network_capture.log`：主网络捕获和处理相关的日志。
  - `worker_threads.log`：每个工作线程处理特定流量类别的日志。
  - `db_classification.log`：数据库交互和流量分类相关的日志。
  - `monitoring.log`：前端页面展示相关的日志。

- **日志级别：**
  - **DEBUG：** 用于诊断问题的详细信息。
  - **INFO：** 一般操作消息。
  - **WARNING：** 潜在问题的警示。
  - **ERROR：** 运行时错误。

- **日志轮转：**
  - 为防止日志文件过大，建议使用 `RotatingFileHandler` 或 `TimedRotatingFileHandler` 实现日志轮转。在每个模块中更新日志配置以应用轮转策略。

## 贡献指南

欢迎贡献！如果您有改进建议、Bug修复或新功能，请提交问题（Issue）或拉取请求（Pull Request）。



## 许可证

本项目采用 [MIT 许可证](LICENSE)。

