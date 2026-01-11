# AI赋能CI/CD学员实操演练

> **演练时长**：60分钟
> **案例场景**：电商积分兑换价格计算
> **核心目标**：体验传统质量门 vs AI赋能质量门的差异

---

## 📋 演练概述

### 学习目标

- 掌握传统CI/CD质量门的搭建
- 理解传统质量门的盲区（规则检查 vs 业务逻辑）
- 体验AI如何补足人的经验不足
- 学会集成AI到CI/CD流水线

### 案例说明

**业务场景**：电商用户使用优惠券+积分兑换商品

**核心漏洞**：当优惠金额超过商品价格时，系统会计算出负价格（倒贴钱）

**教学设计**：

1. 让AI生成**故意包含漏洞**的代码
2. 让AI生成**覆盖率100%但遗漏边界**的测试
3. 传统质量门全部通过✅（但代码有致命漏洞）
4. AI审查发现漏洞❌（拦截部署）

---

## 📚 准备工作（5分钟）

### 环境检查

```bash
# 检查Git版本
git --version  # 需要 >= 2.0

# 检查Python版本
python --version  # 需要 >= 3.8

# 检查GitHub账号
# 访问 https://github.com 确保已登录
```

### 创建项目目录

```bash
# 创建项目
mkdir ai-cicd-demo
cd ai-cicd-demo

# 初始化Git
git init
git branch -M main

# 创建目录结构
mkdir src, tests, .github\workflows
```

### ✅ 阶段0检查点

- [ ] Git、Python已安装
- [ ] 项目目录已创建
- [ ] GitHub账号可访问

---

## 🎯 阶段1：生成缺陷代码（10分钟）

### 步骤1.1：使用AI生成价格计算代码

📋 **使用提示词**：[prompts/01-生成缺陷代码.md](../prompts/01-生成缺陷代码.md)

**操作步骤**：

1. 打开Claude/ChatGPT/Copilot Chat
2. 复制提示词内容，粘贴执行
3. 将生成的代码保存为 `src/price_calculator.py`

**预期生成**（参考）：

```python
class PriceCalculator:
    def calculate_final_price(self, original_price, discount_coupon, points_value):
        """计算最终价格"""
        # ⚠️ 漏洞：未检查负数
        final_price = original_price - discount_coupon - points_value
        return final_price
```

### 步骤1.2：使用AI生成单元测试

📋 **使用提示词**：[prompts/02-生成单元测试.md](../prompts/02-生成单元测试.md)

**操作步骤**：

1. 复制提示词，提供刚生成的代码作为输入
2. 将生成的测试保存为 `tests/test_price_calculator.py`
3. 创建空的 `__init__.py`：

```bash
# 创建Python包标识文件
touch src/__init__.py
touch tests/__init__.py
```

### 步骤1.3：本地验证测试通过

```bash
# 安装依赖
pip install pytest pytest-cov

# 运行测试（应该全部通过）
pytest tests/ -v

# 检查覆盖率（应该100%）
pytest tests/ --cov=src --cov-report=term-missing
```

### ✅ 阶段1检查点

- [ ] `src/price_calculator.py` 已创建
- [ ] `tests/test_price_calculator.py` 已创建
- [ ] 运行 `pytest` 全部通过
- [ ] 运行 `pytest --cov=src` 显示100%覆盖率

💡 **关键观察**：测试全部通过，覆盖率100%，但代码有漏洞！

---

## 🔧 阶段2：搭建传统质量门（15分钟）

### 步骤2.1：使用AI生成GitHub Actions配置

📋 **使用提示词**：[prompts/03-生成GitHub-Actions配置.md](../prompts/03-生成GitHub-Actions配置.md)

**操作步骤**：

1. 复制提示词执行
2. 将生成的配置保存为 `.github/workflows/quality-gate.yml`

### 步骤2.2：创建依赖文件

创建 `requirements.txt`：

```
pytest==7.4.0
pytest-cov==4.1.0
pylint==2.17.4
```

### 步骤2.3：本地验证质量门

在推送代码前，先在本地执行质量门检查，确保所有检查都能通过：

```bash
# 步骤1：安装依赖
pip install -r requirements.txt

# 步骤2：Pylint代码质量检查（要求评分 >= 8.0）
python -m pylint src/ --fail-under=8.0
```

### 步骤2.4：创建GitHub仓库

**操作步骤**：

1. 访问 https://github.com/new
2. 仓库名：`ai-cicd-demo`
3. 类型：Public（私有仓库Actions需要付费）
4. 不勾选任何初始化选项
5. 点击"Create repository"

