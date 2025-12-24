package com.xueye.xueyeWarn.controller;

import com.xueye.xueyeWarn.bean.Result;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.OperatingSystemMXBean;
import java.lang.management.ThreadMXBean;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/systemResource")
public class SystemResourceController {

    private List<Map<String, Object>> getGPUInfo() {
        List<Map<String, Object>> gpuList = new ArrayList<>();
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("nvidia-smi", "--query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.used,memory.free", "--format=csv,noheader,nounits");
            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(", ");
                if (parts.length >= 8) {
                    Map<String, Object> gpuInfo = new HashMap<>();
                    gpuInfo.put("index", Integer.parseInt(parts[0].trim()));
                    gpuInfo.put("name", parts[1].trim());
                    gpuInfo.put("temperature", Integer.parseInt(parts[2].trim()));
                    gpuInfo.put("gpuUtilization", Integer.parseInt(parts[3].trim()));
                    gpuInfo.put("memoryUtilization", Integer.parseInt(parts[4].trim()));
                    gpuInfo.put("totalMemory", Long.parseLong(parts[5].trim()));
                    gpuInfo.put("usedMemory", Long.parseLong(parts[6].trim()));
                    gpuInfo.put("freeMemory", Long.parseLong(parts[7].trim()));
                    gpuList.add(gpuInfo);
                }
            }

            process.waitFor();
            reader.close();
        } catch (Exception e) {
            return null;
        }
        return gpuList.isEmpty() ? null : gpuList;
    }

    @GetMapping("/info")
    public Result<Map<String, Object>> getSystemResourceInfo() {
        Map<String, Object> resourceInfo = new HashMap<>();

        OperatingSystemMXBean osBean = ManagementFactory.getOperatingSystemMXBean();
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();

        long totalPhysicalMemory = 0;
        long freePhysicalMemory = 0;

        try {
            Method getTotalPhysicalMemorySizeMethod = osBean.getClass().getMethod("getTotalPhysicalMemorySize");
            Method getFreePhysicalMemorySizeMethod = osBean.getClass().getMethod("getFreePhysicalMemorySize");
            totalPhysicalMemory = (long) getTotalPhysicalMemorySizeMethod.invoke(osBean);
            freePhysicalMemory = (long) getFreePhysicalMemorySizeMethod.invoke(osBean);
        } catch (Exception e) {
            totalPhysicalMemory = Runtime.getRuntime().totalMemory();
            freePhysicalMemory = Runtime.getRuntime().freeMemory();
        }

        long usedPhysicalMemory = totalPhysicalMemory - freePhysicalMemory;

        int availableProcessors = osBean.getAvailableProcessors();
        String osName = osBean.getName();
        String osVersion = osBean.getVersion();
        double systemLoadAverage = osBean.getSystemLoadAverage();

        long heapMemoryUsed = memoryBean.getHeapMemoryUsage().getUsed();
        long heapMemoryMax = memoryBean.getHeapMemoryUsage().getMax();
        long nonHeapMemoryUsed = memoryBean.getNonHeapMemoryUsage().getUsed();

        int threadCount = threadBean.getThreadCount();

        resourceInfo.put("osName", osName);
        resourceInfo.put("osVersion", osVersion);
        resourceInfo.put("availableProcessors", availableProcessors);
        resourceInfo.put("systemLoadAverage", systemLoadAverage);

        resourceInfo.put("totalMemory", totalPhysicalMemory / (1024 * 1024));
        resourceInfo.put("usedMemory", usedPhysicalMemory / (1024 * 1024));
        resourceInfo.put("freeMemory", freePhysicalMemory / (1024 * 1024));
        resourceInfo.put("memoryUsagePercent", (double) usedPhysicalMemory / totalPhysicalMemory * 100);

        resourceInfo.put("heapMemoryUsed", heapMemoryUsed / (1024 * 1024));
        resourceInfo.put("heapMemoryMax", heapMemoryMax / (1024 * 1024));
        resourceInfo.put("nonHeapMemoryUsed", nonHeapMemoryUsed / (1024 * 1024));

        resourceInfo.put("threadCount", threadCount);

        List<Map<String, Object>> gpuInfo = getGPUInfo();
        if (gpuInfo != null) {
            resourceInfo.put("gpuAvailable", true);
            resourceInfo.put("gpuList", gpuInfo);
        } else {
            resourceInfo.put("gpuAvailable", false);
            resourceInfo.put("gpuInfo", "GPU信息不可用（需要NVIDIA GPU和CUDA）");
        }

        return Result.success(resourceInfo);
    }
}
