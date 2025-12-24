package com.xueye.xueyeWarn.bean;

import lombok.AllArgsConstructor;
import lombok.Data;

// 统一接口返回格式，前端更容易处理
@Data
@AllArgsConstructor  // 新增：生成包含所有字段的全参构造器
public class Result<T> {
    private Integer code;  // 状态码：200成功，500失败
    private String msg;    // 提示信息
    private T data;        // 返回数据

    // 成功（带数据）
    public static <T> Result<T> success(T data) {
        return new Result<>(200, "操作成功", data);
    }

    // 成功（无数据）
    public static <T> Result<T> success() {
        return new Result<>(200, "操作成功", null);
    }

    // 失败
    public static <T> Result<T> fail(String msg) {
        return new Result<>(500, msg, null);
    }
}