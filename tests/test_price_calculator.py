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
