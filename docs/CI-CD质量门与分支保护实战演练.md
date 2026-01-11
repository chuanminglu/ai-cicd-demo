# CI/CD质量门与分支保护实战演练

> **演练时长**：45分钟  
> **案例场景**：通过PR工作流体验质量门真正的拦截能力  
> **核心目标**：理解"Push成功 ≠ 合并成功"，掌握分支保护的正确使用

---

## 📋 演练概述

### 学习目标

- ✅ 理解Git Push和PR合并的区别
- ✅ 掌握Feature分支开发工作流
- ✅ 配置GitHub分支保护规则
- ✅ 体验质量门真正拦截问题代码
- ✅ 学会修复问题并通过质量门

### 核心概念

**常见误解**：
```
❌ 错误理解：git push失败 = 质量门拦截
❌ 实际情况：git push总是成功的
```

**正确理解**：
```
✅ git push → 代码进入feature分支（总是成功）
✅ 创建PR → 触发质量门检查
✅ 质量门失败 → 无法合并到main（真正的拦截）
```

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
mkdir cicd-branch-demo
cd cicd-branch-demo

# 初始化Git
git init
git branch -M main

# 创建目录结构
mkdir src tests .github/workflows
```

### ✅ 阶段0检查点

- [ ] Git、Python已安装
- [ ] 项目目录已创建
- [ ] GitHub账号可访问

---

## 🎯 阶段1：搭建基础代码和质量门（10分钟）

### 步骤1.1：创建价格计算代码

创建 `src/price_calculator.py`：

```python
"""
电商价格计算模块
"""


class PriceCalculator:
    """电商价格计算器类"""

    def __init__(self):
        """初始化价格计算器"""
        self.points_rate = 100  # 100积分抵扣1元

    def calculate_final_price(self, original_price, discount_coupon, points_value):
        """
        计算最终支付价格

        Args:
            original_price (float): 商品原价
            discount_coupon (float): 优惠券金额
            points_value (float): 积分抵扣金额

        Returns:
            float: 最终支付价格
        """
        final_price = original_price - discount_coupon - points_value
        return final_price

    def calculate_points_needed(self, price):
        """
        计算所需积分数量

        Args:
            price (float): 需要抵扣的金额

        Returns:
            int: 所需积分数量
        """
        points_needed = int(price * self.points_rate)
        return points_needed
```

### 步骤1.2：创建单元测试

创建 `tests/test_price_calculator.py`：

```python
"""
电商价格计算模块的单元测试
"""
import pytest
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from price_calculator import PriceCalculator


class TestPriceCalculator:
    """价格计算器测试类"""

    def setup_method(self):
        """每个测试方法执行前的设置"""
        self.calculator = PriceCalculator()

    def test_normal_calculation(self):
        """测试正常价格计算"""
        original_price = 100.0
        discount_coupon = 10.0
        points_value = 5.0
        
        result = self.calculator.calculate_final_price(
            original_price, 
            discount_coupon, 
            points_value
        )
        
        assert result == 85.0

    def test_no_discount(self):
        """测试无优惠情况"""
        original_price = 100.0
        discount_coupon = 0.0
        points_value = 0.0
        
        result = self.calculator.calculate_final_price(
            original_price,
            discount_coupon,
            points_value
        )
        
        assert result == 100.0

    def test_points_calculation(self):
        """测试积分计算"""
        price = 50.0
        
        result = self.calculator.calculate_points_needed(price)
        
        assert result == 5000
        assert isinstance(result, int)
```

### 步骤1.3：创建包标识文件

```bash
# Windows PowerShell
New-Item src/__init__.py
New-Item tests/__init__.py

# Linux/Mac
touch src/__init__.py
touch tests/__init__.py
```

### 步骤1.4：创建GitHub Actions配置

创建 `.github/workflows/quality-gate.yml`：

```yaml
name: Quality Gate

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout代码
      uses: actions/checkout@v3
      
    - name: 设置Python 3.9
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov pylint
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        
    - name: Pylint代码质量检查
      run: |
        echo "🔍 执行Pylint代码质量检查..."
        pylint src/ --fail-under=8.0 --output-format=text || exit 1
        echo "✅ Pylint检查通过 (评分 >= 8.0)"
        
    - name: Pytest单元测试与覆盖率
      run: |
        echo "🧪 执行单元测试并检查覆盖率..."
        pytest tests/ --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80 -v
        echo "✅ 测试通过，覆盖率 >= 80%"
        
    - name: 输出质量门总结
      if: always()
      run: |
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📊 质量门检查总结"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        if [ ${{ job.status }} == 'success' ]; then
          echo "✅ 所有质量门检查通过！"
          echo "   ✓ Pylint代码质量 >= 8.0"
          echo "   ✓ 测试覆盖率 >= 80%"
          echo "   ✓ 所有单元测试通过"
        else
          echo "❌ 质量门检查失败"
          echo "请修复上述问题后重新提交"
        fi
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
    - name: 上传HTML覆盖率报告
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: coverage-report
        path: htmlcov/
