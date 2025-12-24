package com.xueye.xueyeWarn.config; // 包名要和你的项目一致，核心是末尾的config

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * 跨域配置类：解决前端访问后端时的跨域问题
 */
@Configuration // 标记这是一个配置类，Spring会自动加载
public class CorsConfig implements WebMvcConfigurer {

    // 重写跨域配置方法
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // 对所有接口生效（/** 表示匹配所有路径）
        registry.addMapping("/**")
                // 允许前端的域名访问（你的前端运行地址是localhost:8080，必须写对）
                .allowedOriginPatterns("http://localhost:8080") // 注意：用allowedOriginPatterns而非allowedOrigins（新版本Spring推荐）
                // 允许的请求方法（GET/POST/PUT/DELETE对应前端的增删改查）
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                // 允许携带Token、Cookie等认证信息（登录必须要这个）
                .allowCredentials(true)
                // 预检请求的有效期（3600秒=1小时，避免频繁发预检请求）
                .maxAge(3600);
    }
}