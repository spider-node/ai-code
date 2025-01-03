import mysql.connector
from mysql.connector import Error


class MySQLDatabase:
    def __init__(self, host, database, user, password):
        self.connection = None
        try:
            print("==================")
            self.connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=3306,

            )
            print("=====================")
            if self.connection.is_connected():
                print("MySQL Database connection successful")
        except Error as e:
            print(f"Error: {e}")

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def _format_query(self, query, params):
        """ 将参数字典中的值替换到SQL模板中的占位符。"""
        for key, value in params.items():
            placeholder = f"#{{{key}}}"
            # 为防止SQL注入，对参数进行转义
            escaped_value = self.connection.converter.escape(value)
            query = query.replace(placeholder, escaped_value)
        return query

    def execute_query(self, query, params=None):
        """ 执行给定的SQL查询。"""
        cursor = self.connection.cursor(dictionary=True)
        try:
            if params:
                query = self._format_query(query, params)
            cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Failed to execute query: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def update(self, query, params):
        """ 执行更新操作。"""
        return self.execute_query(query, params)

    def insert(self, query, params):
        """ 执行插入操作。"""
        return self.execute_query(query, params)


# 使用示例
if __name__ == "__main__":
    # 创建数据库实例
    db = MySQLDatabase(host='47.109.67.130', database='spider_demo', user='spider_demo', password='spider_demo')
    insert_sql = "INSERT INTO stock (id, good_code, good_name, good_number, lock_status, lock_code, lock_number, create_time, update_time) VALUES (#{id}, #{good_code}, #{good_name}, #{good_number}, #{lock_status}, #{lock_code}, #{lock_number}, NOW(), NOW())"
    insert_params = {'id': 1, 'good_code': '001', 'good_name': '商品A', 'good_number': 10, 'lock_status': '4156', 'lock_code': '11258', 'lock_number': 0}
    if db.insert(insert_sql, insert_params):
        print("Insert successful")
    else:
        print("Insert failed")

    # 关闭数据库连接
    db.close()
