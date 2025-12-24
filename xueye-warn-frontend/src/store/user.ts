// src/store/user.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUserStore = defineStore('user', () => {
    const token = ref(localStorage.getItem('token') || '');
    const role = ref(localStorage.getItem('role') || '');

    const setToken = (newToken: string) => {
        token.value = newToken;
        localStorage.setItem('token', newToken);
    };

    const setRole = (newRole: string) => {
        role.value = newRole;
        localStorage.setItem('role', newRole);
    };

    const clearToken = () => {
        token.value = '';
        role.value = '';
        localStorage.removeItem('token');
        localStorage.removeItem('role');
    };

    const isLoggedIn = () => {
        return !!token.value;
    };

    const isAdmin = () => {
        return role.value === 'admin';
    };

    const isStudent = () => {
        return role.value === 'student';
    };

    return {
        token,
        role,
        setToken,
        setRole,
        clearToken,
        isLoggedIn,
        isAdmin,
        isStudent
    };
});