```

### 步骤1.5：创建依赖文件

创建 `requirements.txt`：

```
pytest==7.4.0
pytest-cov==4.1.0
pylint==2.17.4
```

### 步骤1.6：本地验证

```bash
# 安装依赖
pip install -r requirements.txt

# Pylint检查
python -m pylint src/ --fail-under=8.0

# 运行测试
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80 -v
```

**预期结果**：
```
✅ Pylint: 10.00/10
✅ Tests: 3 passed
✅ Coverage: 100%
```

### 步骤1.7：创建GitHub仓库并推送初始代码

```bash
# 提交初始代码
git add .
git commit -m "feat: initial setup with quality gate"

# 创建GitHub仓库
# 访问 https://github.com/new
# 仓库名：cicd-branch-demo
# 类型：Public

# 关联远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/cicd-branch-demo.git

# 推送到main
git push -u origin main
```

### ✅ 阶段1检查点

- [ ] 代码文件已创建
- [ ] 测试用例已创建
- [ ] GitHub Actions配置已创建
- [ ] 本地质量门检查通过
- [ ] 代码已推送到GitHub
- [ ] GitHub Actions执行成功（在Actions标签页查看）

---

## 🚫 阶段2：体验"Push成功但有问题"的场景（10分钟）

> **💡 核心概念**：本阶段演示直接push到main的问题——即使质量门失败，代码也已经在仓库里了

### 步骤2.1：制造问题代码

在 `src/price_calculator.py` 的 `calculate_final_price` 方法中添加未使用的变量：

```python
def calculate_final_price(self, original_price, discount_coupon, points_value):
    """
    计算最终支付价格

    Args:
        original_price (float): 商品原价
        discount_coupon (float): 优惠券金额
        points_value (float): 积分抵扣金额

    Returns:
        float: 最终支付价格
    """
    final_price = original_price - discount_coupon - points_value
    x = 1  # ❌ 未使用的变量（会导致Pylint失败）
    y = 2  # ❌ 未使用的变量
    return final_price
```

### 步骤2.2：本地验证问题

```bash
# 验证Pylint会失败
python -m pylint src/ --fail-under=8.0
```

**预期输出**：
```
************* Module price_calculator
src/price_calculator.py:23:8: W0612: Unused variable 'x' (unused-variable)
src/price_calculator.py:24:8: W0612: Unused variable 'y' (unused-variable)

Your code has been rated at 7.50/10  ❌ (阈值: 8.0)
```

### 步骤2.3：直接推送到main（演示问题）

```bash
git add .
git commit -m "test: add unused variables to demo quality gate"
git push origin main
```

**观察结果**：
```
✅ Git push成功（代码已推送）
```

### 步骤2.4：查看GitHub Actions结果

访问仓库的 **Actions** 标签页，观察最新的workflow运行：

**预期看到**：
```
❌ quality-check — Failed

Details:
  ✅ Checkout代码
  ✅ 设置Python 3.9
  ✅ 安装依赖
  ❌ Pylint代码质量检查 ← 失败在这里
     Your code has been rated at 7.50/10
```

### 步骤2.5：关键观察

**此时的状态**：
```
✅ 代码在main分支上（可以在GitHub看到）
❌ 但Actions失败了
⚠️ 问题代码已经进入main分支！
```

**核心问题**：
- Push和质量门检查是**分离**的
- Push成功后，Actions才异步执行
- Actions失败**无法撤销**已推送的代码

### ✅ 阶段2检查点

- [ ] 已制造问题代码（未使用的变量）
- [ ] 本地验证Pylint失败
- [ ] 代码已成功推送到main
- [ ] GitHub Actions显示失败
- [ ] 理解了"Push成功 ≠ 质量门拦截"

💡 **核心认知**：直接推送到main无法真正阻止问题代码！

---

## ✅ 阶段3：配置分支保护 + PR工作流（15分钟）

> **💡 目标**：通过分支保护和PR工作流，让质量门真正起作用

### 步骤3.1：先恢复main分支的代码

```bash
# 回退到没有问题的版本
git revert HEAD
git push origin main
```

或者直接修复：

```bash
# 删除未使用的变量
# 编辑 src/price_calculator.py，删除 x = 1 和 y = 2 两行

