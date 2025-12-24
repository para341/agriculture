package com.xueye.xueyeWarn.service;

import com.xueye.xueyeWarn.bean.User;
import java.util.List;

public interface UserService {
    User getUserByUsername(String username);
    List<User> getAllUsers();
    User getUserById(Integer id);
    int addUser(User user);
    int updateUser(User user);
    int deleteUser(Integer id);
}