package com.xueye.xueyeWarn;

import org.mybatis.spring.annotation.MapperScan; // 新增导入
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.xueye.xueyeWarn.mapper") // 新增：扫描Mapper接口所在包
public class XueyeWarnBackendApplication {
    public static void main(String[] args) {
        SpringApplication.run(XueyeWarnBackendApplication.class, args);
    }
}