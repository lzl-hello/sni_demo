# db_classify_traffic.py
import psycopg2
import logging

# 设置 db_classify_traffic 的日志记录器
logger = logging.getLogger('db_classify_traffic')
logger.setLevel(logging.DEBUG)

# 检查是否已经添加处理器，避免重复添加
if not logger.handlers:
    db_handler = logging.FileHandler('./log/db_classification.log')
    db_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    db_handler.setFormatter(formatter)
    logger.addHandler(db_handler)
    logger.propagate = False  # 防止日志传播到根记录器

# 数据库连接配置
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# 从数据库中分类流量
def classify_traffic_from_db(sni, protocol):
    try:
        # 连接数据库
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        app_name = None

        # 如果存在 SNI，尝试查找对应的 app_id
        if sni:
            cursor.execute("SELECT app_id FROM app_sni WHERE sni = %s", (sni,))
            app_id_result = cursor.fetchone()

            if app_id_result:
                app_id = app_id_result[0]
                cursor.execute("SELECT app_name FROM app_protocol WHERE app_id = %s", (app_id,))
                app_name_result = cursor.fetchone()

                if app_name_result:
                    app_name = app_name_result[0]
                    logger.debug(f"SNI {sni} 对应的应用名称: {app_name}")
                    return f"{app_name} Traffic", app_name
                else:
                    logger.warning(f"SNI {sni} 对应的 app_id {app_id} 没有找到应用名称。")
                    return "Unknown App Traffic", "Unknown App"
            else:
                logger.warning(f"SNI {sni} 没有找到对应的 app_id。")
                return "Other SNI Traffic", "Other SNI"
        else:
            # 如果没有 SNI，根据协议分类
            if protocol == 'HTTP':
                logger.debug("根据协议分类为 HTTP Traffic。")
                return "HTTP Traffic", "HTTP"
            elif protocol == 'DNS':
                logger.debug("根据协议分类为 DNS Traffic。")
                return "DNS Traffic", "DNS"
            else:
                logger.debug("协议未分类，归类为 Unclassified。")
                return "Unclassified", "Unclassified"
    except Exception as e:
        logger.error(f"Database error: {e}")
        return "Database Error", "Database Error"
    finally:
        # 关闭数据库连接
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            logger.debug("数据库连接已关闭。")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
