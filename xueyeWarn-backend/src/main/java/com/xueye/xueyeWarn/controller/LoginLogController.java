package com.xueye.xueyeWarn.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.xueye.xueyeWarn.bean.LoginLog;
import com.xueye.xueyeWarn.bean.LoginLogExcel;
import com.xueye.xueyeWarn.bean.Result;
import com.xueye.xueyeWarn.service.LoginLogService;
import com.xueye.xueyeWarn.util.ExcelUtil;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletResponse;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/loginLog")
public class LoginLogController {

    @Autowired
    private LoginLogService loginLogService;

    @GetMapping("/page")
    public Result<IPage<LoginLog>> getLoginLogPage(
            @RequestParam(defaultValue = "1") Integer current,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) String username,
            @RequestParam(required = false) String role) {
        Page<LoginLog> page = new Page<>(current, size);
        IPage<LoginLog> result = loginLogService.getLoginLogPage(page, username, role);
        return Result.success(result);
    }

    @DeleteMapping("/{id}")
    public Result<String> deleteLoginLog(@PathVariable Integer id) {
        loginLogService.removeById(id);
        return Result.success("删除成功");
    }

    @DeleteMapping("/batch")
    public Result<String> batchDeleteLoginLog(@RequestBody java.util.List<Integer> ids) {
        loginLogService.removeByIds(ids);
        return Result.success("批量删除成功");
    }

    @GetMapping("/export")
    public void exportLoginLogExcel(HttpServletResponse response) {
        try {
            Page<LoginLog> page = new Page<>(1, 10000);
            IPage<LoginLog> result = loginLogService.getLoginLogPage(page, null, null);
            List<LoginLogExcel> excelList = result.getRecords().stream().map(log -> {
                LoginLogExcel excel = new LoginLogExcel();
                BeanUtils.copyProperties(log, excel);
                return excel;
            }).collect(Collectors.toList());
            ExcelUtil.export(response, "登录日志", LoginLogExcel.class, excelList);
        } catch (Exception e) {
            throw new RuntimeException("导出登录日志Excel失败: " + e.getMessage());
        }
    }
}