### 步骤2.5：推送代码到GitHub

```bash
# 添加所有文件
git add .
git commit -m "feat: add price calculator with traditional quality gate"

# 关联远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/ai-cicd-demo.git

# 推送代码
git push -u origin main
```

### 步骤2.6：查看Actions运行结果

**操作步骤**：

1. 访问你的仓库页面
2. 点击"Actions"标签页
3. 观察流水线执行情况

**预期结果**：

```
✅ Checkout code              (5s)
✅ Set up Python              (8s)
✅ Install dependencies       (15s)
✅ Lint with pylint           (3s)  Score: 9.8/10
✅ Run unit tests             (2s)  Coverage: 100%
✅ Quality Gate Check         (1s)
✅ Upload coverage report     (2s)

Total: 36s - SUCCESS 🎉
```

### 步骤2.7：下载并查看覆盖率报告

**操作步骤**：

1. 在Actions流水线详情页面，滚动到页面底部
2. 找到 **Artifacts** 区域
3. 点击下载 `coverage-report`
4. 解压缩后，用浏览器打开 `index.html`

**查看内容**：

- 📊 整体覆盖率统计（100%）
- 📁 每个文件的详细覆盖情况
- 🎨 代码行级别的覆盖高亮

💡 **提示**：HTML报告比终端输出更直观，可以看到哪些代码行被测试覆盖。


---

## 🤖 阶段3：AI发现问题（15分钟）

> **💡 简化说明**：本阶段重点是体验AI代码审查能力，无需本地操作，直接在GitHub网页上完成。

### 步骤3.1：在GitHub上查看已推送的代码

**操作步骤**：

1. 访问你的GitHub仓库页面
2. 点击 `src/price_calculator.py` 文件
3. 观察代码内容，特别是 `calculate_final_price` 方法

**关键观察**：
- ✅ 代码简洁清晰
- ✅ Pylint评分10.0/10
- ✅ 测试覆盖率100%
- ⚠️ 但存在负价格漏洞（我们即将用AI发现）

### 步骤3.2：使用AI审查代码

📋 **使用提示词**：[prompts/04-AI代码审查.md](../prompts/04-AI代码审查.md)

**操作步骤**：

1. 在GitHub仓库页面，点击 `src/price_calculator.py` 文件
2. 点击右上角"复制"按钮，复制代码
3. 打开Claude/ChatGPT/Copilot Chat（任选一个）
4. 打开提示词文件，复制提示词内容
5. 将提示词和代码一起发送给AI
6. 阅读AI的审查反馈

💡 **提示**：如果有GitHub Copilot订阅，可以在Issues或Discussions中@copilot直接审查。

### 步骤3.3：观察AI发现的问题

**预期AI反馈**（关键片段）：

```
⚠️ BLOCKER级别问题

业务逻辑漏洞：未检查final_price是否为负数

风险场景：
当 discount_coupon + points_value > original_price 时，
final_price 将为负数，用户不仅不用付款，系统还会倒贴钱。

示例：
  original_price = 50
  discount_coupon = 30
  points_value = 30
  final_price = 50 - 30 - 30 = -10  # ❌ 系统倒贴10元

建议修复：
1. 添加负数检查：return max(0, final_price)
2. 或在应用优惠前校验：discount + points <= price
3. 添加边界测试用例
```

### 步骤3.5：对比两种质量门

| 检查项         | 传统质量门        | AI质量门                |
| -------------- | ----------------- | ----------------------- |
| 语法检查  4：对比两种质量门

| 检查项         | 传统质量门        | AI质量门                |
| -------------- | ----------------- | ----------------------- |
| 语法检查       | ✅ 通过           | ✅ 通过                 |
| 代码规范       | ✅ 通过(10.0分)   | ✅ 通过                 |
| 单元测试       | ✅ 通过(100%覆盖) | ❌ 发现测试缺失边界场景 |
| 业务逻辑       | ⚠️ 无法检测     | ❌ 发现负价格漏洞       |
| **结果** | ✅ 通过（误判）   | ❌ 拦截（正确）         |

### ✅ 阶段3检查点

- [ ] 已在GitHub上查看代码
- [ ] 已使用AI审查代码
💡 **核心洞察**：传统工具检查代码"格式"，AI理解代码"逻辑"

---

## 🔧 阶段4：AI辅助修复（15分钟）

### 步骤4.1：使用AI生成修复代码