git add .
git commit -m "fix: remove unused variables"
git push origin main
```

### 步骤3.2：配置GitHub分支保护规则

**操作步骤**：

1. 访问仓库页面
2. 点击 **Settings** → **Branches**
3. 点击 **Add branch protection rule**
4. 配置以下规则：

```
Branch name pattern: main

☑️ Require a pull request before merging
   ☑️ Require approvals: 0 (演练可设为0)

☑️ Require status checks to pass before merging
   ☑️ Require branches to be up to date before merging
   Status checks that are required:
     ☑️ quality-check (选择你的GitHub Actions job名称)

☑️ Do not allow bypassing the above settings

☑️ Include administrators (建议勾选，否则管理员可以绕过)
```

5. 点击 **Create** 保存

### 步骤3.3：验证分支保护生效

尝试直接推送到main：

```bash
# 尝试直接修改并推送
echo "# Test" >> README.md
git add .
git commit -m "test: try direct push"
git push origin main
```

**预期结果**：
```
remote: error: GH006: Protected branch update failed
❌ 推送被拒绝！
```

✅ **成功**：分支保护已生效，无法直接推送到main！

### 步骤3.4：使用正确的PR工作流

#### 第1步：创建feature分支

```bash
# 创建并切换到feature分支
git checkout -b feature/test-quality-gate

# 如果上一步push失败，需要先撤销本地commit
git reset HEAD~1
```

#### 第2步：制造问题代码

在 `src/price_calculator.py` 中再次添加未使用的变量：

```python
def calculate_final_price(self, original_price, discount_coupon, points_value):
    """计算最终支付价格"""
    final_price = original_price - discount_coupon - points_value
    unused_var = 1  # ❌ 未使用的变量
    return final_price
```

#### 第3步：提交并推送到feature分支

```bash
git add .
git commit -m "test: add unused variable to trigger quality gate"
git push origin feature/test-quality-gate
```

**观察**：
```
✅ Push成功！（代码在feature分支，不影响main）
```

#### 第4步：创建Pull Request

1. 访问GitHub仓库页面
2. 会看到提示："Compare & pull request"，点击它
3. 或者点击 **Pull requests** → **New pull request**
4. 选择：`base: main` ← `compare: feature/test-quality-gate`
5. 标题：`test: 测试质量门拦截功能`
6. 点击 **Create pull request**

#### 第5步：观察质量门检查

在PR页面会看到：

```
┌─────────────────────────────────────────────┐
│  Some checks haven't completed yet          │
│  ⏳ quality-check — In progress             │
└─────────────────────────────────────────────┘

几秒后变为：

┌─────────────────────────────────────────────┐
│  All checks have failed                     │
│  ❌ quality-check — Failed                  │
│     Pylint evaluation failed (7.5/10)       │
│                                             │
│  🚫 Merge pull request (按钮禁用)           │
│     Merging is blocked                      │
│     Required status check "quality-check"   │
│     has failed                              │
└─────────────────────────────────────────────┘
```

**关键观察**：
- ✅ PR创建成功
- ❌ 质量门检查失败
- 🚫 **无法点击合并按钮**（被分支保护拦截）
- 💡 这才是真正的质量门拦截！

### 步骤3.5：修复代码并观察通过

#### 在本地修复：

```bash
# 切回feature分支（如果不在的话）
git checkout feature/test-quality-gate

# 删除未使用的变量
# 编辑 src/price_calculator.py，删除 unused_var = 1

# 提交修复
git add .
git commit -m "fix: remove unused variable"
git push origin feature/test-quality-gate
```

#### 观察PR页面自动更新：

```
┌─────────────────────────────────────────────┐
│  Some checks are pending                    │
│  ⏳ quality-check — In progress             │
└─────────────────────────────────────────────┘

几秒后变为：

