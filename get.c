#include <stdio.h>
#include <gpiod.h>
#include <time.h>

#define GPIO_CHIP_PATH "/dev/gpiochip0"  // GPIO 控制器路径
#define SDA 12  // 要读取的 GPIO 引脚（这里使用 GPIO 12）
#define SCL 13  // 要读取的 GPIO 引脚（这里使用 GPIO 12）

int main(void) {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    struct gpiod_line *line1;
    int value, count = 0;
    int value1 = 0;
    char *bits = malloc(7500000);
    char *bits1 = malloc(7500000);
    if (bits == NULL || bits1 == NULL) {
        perror("Failed to allocate memory");
        return 1;
    }
    clock_t start, end;
    printf("OK");
    // 打开 GPIO 控制器
    chip = gpiod_chip_open(GPIO_CHIP_PATH);
    if (!chip) {
        perror("Failed to open GPIO chip");
        return 1;
    }

    // 获取 GPIO 引脚
    line = gpiod_chip_get_line(chip, SDA);
    if (!line) {
        perror("Failed to get GPIO line");
        gpiod_chip_close(chip);
        return 1;
    }
    line1 = gpiod_chip_get_line(chip, SCL);
    if (!line1) {
        perror("Failed to get GPIO line");
        gpiod_chip_close(chip);
        return 1;
    }

    // 设置为输入模式
    if (gpiod_line_request_input(line, "gpio_speed_test") < 0) {
        perror("Failed to request GPIO line as input");
        gpiod_chip_close(chip);
        return 1;
    }
    if (gpiod_line_request_input(line1, "gpio_speed_test") < 0) {
        perror("Failed to request GPIO line as input");
        gpiod_chip_close(chip);
        return 1;
    }

    // 记录开始时间
    start = clock();
    // 在 1 秒内循环读取 GPIO 引脚的电平
    while (1) {
        value = gpiod_line_get_value(line);  // 读取电平
        value1 = gpiod_line_get_value(line1);  // 读取电平
        
        if (value < 0) {
            perror("Failed to read GPIO line");
            gpiod_chip_close(chip);
            return 1;
        }
        if (value1 < 0) {
            perror("Failed to read GPIO line");
            gpiod_chip_close(chip);
            return 1;
        }
        
        bits[count] = value;
        bits1[count] = value1;
        count++;  // 计数
        
        // 每秒钟输出一次读取的次数
        end = clock();
        if ((double)(end - start) / CLOCKS_PER_SEC >= 1.0) {
            printf("GPIO read count in 1 second: %d\n", count);
            break;
        }
    }

    // 关闭 GPIO 控制器
    gpiod_chip_close(chip);
    
        // 打开文件用于写入
    FILE *file = fopen("output_SDA.txt", "w");
    if (file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    // 将 bits 数组的内容写入文件
    for (int i = 0; i < count; i++) {
        fprintf(file, "%d", bits[i]);  // 写入每个 bit
    }

    // 关闭文件
    fclose(file);

    printf("Data written to outputSDA.txt successfully!\n");
    
    FILE *file1 = fopen("output_SCL.txt", "w");
    if (file1 == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    // 将 bits 数组的内容写入文件
    for (int i = 0; i < count; i++) {
        fprintf(file1, "%d", bits1[i]);  // 写入每个 bit
    }

    // 关闭文件
    fclose(file1);
    free(bits);
    free(bits1);
    printf("Data written to outputSCL.txt successfully!\n");     
    
    return 0;
}
