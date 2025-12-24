package com.xueye.xueyeWarn.controller;

import com.xueye.xueyeWarn.bean.LoginLog;
import com.xueye.xueyeWarn.bean.Result;
import com.xueye.xueyeWarn.bean.User;
import com.xueye.xueyeWarn.service.LoginLogService;
import com.xueye.xueyeWarn.service.UserService;
import com.xueye.xueyeWarn.utils.JwtUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/login")
public class LoginController {

    @Autowired
    private UserService userService;

    @Autowired
    private LoginLogService loginLogService;

    @PostMapping
    public Result<String> login(@RequestBody User user) {
        User dbUser = userService.getUserByUsername(user.getUsername());
        if (dbUser == null) {
            return Result.fail("用户名不存在");
        }

        if (!dbUser.getPassword().equals(user.getPassword())) {
            return Result.fail("密码错误");
        }

        if (!dbUser.getRole().equals(user.getRole())) {
            return Result.fail("角色不匹配");
        }

        String token = JwtUtils.generateToken(user.getUsername(), dbUser.getRole());

        LoginLog loginLog = new LoginLog();
        loginLog.setUsername(user.getUsername());
        loginLog.setRole(dbUser.getRole());
        loginLog.setLoginTime(LocalDateTime.now());
        loginLogService.save(loginLog);

        return Result.success(token);
    }
}