┌─────────────────────────────────────────────┐
│  All checks have passed                     │
│  ✅ quality-check — Success                 │
│                                             │
│  [Merge pull request] ← 按钮现在可以点击了   │
└─────────────────────────────────────────────┘
```

### 步骤3.6：合并PR

1. 点击绿色的 **Merge pull request** 按钮
2. 选择合并方式（推荐：Squash and merge）
3. 点击 **Confirm merge**
4. 删除feature分支（可选）

**成功**：
```
✅ Pull request successfully merged and closed
✅ 代码已合并到main分支
✅ main分支代码质量有保障
```

### ✅ 阶段3检查点

- [ ] 已配置main分支保护规则
- [ ] 无法直接推送到main
- [ ] 使用feature分支开发
- [ ] 创建PR触发质量门
- [ ] 质量门失败时无法合并
- [ ] 修复后成功合并

💡 **核心收获**：分支保护 + PR工作流 = 质量门真正起作用！

---

## 📊 阶段4：总结与对比（5分钟）

### 两种工作方式对比

| 工作方式 | 直接Push到main | PR工作流 + 分支保护 |
|---------|---------------|-------------------|
| **代码审查** | ❌ 无 | ✅ PR评审 |
| **质量门触发** | ✅ 触发 | ✅ 触发 |
| **质量门失败** | ⚠️ 代码已在main | 🚫 无法合并 |
| **问题代码** | ❌ 已进入main | ✅ 被拦截在feature分支 |
| **适用场景** | ❌ 不推荐 | ✅ 企业标准实践 |

### 流程对比图

**直接Push到main（不推荐）**：
```
开发代码 → git push origin main
              ↓
         ✅ Push成功
              ↓
         触发Actions
              ↓
         ❌ 质量门失败
              ↓
      ⚠️ 但代码已经在main了！
```

**PR工作流 + 分支保护（推荐）**：
```
开发代码 → git push origin feature/xxx
              ↓
         ✅ Push成功（feature分支）
              ↓
         创建PR → main
              ↓
         触发Actions
              ↓
         ❌ 质量门失败
              ↓
      🚫 无法合并到main（被拦截）
              ↓
         修复代码 → push
              ↓
         ✅ 质量门通过
              ↓
         ✅ 合并到main
```

### 核心概念总结

1. **Git Push ≠ 质量门拦截**
   - Push只是上传代码到仓库
   - 质量门是事后异步执行的检查
   - Actions失败无法撤销已推送的代码

2. **真正的拦截 = 分支保护 + PR工作流**
   - 分支保护：要求PR通过检查才能合并
   - PR工作流：代码先到feature分支，review后合并
   - 质量门失败时，PR无法合并

3. **企业级最佳实践**
   - 永远不要直接推送到main/master
   - 使用feature分支开发
   - 通过PR审查和合并
   - 配置强制的分支保护规则

---

## 🎓 延伸练习

### 练习1：体验更多质量门失败场景

尝试制造其他问题：

```python
# 1. 测试失败
def calculate_final_price(...):
    return final_price + 1  # 返回错误的值

# 2. 覆盖率不足
def new_method_without_test(self):
    """这个方法没有测试覆盖"""
    return True
```

### 练习2：配置更严格的保护规则

在分支保护设置中：
- ✅ 要求至少1个审批人
- ✅ 要求线性历史（no merge commits）
- ✅ 要求签署commits

### 练习3：本地Pre-commit Hook

创建 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
echo "🔍 执行pre-commit质量检查..."
python -m pylint src/ --fail-under=8.0 || exit 1
python -m pytest tests/ --cov=src --cov-fail-under=80 -v || exit 1
echo "✅ 质量检查通过"
```

---

## 📚 参考资源

- [GitHub分支保护文档](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [Git工作流最佳实践](https://docs.github.com/en/get-started/quickstart/github-flow)
- [质量门检查执行指南](./质量门检查执行指南.md)
- [Git提交vs质量门检查-核心概念](./Git提交vs质量门检查-核心概念.md)

---

## ❓ 常见问题

**Q1: 为什么配置了分支保护，还是可以直接push？**

A: 检查是否勾选了"Include administrators"。默认情况下管理员可以绕过规则。

**Q2: PR合并后，feature分支需要删除吗？**

A: 建议删除。可以在PR合并界面勾选"Delete branch"自动删除。

**Q3: 如果是个人项目，需要这么复杂吗？**

A: 建议养成习惯。即使个人项目也应该：
- 使用feature分支开发
- 通过PR合并（可以自己approve）
- 配置基本的质量门检查

**Q4: 质量门检查失败后，可以强制合并吗？**

A: 管理员可以，但不建议。应该修复问题后再合并。

**Q5: 多人协作时，如何避免冲突？**

A: 
- 频繁从main拉取最新代码
- feature分支保持较小的改动
- 及时合并，不要长期不合

---

**演练结束！你已经掌握了企业级的CI/CD工作流程！** 🎉

**关键收获**：
- ✅ 理解了Push和合并的区别
- ✅ 学会了配置分支保护
- ✅ 掌握了PR工作流
- ✅ 知道了如何让质量门真正起作用

---

**文档更新时间**: 2026-01-11
