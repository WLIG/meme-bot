import asyncio
import os
import json
import threading
import logging
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from market_data_collector import MarketDataCollector
from on_chain_data_collector import OnChainDataCollector
from social_media_data_collector import SocialMediaDataCollector
from data_processor import DataProcessor
from ai_signal_generator import AISignalGenerator
from on_chain_scanner import OnChainScanner
from twitter_monitor import TwitterMonitor
from chatgpt_decision_support import ChatGPTDecisionSupport
from strategy_executor import StrategyExecutor
from risk_manager import RiskManager
from telegram_notifier import TelegramNotifier
from monitoring_logging import MonitoringLogging

# Initialize database
db = SQLAlchemy()

class MemeCoinTradingBot:
    def __init__(self):
        # 使用安全配置管理器
        try:
            from secure_config import SecureConfigManager, config_manager
            self.config_manager = config_manager
            if not self.config_manager:
                raise ValueError("安全配置管理器初始化失败")
            
            # 获取API配置
            self.api_config = self.config_manager.get_api_config()
            
            # 验证API密钥
            validation_results = self.config_manager.validate_api_keys()
            invalid_keys = [k for k, v in validation_results.items() if not v]
            if invalid_keys:
                logging.warning(f"以下API密钥格式无效: {invalid_keys}")
                
            # 从安全配置获取API密钥
            self.binance_api_key = self.api_config.get('binance', {}).get('api_key')
            self.binance_secret_key = self.api_config.get('binance', {}).get('secret_key')
            self.infura_project_id = self.api_config.get('infura', {}).get('project_id')
            self.twitter_consumer_key = self.api_config.get('twitter', {}).get('consumer_key')
            self.twitter_consumer_secret = self.api_config.get('twitter', {}).get('consumer_secret')
            self.twitter_access_token = self.api_config.get('twitter', {}).get('access_token')
            self.twitter_access_token_secret = self.api_config.get('twitter', {}).get('access_token_secret')
            self.openai_api_key = self.api_config.get('openai', {}).get('api_key')
            self.telegram_bot_token = self.api_config.get('telegram', {}).get('bot_token')
            self.telegram_chat_id = self.api_config.get('telegram', {}).get('chat_id')
        except ImportError:
            # 回退到环境变量
            logging.warning("安全配置模块不可用，使用环境变量")
            self.binance_api_key = os.getenv("BINANCE_API_KEY", "YOUR_BINANCE_API_KEY")
            self.binance_secret_key = os.getenv("BINANCE_SECRET_KEY", "YOUR_BINANCE_SECRET_KEY")
            self.infura_project_id = os.getenv("INFURA_PROJECT_ID", "YOUR_INFURA_PROJECT_ID")
            self.twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY", "YOUR_TWITTER_CONSUMER_KEY")
            self.twitter_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET", "YOUR_TWITTER_CONSUMER_SECRET")
            self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN", "YOUR_TWITTER_ACCESS_TOKEN")
            self.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "YOUR_TWITTER_ACCESS_TOKEN_SECRET")
            self.openai_api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
            self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
            self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")

        # Initialize modules
        self.market_data_collector = MarketDataCollector(exchange_api_keys={
            "binance": {"api_key": self.binance_api_key, "secret_key": self.binance_secret_key}
        })
        self.on_chain_data_collector = OnChainDataCollector(rpc_url=f"https://mainnet.infura.io/v3/{self.infura_project_id}")
        self.social_media_data_collector = SocialMediaDataCollector(
            self.twitter_consumer_key, self.twitter_consumer_secret, self.twitter_access_token, self.twitter_access_token_secret
        )
        self.data_processor = DataProcessor()
        self.ai_signal_generator = AISignalGenerator()
        self.on_chain_scanner = OnChainScanner(rpc_url=f"https://mainnet.infura.io/v3/{self.infura_project_id}")
        self.twitter_monitor = TwitterMonitor(
            self.twitter_consumer_key, self.twitter_consumer_secret, self.twitter_access_token, self.twitter_access_token_secret
        )
        self.chatgpt_decision_support = ChatGPTDecisionSupport(api_key=self.openai_api_key)
        self.strategy_executor = StrategyExecutor("binance", self.binance_api_key, self.binance_secret_key)
        self.risk_manager = RiskManager()
        self.telegram_notifier = TelegramNotifier(self.telegram_bot_token, self.telegram_chat_id)
        self.logger = MonitoringLogging()

        self.logger.log_info("MemeCoinTradingBot initialized.")

    async def run_once(self, symbol="DOGEUSDT", twitter_query="#DOGE OR #DOGECOIN"):
        self.logger.log_info(f"Running bot cycle for {symbol}...")

        # 1. Data Acquisition
        market_data = await self.market_data_collector.collect_market_data("binance", symbol)
        on_chain_data = await self.on_chain_data_collector.collect_on_chain_data()
        social_media_tweets = self.social_media_data_collector.search_tweets(twitter_query, count=50)

        # 2. Data Processing
        processed_market_data = self.data_processor.process_market_data(market_data["klines"], market_data["order_book"])
        processed_on_chain_data = self.data_processor.process_on_chain_data(on_chain_data)
        processed_social_media_data = self.data_processor.process_social_media_data(social_media_tweets)

        # 3. AI Signal Generation
        # For demonstration, we need to train the model first if not already trained
        # In a real scenario, model training would be a separate, scheduled process
        # self.ai_signal_generator.train_model(self.ai_signal_generator.load_data(processed_market_data, processed_on_chain_data, processed_social_media_data))
        ai_signal = self.ai_signal_generator.generate_signal(processed_market_data, processed_on_chain_data, processed_social_media_data)
        self.logger.log_info(f"AI Signal: {ai_signal}")

        # 4. On-chain Scanning (example usage)
        latest_block_number = await self.on_chain_scanner.get_latest_block_number()
        new_tokens = await self.on_chain_scanner.detect_new_token_deployments(latest_block_number)
        whale_activities = await self.on_chain_scanner.track_whale_addresses(latest_block_number, ["0xYourWhaleAddress1"])
        self.logger.log_info(f"New Tokens Detected: {len(new_tokens)}")
        self.logger.log_info(f"Whale Activities: {len(whale_activities)}")

        # 5. Twitter Monitoring (example usage)
        twitter_monitoring_results = await self.twitter_monitor.monitor_tweets_for_meme_coin(twitter_query, count=20)
        self.logger.log_info(f'Twitter Sentiment: {twitter_monitoring_results.get("analyzed_tweets", [])[0].get("sentiment") if twitter_monitoring_results.get("analyzed_tweets") else "N/A"}')
        trading_advice = await self.chatgpt_decision_support.generate_trading_advice(
            processed_market_data, processed_on_chain_data, twitter_monitoring_results, ai_signal
        )
        self.logger.log_info(f"ChatGPT Trading Advice: {trading_advice}")

        trading_instruction = await self.chatgpt_decision_support.generate_trading_instruction(trading_advice)
        self.logger.log_info(f"ChatGPT Trading Instruction: {json.dumps(trading_instruction)}")

        # 7. Strategy Execution and Risk Management
        if trading_instruction and trading_instruction.get("action") in ["BUY", "SELL"]:
            # Example: calculate position size based on risk manager (simplified)
            # This would need actual current price and stop loss from the instruction or market data
            # For demonstration, we'll use a fixed amount
            amount_to_trade = trading_instruction.get("amount", 0.001) # Default small amount
            trade_result = await self.strategy_executor.execute_trade(trading_instruction)
            self.logger.log_info(f"Trade Result: {trade_result}")
            
            # Update risk manager positions (simplified)
            if trade_result and trade_result["status"] == "EXECUTED":
                # This part needs real price and amount from the executed order
                # For now, just a placeholder
                # self.risk_manager.update_position(symbol, amount_to_trade, current_price, is_buy=(trading_instruction["action"] == "BUY"))
                pass
        else:
            self.logger.log_info("No trade executed based on instruction.")

        # 8. Notifications
        await self.telegram_notifier.send_message(f"Bot cycle completed for {symbol}. AI Signal: {ai_signal}. Trading Instruction: {trading_instruction.get('action')}")

        self.logger.log_info(f"Bot cycle for {symbol} finished.")

    async def run_continuously(self, interval_seconds=300, symbol="DOGEUSDT", twitter_query="#DOGE OR #DOGECOIN"):
        while True:
            await self.run_once(symbol, twitter_query)
            self.logger.log_info(f"Waiting for {interval_seconds} seconds before next cycle...")
            await asyncio.sleep(interval_seconds)

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # 安全配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or os.urandom(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///trading_bot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # 安全头配置
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # 创建必要的目录
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # 初始化扩展
    db.init_app(app)
    
    # CORS配置 - 限制来源
    allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    CORS(app, origins=allowed_origins, supports_credentials=True)
    
    # 初始化安全中间件
    try:
        from session_manager import SecurityMiddleware
        SecurityMiddleware(app)
    except ImportError:
        logging.warning("安全中间件模块不可用")
    
    # 初始化限流器
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # 注册API路由
    try:
        from api_routes import create_api_routes
        app = create_api_routes(app)
        logging.info("API routes registered successfully")
    except ImportError as e:
        logging.warning(f"Failed to import API routes: {e}")
    
    # 前端路由
    from flask import render_template, send_from_directory
    
    @app.route('/')
    def index():
        """主页面"""
        return render_template('index.html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        """静态文件服务"""
        return send_from_directory('static', filename)
    
    # 健康检查端点
    @app.route('/health')
    def health_check():
        """健康检查"""
        return {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    
    # SPA路由处理
    @app.errorhandler(404)
    def not_found_error(error):
        # 对于前端路由，返回index.html
        if not str(error).startswith('/api/'):
            return render_template('index.html'), 200
        return {'error': 'API endpoint not found'}, 404
    
    return app

async def main():
    bot = MemeCoinTradingBot()
    # To run once:
    # await bot.run_once()

    # To run continuously:
    await bot.run_continuously(interval_seconds=300) # Run every 5 minutes

if __name__ == "__main__":
    # 配置日志
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/trading_bot.log'),
            logging.StreamHandler()
        ]
    )
    
    # 检查是否运行Web应用
    if os.getenv('RUN_WEB_APP') == 'true':
        app = create_app()
        
        # 创建数据库表
        with app.app_context():
            db.create_all()
            
            # 创建默认管理员用户（如果不存在）
            try:
                from user import User
                admin_user = User.query.filter_by(username='admin').first()
                if not admin_user:
                    admin_user = User(
                        username='admin',
                        email='admin@tradingbot.com',
                        role='admin'
                    )
                    admin_user.set_password(os.getenv('ADMIN_PASSWORD', 'TradingBot@2024!'))
                    db.session.add(admin_user)
                    db.session.commit()
                    logging.info("默认管理员用户已创建")
            except ImportError:
                logging.warning("用户模块不可用，跳过管理员用户创建")
        
        # 启动应用
        debug_mode = os.getenv('FLASK_ENV') == 'development'
        app.run(
            host='0.0.0.0',
            port=int(os.getenv('PORT', 5000)),
            debug=debug_mode,
            ssl_context='adhoc' if os.getenv('USE_SSL') == 'true' else None
        )
    else:
        # 运行交易机器人
        asyncio.run(main())


