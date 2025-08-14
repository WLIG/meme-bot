import asyncio
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import json

from trading_config import TradingConfig, TradingSignal, TradingHistory, db

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingBotService:
    """交易机器人核心服务"""
    
    def __init__(self):
        self.is_running = False
        self.bot_thread = None
        self.start_time = None
        self.stats = {
            'total_trades': 0,
            'successful_trades': 0,
            'failed_trades': 0,
            'total_profit': 0.0,
            'today_profit': 0.0
        }
        
    def start_bot(self):
        """启动交易机器人"""
        if self.is_running:
            logger.warning("交易机器人已在运行中")
            return False
            
        self.is_running = True
        self.start_time = datetime.utcnow()
        
        # 在新线程中运行机器人
        self.bot_thread = threading.Thread(target=self._run_bot_loop, daemon=True)
        self.bot_thread.start()
        
        logger.info("交易机器人已启动")
        return True
    
    def stop_bot(self):
        """停止交易机器人"""
        if not self.is_running:
            logger.warning("交易机器人未在运行")
            return False
            
        self.is_running = False
        
        if self.bot_thread and self.bot_thread.is_alive():
            self.bot_thread.join(timeout=5)
            
        logger.info("交易机器人已停止")
        return True
    
    def get_status(self) -> Dict:
        """获取机器人状态"""
        runtime_seconds = 0
        if self.start_time and self.is_running:
            runtime_seconds = int((datetime.utcnow() - self.start_time).total_seconds())
            
        return {
            'running': self.is_running,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'runtime_seconds': runtime_seconds,
            'stats': self.stats.copy()
        }
    
    def _run_bot_loop(self):
        """机器人主循环"""
        logger.info("交易机器人主循环开始")
        
        while self.is_running:
            try:
                # 执行一轮交易逻辑
                self._execute_trading_cycle()
                
                # 等待下一轮（每30秒执行一次）
                time.sleep(30)
                
            except Exception as e:
                logger.error(f"交易循环出错: {e}")
                time.sleep(10)  # 出错后短暂等待
                
        logger.info("交易机器人主循环结束")
    
    def _execute_trading_cycle(self):
        """执行一轮交易循环"""
        try:
            # 1. 获取市场数据
            market_data = self._collect_market_data()
            
            # 2. 生成AI信号
            signals = self._generate_ai_signals(market_data)
            
            # 3. 执行交易决策
            for signal in signals:
                self._execute_trading_signal(signal)
                
            # 4. 更新统计数据
            self._update_statistics()
            
        except Exception as e:
            logger.error(f"交易循环执行出错: {e}")
    
    def _collect_market_data(self) -> Dict:
        """收集市场数据"""
        # 模拟数据收集
        coins = ['DOGE', 'SHIB', 'PEPE', 'FLOKI', 'BONK']
        market_data = {}
        
        for coin in coins:
            market_data[coin] = {
                'price': round(0.00001 + (hash(coin + str(time.time())) % 1000) / 100000000, 8),
                'volume': (hash(coin + str(time.time())) % 1000000) + 500000,
                'change_24h': ((hash(coin + str(time.time())) % 200) - 100) / 10,
                'social_sentiment': (hash(coin + str(time.time())) % 100),
                'whale_activity': (hash(coin + str(time.time())) % 5),
                'technical_score': (hash(coin + str(time.time())) % 100)
            }
            
        return market_data
    
    def _generate_ai_signals(self, market_data: Dict) -> List[Dict]:
        """生成AI交易信号"""
        signals = []
        
        for coin, data in market_data.items():
            # 简单的信号生成逻辑
            confidence = self._calculate_signal_confidence(data)
            
            if confidence > 70:
                signal_type = 'BUY' if data['social_sentiment'] > 60 else 'SELL'
                reason = self._generate_signal_reason(data, signal_type)
                
                signal = {
                    'coin': coin,
                    'signal': signal_type,
                    'confidence': confidence,
                    'reason': reason,
                    'price': data['price'],
                    'timestamp': datetime.utcnow()
                }
                
                signals.append(signal)
                
                # 保存信号到数据库
                self._save_signal_to_db(signal)
        
        return signals
    
    def _calculate_signal_confidence(self, data: Dict) -> int:
        """计算信号置信度"""
        # 综合多个因素计算置信度
        social_weight = 0.3
        technical_weight = 0.4
        whale_weight = 0.3
        
        confidence = (
            data['social_sentiment'] * social_weight +
            data['technical_score'] * technical_weight +
            data['whale_activity'] * 20 * whale_weight
        )
        
        return min(95, max(50, int(confidence)))
    
    def _generate_signal_reason(self, data: Dict, signal_type: str) -> str:
        """生成信号原因"""
        reasons = {
            'BUY': [
                '社交媒体情绪积极',
                '技术指标显示上涨趋势',
                '大户地址增持',
                '交易量显著增加',
                '突破关键阻力位'
            ],
            'SELL': [
                '社交媒体情绪转向消极',
                '技术指标显示下跌趋势',
                '大户地址减持',
                '交易量萎缩',
                '跌破关键支撑位'
            ]
        }
        
        # 根据数据选择最合适的原因
        if data['social_sentiment'] > 70:
            return reasons[signal_type][0]
        elif data['technical_score'] > 70:
            return reasons[signal_type][1]
        elif data['whale_activity'] > 3:
            return reasons[signal_type][2]
        else:
            return reasons[signal_type][3]
    
    def _save_signal_to_db(self, signal: Dict):
        """保存信号到数据库"""
        try:
            from flask import current_app
            with current_app.app_context():
                db_signal = TradingSignal(
                    coin=signal['coin'],
                    signal=signal['signal'],
                    confidence=signal['confidence'],
                    reason=signal['reason'],
                    price=signal['price'],
                    source='AI',
                    timestamp=signal['timestamp']
                )
                db.session.add(db_signal)
                db.session.commit()
        except Exception as e:
            logger.error(f"保存信号到数据库失败: {e}")
    
    def _execute_trading_signal(self, signal: Dict):
        """执行交易信号"""
        try:
            # 模拟交易执行
            if signal['confidence'] > 80:
                # 执行交易
                trade_result = self._simulate_trade_execution(signal)
                
                if trade_result['success']:
                    self.stats['successful_trades'] += 1
                    self.stats['total_profit'] += trade_result['profit']
                    self.stats['today_profit'] += trade_result['profit']
                    
                    # 保存交易记录
                    self._save_trade_to_db(signal, trade_result)
                    
                    logger.info(f"交易执行成功: {signal['coin']} {signal['signal']} 盈利: {trade_result['profit']}")
                else:
                    self.stats['failed_trades'] += 1
                    logger.warning(f"交易执行失败: {signal['coin']} {signal['signal']}")
                    
                self.stats['total_trades'] += 1
                
        except Exception as e:
            logger.error(f"执行交易信号失败: {e}")
    
    def _simulate_trade_execution(self, signal: Dict) -> Dict:
        """模拟交易执行"""
        # 模拟交易结果
        success_rate = 0.7  # 70%成功率
        success = (hash(signal['coin'] + str(time.time())) % 100) < (success_rate * 100)
        
        if success:
            # 模拟盈利
            profit = round((hash(signal['coin'] + str(time.time())) % 50) / 10 + 1, 2)
            if signal['signal'] == 'SELL':
                profit *= -1  # 卖出信号可能是止损
        else:
            # 模拟亏损
            profit = -round((hash(signal['coin'] + str(time.time())) % 20) / 10 + 1, 2)
        
        return {
            'success': success,
            'profit': profit,
            'amount': 1000,  # 固定交易金额
            'executed_price': signal['price']
        }
    
    def _save_trade_to_db(self, signal: Dict, trade_result: Dict):
        """保存交易记录到数据库"""
        try:
            from flask import current_app
            with current_app.app_context():
                trade = TradingHistory(
                    user_id=1,  # 默认用户
                    symbol=f"{signal['coin']}/USDT",
                    side=signal['signal'],
                    amount=trade_result['amount'],
                    price=trade_result['executed_price'],
                    total_value=trade_result['amount'] * trade_result['executed_price'],
                    profit_loss=trade_result['profit'],
                    profit_loss_percentage=(trade_result['profit'] / (trade_result['amount'] * trade_result['executed_price']) * 100),
                    status='COMPLETED',
                    order_id=f"ORDER_{int(time.time())}",
                    timestamp=datetime.utcnow()
                )
                db.session.add(trade)
                db.session.commit()
        except Exception as e:
            logger.error(f"保存交易记录失败: {e}")
    
    def _update_statistics(self):
        """更新统计数据"""
        try:
            # 重置今日盈亏（如果是新的一天）
            now = datetime.utcnow()
            if hasattr(self, '_last_update_date'):
                if self._last_update_date.date() != now.date():
                    self.stats['today_profit'] = 0.0
            
            self._last_update_date = now
            
        except Exception as e:
            logger.error(f"更新统计数据失败: {e}")

# 全局交易机器人实例
trading_bot = TradingBotService()

