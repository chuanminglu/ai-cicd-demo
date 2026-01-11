# 提示词03：生成GitHub Actions配置

## 🎭 角色
DevOps工程师，擅长CI/CD流水线配置。

## 📋 任务
生成传统质量门的GitHub Actions配置（包含Lint + 测试 + 覆盖率检查）。

## 🎯 目标
配置完整的传统质量门流水线。

## 📤 输出要求

### 流水线步骤
1. 代码检出
2. Python环境设置
3. 安装依赖
4. Pylint代码规范检查
5. Pytest单元测试
6. 覆盖率检查（≥80%）

### 质量标准
- Pylint评分 ≥ 8.0
- 测试覆盖率 ≥ 80%
- 所有测试通过

---

## 💬 复制以下内容到AI

```
你是DevOps专家。生成GitHub Actions配置文件：

要求：
1. 文件名：quality-gate.yml
2. 触发条件：push和pull_request
3. 步骤：
   - Checkout代码
   - 设置Python 3.9
   - 安装依赖（pytest、pytest-cov、pylint）
   - Pylint检查（fail-under=8.0）
   - Pytest测试（--cov=src --cov-fail-under=80）
   - 输出质量门总结

4. Python项目结构：
   - 代码目录：src/
   - 测试目录：tests/

直接输出YAML配置，不要解释。
```

---

## ✅ 验证输出

生成的配置应该：
- [ ] 文件格式为有效的YAML
- [ ] 包含所有必需步骤
- [ ] 触发条件为push和pull_request
- [ ] 包含质量门检查（Lint + Test + Coverage）
