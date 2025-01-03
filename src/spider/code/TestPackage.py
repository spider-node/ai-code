from src.spider.code.tool.CodeTool import generate_package


def check_import_section(java_code):
    lines = java_code.splitlines()
    in_import_section = False  # 标记是否在import代码块中
    missing_imports = []
    found_class_definition = False

    for line in lines:
        stripped_line = line.strip()

        # 如果遇到了 package 声明，则开始进入 import 区域
        if stripped_line.startswith('package'):
            in_import_section = True
            continue

        # 如果遇到了 public class 定义，则结束 import 区域
        if 'public class' in stripped_line:
            found_class_definition = True
            break

        # 在 import 区域中检查是否有缺少 'import' 关键字的导入语句
        if in_import_section and stripped_line and not stripped_line.startswith(('import', '@')):
            if stripped_line.endswith(';'):
                missing_imports.append(line)

    if missing_imports:
        print("Warning: Found potential import statements without 'import' keyword:")
        for miss in missing_imports:
            print(f"- {miss.strip()}")
        return False
    else:
        if found_class_definition:
            print("All import statements in the import section seem to be correctly prefixed with 'import'.")
        else:
            print("No class definition found, could not verify import section.")
        return True

# 示例Java代码字符串
java_code_string = """
f"```java
package cn.spider.spider.order.update.order.status.component.spider.service;

cn.spider.framework.annotation.NoticeScope;
lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeanUtils;

@Component
public class UpdateOrderStatusComponent {
    // Class code...
}
\n```"
"""

if __name__ == '__main__':
    check_import_section(java_code_string)