📋 **使用提示词**：[prompts/05-AI修复代码.md](../prompts/05-AI修复代码.md)

**操作步骤**：

1. 复制提示词，附上原代码和AI的审查反馈
2. 将生成的修复代码更新到 `src/price_calculator.py`

**预期修复**（关键部分）：

```python
def calculate_final_price(self, original_price, discount_coupon, points_value):
    """计算最终价格（已修复负价格漏洞）"""
    # 参数校验
    if original_price < 0 or discount_coupon < 0 or points_value < 0:
        raise ValueError("价格和优惠金额不能为负数")
  
    # 计算价格
    final_price = original_price - discount_coupon - points_value
  
    # 防止负价格
    if final_price < 0:
        logger.warning(f"优惠超价：调整为0")
        final_price = 0
  
    return final_price
```

### 步骤4.2：使用AI生成边界测试用例

📋 **使用提示词**：[prompts/06-AI生成边界测试.md](../prompts/06-AI生成边界测试.md)

**操作步骤**：

1. 复制提示词，提供修复后的代码
2. 将生成的测试用例追加到 `tests/test_price_calculator.py`

**预期生成**（关键测试）：

```python
def test_discount_exceeds_price(self):
    """测试优惠超过商品价格"""
    result = self.calculator.calculate_final_price(50, 30, 30)
    self.assertEqual(result, 0)  # ✅ 应该返回0而不是-10

def test_negative_price_input(self):
    """测试负数原价"""
    with self.assertRaises(ValueError):
        self.calculator.calculate_final_price(-100, 10, 20)
```

### 步骤4.3：本地验证修复效果

```bash
# 运行测试（新增的边界测试应该通过）
pytest tests/ -v

# 检查覆盖率
pytest tests/ --cov=src --cov-report=term-missing
```

**预期输出**：

```
tests/test_price_calculator.py::test_normal_calculation PASSED
tests/test_price_calculator.py::test_discount_exceeds_price PASSED  # 新增
tests/test_price_calculator.py::test_negative_price_input PASSED    # 新增

---------- coverage: 100% -----------
```

### ✅ 阶段4检查点

- [ ] 代码已修复（防止负价格）
- [ ] 测试用例已补充（边界场景）
- [ ] 本地运行pytest全部通过
- [ ] 覆盖率保持100%

💡 **关键收获**：AI不仅发现问题，还能帮你修复并生成测试

---

## 🚀 阶段5：集成AI流水线（10分钟）

### 步骤5.1：使用AI生成AI赋能的流水线配置
总结与展望（5分钟）

> **💡 说明**：本阶段总结AI在CI/CD中的价值，实际集成AI流水线需要企业级API支持，超出本次演练范围。

### 步骤5.1：回顾完整流程

**我们完成了什么**：

1. ✅ **阶段1**：生成了有漏洞的代码和100%覆盖率的测试
2. ✅ **阶段2**：搭建了传统质量门（Pylint + Pytest + Coverage）
3. ✅ **阶段3**：用AI发现了传统工具无法检测的业务逻辑漏洞
4. ✅ **阶段4**：用AI辅助修复代码并生成边界测试

**核心发现**：
```
传统质量门：✅ Pylint 10.0/10 + ✅ 测试覆盖率100% = ❌ 仍有致命漏洞
AI质量门：  🤖 理解业务逻辑 + 🔍 发现负价格风险 = ✅ 正确拦截
```

### 步骤5.2：理解AI集成的现实场景

**企业级AI集成方案**（参考）：

```yaml
# .github/workflows/ai-quality-gate.yml（概念示例）
name: AI-Enhanced Quality Gate

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # 调用企业AI服务（需要API Key和付费订阅）
      - name: AI代码审查
        uses: enterprise/ai-code-review@v1
        with:
          api_key: ${{ secrets.AI_API_KEY }}
          severity_threshold: 'BLOCKER'
          
      # 如果发现阻断性问题，终止部署
      - name: 检查AI审查结果
        run: |
          if [ -f ".ai-review/blocker-found" ]; then
            echo "❌ AI发现阻断性问题，终止部署"
            exit 1
          fi
```

**实施建议**：

| 场景 | 方案 | 成本 |
|------|------|------|
| 个人项目 | 手动使用Claude/ChatGPT审查核心代码 | 免费/低成本 |
| 小团队 | Pre-commit Hook + AI CLI工具 | 低成本 |
| 中型团队 | GitHub Copilot + 代码评审规范 | 中成本 |
| 大型企业 | 自建AI平台 + CI/CD深度集成 | 高成本 |

