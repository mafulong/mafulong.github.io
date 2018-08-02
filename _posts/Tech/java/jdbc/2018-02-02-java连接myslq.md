---
layout: post
category: JAVA
title: java连接Mysql例子
---

intellij idea添加jar，参考学习中blog

## 连接
```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class DBHelper {
    public static final String url = "jdbc:mysql://127.0.0.1/testdb";
    public static final String name = "com.mysql.jdbc.Driver";
    public static final String user = "root";
    public static final String password = "123456";

    public Connection conn = null;
    public PreparedStatement pst = null;

    public DBHelper(String sql) {
        try {
            Class.forName(name);//指定连接类型  
            conn = DriverManager.getConnection(url, user, password);//获取连接  
            pst = conn.prepareStatement(sql);//准备执行语句  
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void close() {
        try {
            this.conn.close();
            this.pst.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

## 查询（主类)
```java
import java.sql.ResultSet;
import java.sql.SQLException;

public class Demo {

    static String sql = null;
    static DBHelper db1 = null;
    static ResultSet ret = null;

    public static void main(String[] args) {
        sql = "select * from employee";//SQL语句
        db1 = new DBHelper(sql);//创建DBHelper对象  

        try {
            ret = db1.pst.executeQuery();//执行语句，得到结果集  
            while (ret.next()) {
                String uid=ret.getString(1);
                String ufname = ret.getString(2);
                String ulname = ret.getString(3);
                String udate = ret.getString(4);
                System.out.println(uid + "\t" + ufname + "\t" + ulname + "\t" + udate );
            }//显示数据  
            ret.close();
            db1.close();//关闭连接  
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

}  
```