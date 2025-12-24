package com.xueye.xueyeWarn.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.xueye.xueyeWarn.bean.LoginLog;
import com.xueye.xueyeWarn.mapper.LoginLogMapper;
import com.xueye.xueyeWarn.service.LoginLogService;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
public class LoginLogServiceImpl extends ServiceImpl<LoginLogMapper, LoginLog> implements LoginLogService {
    @Override
    public IPage<LoginLog> getLoginLogPage(Page<LoginLog> page, String username, String role) {
        QueryWrapper<LoginLog> queryWrapper = new QueryWrapper<>();
        if (StringUtils.hasText(username)) {
            queryWrapper.like("username", username);
        }
        if (StringUtils.hasText(role)) {
            queryWrapper.eq("role", role);
        }
        queryWrapper.orderByDesc("login_time");
        return page(page, queryWrapper);
    }
}
