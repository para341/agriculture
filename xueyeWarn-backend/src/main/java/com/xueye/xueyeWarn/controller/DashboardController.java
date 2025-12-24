package com.xueye.xueyeWarn.controller;

import com.xueye.xueyeWarn.bean.Result;
import com.xueye.xueyeWarn.service.DashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/dashboard")
public class DashboardController {

    @Autowired
    private DashboardService dashboardService;

    // 1. 数据卡片统计
    @GetMapping("/cards")
    public Result<Map<String, Integer>> getDashboardCards() {
        return Result.success(dashboardService.getDashboardCards());
    }

    // 2. 专业分布饼图
    @GetMapping("/majorDistribution")
    public Result<Map<String, Object>> getMajorDistribution() {
        return Result.success(dashboardService.getMajorDistribution());
    }

    // 3. 各专业预警人数柱状图
    @GetMapping("/majorWarning")
    public Result<Map<String, Object>> getMajorWarningData() {
        return Result.success(dashboardService.getMajorWarningData());
    }

    // 4. 预警等级性别分布
    @GetMapping("/genderWarning")
    public Result<Map<String, Object>> getGenderWarningData() {
        return Result.success(dashboardService.getGenderWarningData());
    }

    // 5. 各专业平均绩点
    @GetMapping("/majorAvgGrade")
    public Result<Map<String, Object>> getMajorAvgGrade() {
        return Result.success(dashboardService.getMajorAvgGrade());
    }
}