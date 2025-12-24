package com.xueye.xueyeWarn.bean;

import com.alibaba.excel.annotation.ExcelProperty;
import com.alibaba.excel.annotation.write.style.ColumnWidth;
import com.alibaba.excel.annotation.write.style.ContentRowHeight;
import com.alibaba.excel.annotation.write.style.HeadRowHeight;
import com.alibaba.excel.annotation.format.DateTimeFormat;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@HeadRowHeight(20)
@ContentRowHeight(18)
public class LoginLogExcel {
    @ExcelProperty(value = "用户名", index = 0)
    @ColumnWidth(15)
    private String username;

    @ExcelProperty(value = "角色", index = 1)
    @ColumnWidth(12)
    private String role;

    @ExcelProperty(value = "登录时间", index = 2)
    @ColumnWidth(20)
    @DateTimeFormat("yyyy-MM-dd HH:mm:ss")
    private LocalDateTime loginTime;
}
