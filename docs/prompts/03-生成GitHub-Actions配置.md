# 提示词03：生成GitHub Actions配置

## 🎭 角色
DevOps工程师，擅长CI/CD流水线配置。

## 📋 任务
生成传统质量门的GitHub Actions配置（包含Lint + 测试 + 覆盖率检查）。

## 🎯 目标
配置完整的传统质量门流水线。

## 📤 输出要求

### 流水线步骤
1. 代码检出（actions/checkout@v3）
2. Python环境设置（Python 3.9）
3. 安装依赖（支持requirements.txt）
4. Pylint代码规范检查（评分≥8.0）
5. Pytest单元测试（带详细输出）
6. 覆盖率检查（≥80%，生成HTML报告）
7. 上传HTML覆盖率报告（artifact）

### 质量标准
- Pylint评分 ≥ 8.0
- 测试覆盖率 ≥ 80%
- 所有测试通过
- 生成可下载的HTML覆盖率报告

---

## 💬 复制以下内容到AI

```
你是DevOps专家。生成GitHub Actions配置文件：

要求：
1. 文件名：quality-gate.yml
2. 触发条件：push和pull_request到main/develop分支
3. 步骤：
   - Checkout代码（使用actions/checkout@v3）
   - 设置Python 3.9（使用actions/setup-python@v4）
   - 安装依赖（pytest、pytest-cov、pylint，支持requirements.txt）
   - Pylint检查（fail-under=8.0，输出text格式）
   - Pytest测试（--cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80 -v）
   - 输出质量门总结（使用emoji，展示所有检查结果）
   - 上传HTML覆盖率报告（使用actions/upload-artifact@v4，上传htmlcov/目录）

4. Python项目结构：
   - 代码目录：src/
   - 测试目录：tests/

5. 特别要求：
   - 每个步骤添加中文说明和emoji
   - 如果检查失败立即退出（|| exit 1）
   - 覆盖率报告步骤使用if: always()确保总是执行

直接输出YAML配置，不要解释。
```

---

## ✅ 验证输出

生成的配置应该：
- [ ] 文件格式为有效的YAML
- [ ] 包含所有必需步骤（7个步骤）
- [ ] 触发条件为push和pull_request到main/develop分支
- [ ] 包含质量门检查（Lint + Test + Coverage）
- [ ] Pytest命令包含 `--cov-report=html` 生成HTML报告
- [ ] 使用 `actions/upload-artifact@v4` 上传 `htmlcov/` 目录
- [ ] 上传步骤使用 `if: always()` 确保总是执行
- [ ] 每个步骤有清晰的中文名称和emoji
