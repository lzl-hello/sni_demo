# db_classify_traffic.py
import psycopg2
import logging
import re

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
    'dbname': 'xxx',
    'user': 'postgres',
    'password': 'xxx',
    'host': 'localhost',
    'port': '5432'
}

# SQL 语句模板
SELECT_UNMATCHED_SNI_SQL = """
SELECT 1 FROM unmatched_sni_records WHERE sni = %s
"""

INSERT_UNMATCHED_SNI_SQL = """
INSERT INTO unmatched_sni_records (sni, app_name)
VALUES (%s, %s)
"""

# 从数据库中分类流量
def classify_traffic_from_db(sni, protocol):
    try:
        # 连接数据库
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        app_name = None

        # 如果存在 SNI，尝试查找对应的 app_id
        if sni:
            # 使用正则表达式匹配 SNI
            # cursor.execute("SELECT app_id FROM app_sni WHERE %s ~ sni", (sni,))
            cursor.execute("SELECT app_name FROM sni_re WHERE %s ~ sni_re", (sni,))
            app_name_result = cursor.fetchone()

            if app_name_result:
                # app_id = app_id_result[0]
                # cursor.execute("SELECT app_name FROM app_protocol WHERE app_id = %s", (app_id,))
                app_name = app_name_result[0]

                # if app_name_result:
                #     app_name = app_name_result[0]
                logger.debug(f"SNI {sni} 对应的应用名称: {app_name}")
                return f"{app_name} Traffic", app_name
            else:
                logger.warning(f"SNI {sni} 没有找到应用名称。")
                return "Unknown App Traffic", "Unknown App"
            # else:
            #     logger.warning(f"SNI {sni} 没有找到对应的 app_id。")
            #     # 插入未匹配的 SNI 记录
            #     insert_unmatched_sni(sni)
            #     return "Other SNI Traffic", "Other SNI"

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


def insert_unmatched_sni(sni):
    """
    插入未匹配的 SNI 记录到 unmatched_sni_records 表中，如果该 SNI 尚未存在。

    :param sni: 未匹配的 Server Name Indication
    """
    if not sni:
        logger.warning("尝试插入空的 SNI。")
        return

    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                # 检查 SNI 是否已存在
                cursor.execute(SELECT_UNMATCHED_SNI_SQL, (sni,))
                exists = cursor.fetchone()

                if not exists:
                    # 插入新记录
                    cursor.execute(INSERT_UNMATCHED_SNI_SQL, (sni, "unknown"))
                    conn.commit()
                    logger.debug(f"已插入未匹配的 SNI 记录: SNI='{sni}', app_name='unknown'")
                else:
                    logger.debug(f"SNI '{sni}' 已存在于 unmatched_sni_records 表中，无需重复插入。")
    except psycopg2.Error as db_err:
        logger.error(f"插入未匹配的 SNI 记录时数据库错误: {db_err}")
    except Exception as e:
        logger.error(f"插入未匹配的 SNI 记录时发生错误: {e}")
