package com.xueye.xueyeWarn.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.xueye.xueyeWarn.bean.LoginLog;

public interface LoginLogService extends IService<LoginLog> {
    IPage<LoginLog> getLoginLogPage(Page<LoginLog> page, String username, String role);
}