### ✅ 阶段5检查点

- [ ] 已完成完整的演练流程
- [ ] 已理解AI在质量门中的价值
- [ ] 已了解企业级AI集成的方向
- [ ] 已掌握如何在实际项目中应用AI辅助

💡 **关键启发**：AI不是替代传统工具，而是作为"第二双眼睛"补足人的经验不足
## 📊 阶段6：总结讨论（5分钟）

### 核心对比

| 维度                 | 传统质量门 | AI赋能质量门   |
| -------------------- | ---------- | -------------- |
| **检查方式**   | 规则匹配   | 语义理解       |
| **覆盖范围**   | 语法+规范  | 语法+规范+逻辑 |
| **业务理解**   | ❌ 无      | ✅ 有          |
| **测试完整性** | 依赖人工   | AI辅助识别     |
| **边界场景**   | 易遗漏     | AI主动发现     |

### 关键收获

1. **传统质量门的价值**：
讨论与思考
   - ✅ 自动化基础检查
   - ✅ 快速反馈语法问题
   - ⚠️ 但无法理解业务逻辑
2. **AI赋能的价值**：

   - ✅ 补足人的经验不足
   - ✅ 发现深层逻辑问题
   - ✅ 辅助生成测试用例
   - ⚠️ 但也可能误报，需人工判断
3. **最佳实践**：

   - AI + 传统工具组合使用
   - AI作为"第二双眼睛"
   - 关键决策仍需人工确认

### 讨论问题

1. **Q：AI能完全替代Code Review吗？**

   - A：不能。AI发现问题，人类做最终决策
2. **Q：如果我经验丰富，会写边界测试，还需要AI吗？**

   - A：需要。即使资深工程师也会：
     - 时间紧张时遗漏测试
     - 评审疲劳时漏看问题
     - AI提供"永不疲劳的第二双眼睛"
3. **Q：AI会不会误报？**

   - A：会。处理方式：
     - 标注反馈（这是误报）
     - 模型持续学习优化
     - 关键是：宁可误报，不可漏报

---

## 📦 课后作业

### 必做任务

1. [ ] 在自己的项目中实施传统质量门
2. [ ] 选择1个核心模块，使用AI进行代码审查
3. [ ] 记录AI发现的问题（是否是真问题？）

### 选做任务

1. [ ] 将AI审查集成到你的CI/CD流水线
2. [ ] 对比1周内AI发现的问题 vs 人工Code Review发现的问题
3. [ ] 设计你的团队的AI质量门方案

---

## 🔗 参考资源

### 提示词清单

- [01-生成缺陷代码](../prompts/01-生成缺陷代码.md)
- [02-生成单元测试](../prompts/02-生成单元测试.md)
- [03-生成GitHub-Actions配置](../prompts/03-生成GitHub-Actions配置.md)
- [04-AI代码审查](../prompts/04-AI代码审查.md)
- [05-AI修复代码](../prompts/05-AI修复代码.md)
- [06-AI生成边界测试](../prompts/06-AI生成边界测试.md)
- [07-生成AI赋能流水线](../prompts/07-生成AI赋能流水线.md)

### 延伸阅读

- [GitHub Copilot官方文档](https://docs.github.com/en/copilot)
- [AI辅助测试最佳实践](https://example.com)
- [CI/CD质量门设计指南](https://example.com)

---

## ❓ 常见问题

### 环境问题

**Q：GitHub Actions没有执行**

- 检查仓库是否为Public（私有仓库Actions需付费）
- 检查 `.github/workflows/` 路径是否正确
- 检查YAML语法是否正确（可用在线工具验证）

**Q：pytest找不到模块**

- 确保 `src/__init__.py` 和 `tests/__init__.py` 已创建
- 在项目根目录运行pytest
- 检查Python路径：`export PYTHONPATH=$PYTHONPATH:$(pwd)`

### AI使用问题

**Q：没有GitHub Copilot订阅怎么办？**

- 使用Claude/ChatGPT/通义千问等免费AI
- 手动复制代码到AI进行审查
- 效果相同，只是需要手动操作

**Q：AI反馈的建议不对怎么办？**

- 这是正常的，AI也会出错
- 人工判断AI的建议是否合理
- 这就是为什么强调"AI辅助，人类决策"

**Q：如何提高AI审查的准确率？**

- 提供更详细的上下文（业务场景、技术栈）
- 明确告诉AI关注点（性能、安全、边界场景）
- 反馈误报，帮助AI学习

---

**演练结束，祝学习愉快！🎉**
