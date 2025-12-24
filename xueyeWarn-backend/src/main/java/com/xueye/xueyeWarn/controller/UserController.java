package com.xueye.xueyeWarn.controller;

import com.xueye.xueyeWarn.bean.Result;
import com.xueye.xueyeWarn.bean.User;
import com.xueye.xueyeWarn.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/user")
@Validated
public class UserController {

    private static final Logger log = LoggerFactory.getLogger(UserController.class);

    @Autowired
    private UserService userService;

    @GetMapping("/list")
    public Result<List<User>> getAllUsers() {
        log.info("收到获取所有用户的请求");
        List<User> users = userService.getAllUsers();
        log.info("返回用户数据，数量: {}", users.size());
        return Result.success(users);
    }

    @GetMapping("/{id}")
    public Result<User> getUserById(@PathVariable Integer id) {
        User user = userService.getUserById(id);
        if (user == null) {
            return Result.fail("用户不存在");
        }
        return Result.success(user);
    }

    @PostMapping("/add")
    public Result<Integer> addUser(@Valid @RequestBody User user) {
        User existingUser = userService.getUserByUsername(user.getUsername());
        if (existingUser != null) {
            return Result.fail("用户名已存在");
        }
        int rows = userService.addUser(user);
        return Result.success(rows);
    }

    @PutMapping("/update")
    public Result<Integer> updateUser(@Valid @RequestBody User user) {
        int rows = userService.updateUser(user);
        return Result.success(rows);
    }

    @DeleteMapping("/delete/{id}")
    public Result<Integer> deleteUser(@PathVariable Integer id) {
        User user = userService.getUserById(id);
        if (user == null) {
            return Result.fail("用户不存在");
        }
        int rows = userService.deleteUser(id);
        return Result.success(rows);
    }
}
