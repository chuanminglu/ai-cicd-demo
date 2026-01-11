"""
电商价格计算模块

提供价格计算相关功能，包括优惠券和积分抵扣。
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
        x = 1  # 添加未使用的变量（会被Pylint检测）
        y = 2  # 添加未使用的变量
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
