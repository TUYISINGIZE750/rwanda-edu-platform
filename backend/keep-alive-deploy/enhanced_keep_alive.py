"""
Enhanced Keep-Alive Service for Rwanda Education Platform
Prevents Render free tier from sleeping with multiple strategies
"""
import requests
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
import logging
import os
from typing import List, Dict
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedKeepAlive:
    def __init__(self):
        self.base_url = "https://rwanda-edu-platform.onrender.com"
        self.ping_interval = 480  # 8 minutes (less than 15min Render timeout)
        self.endpoints = [
            "/health",
            "/api/v1/locations/provinces", 
            "/api/v1/auth/test",
        ]
        self.stats = {
            "total_pings": 0,
            "successful_pings": 0,
            "failed_pings": 0,
            "last_success": None,
            "last_failure": None,
            "uptime_start": datetime.now()
        }
    
    async def ping_endpoint(self, session: aiohttp.ClientSession, endpoint: str) -> Dict:
        """Ping a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                success = response.status == 200
                return {
                    "endpoint": endpoint,
                    "status_code": response.status,
                    "success": success,
                    "response_time": time.time()
                }
        except Exception as e:
            return {
                "endpoint": endpoint,
                "status_code": 0,
                "success": False,
                "error": str(e),
                "response_time": time.time()
            }
    
    async def multi_ping(self) -> List[Dict]:
        """Ping multiple endpoints simultaneously"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.ping_endpoint(session, endpoint) for endpoint in self.endpoints]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [r for r in results if isinstance(r, dict)]
    
    def sync_ping_backup(self) -> bool:
        """Synchronous backup ping method"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=30)
            return response.status_code == 200
        except:
            return False
    
    def update_stats(self, results: List[Dict]):
        """Update ping statistics"""
        self.stats["total_pings"] += 1
        
        successful = any(r.get("success", False) for r in results)
        
        if successful:
            self.stats["successful_pings"] += 1
            self.stats["last_success"] = datetime.now()
        else:
            self.stats["failed_pings"] += 1
            self.stats["last_failure"] = datetime.now()
    
    def log_results(self, results: List[Dict]):
        """Log ping results"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for result in results:
            status = "✅" if result.get("success") else "❌"
            endpoint = result.get("endpoint", "unknown")
            status_code = result.get("status_code", 0)
            
            if result.get("success"):
                logger.info(f"{status} {endpoint} - HTTP {status_code}")
            else:
                error = result.get("error", f"HTTP {status_code}")
                logger.warning(f"{status} {endpoint} - {error}")
        
        # Log summary
        successful_count = sum(1 for r in results if r.get("success"))
        total_count = len(results)
        
        if successful_count > 0:
            logger.info(f"🎯 Keep-alive successful ({successful_count}/{total_count} endpoints)")
        else:
            logger.error(f"🚨 All endpoints failed ({successful_count}/{total_count})")
    
    def log_stats(self):
        """Log current statistics"""
        uptime = datetime.now() - self.stats["uptime_start"]
        success_rate = (self.stats["successful_pings"] / max(self.stats["total_pings"], 1)) * 100
        
        logger.info(f"📊 Stats - Uptime: {uptime}, Success Rate: {success_rate:.1f}%, Total Pings: {self.stats['total_pings']}")
    
    async def keep_alive_cycle(self):
        """Single keep-alive cycle"""
        logger.info("🔄 Starting keep-alive cycle...")
        
        # Try async multi-ping first
        try:
            results = await self.multi_ping()
            self.update_stats(results)
            self.log_results(results)
            
            # If all async pings failed, try sync backup
            if not any(r.get("success", False) for r in results):
                logger.info("🔄 Trying synchronous backup ping...")
                backup_success = self.sync_ping_backup()
                if backup_success:
                    logger.info("✅ Backup ping successful")
                    self.stats["successful_pings"] += 1
                    self.stats["last_success"] = datetime.now()
                else:
                    logger.error("❌ Backup ping also failed")
        
        except Exception as e:
            logger.error(f"🚨 Keep-alive cycle error: {e}")
            # Try sync backup as last resort
            if self.sync_ping_backup():
                logger.info("✅ Emergency backup ping successful")
    
    async def run(self):
        """Main keep-alive loop"""
        logger.info(f"🚀 Enhanced Keep-Alive Service Started")
        logger.info(f"🎯 Target: {self.base_url}")
        logger.info(f"⏰ Interval: {self.ping_interval} seconds ({self.ping_interval//60} minutes)")
        logger.info(f"🔗 Endpoints: {', '.join(self.endpoints)}")
        logger.info("=" * 60)
        
        while True:
            try:
                await self.keep_alive_cycle()
                
                # Log stats every 10 cycles
                if self.stats["total_pings"] % 10 == 0:
                    self.log_stats()
                
                # Wait for next cycle
                logger.info(f"⏳ Waiting {self.ping_interval//60} minutes until next ping...")
                await asyncio.sleep(self.ping_interval)
                
            except KeyboardInterrupt:
                logger.info("🛑 Keep-alive service stopped by user")
                break
            except Exception as e:
                logger.error(f"🚨 Unexpected error: {e}")
                logger.info("🔄 Continuing in 60 seconds...")
                await asyncio.sleep(60)

def main():
    """Entry point"""
    keep_alive = EnhancedKeepAlive()
    
    try:
        asyncio.run(keep_alive.run())
    except KeyboardInterrupt:
        logger.info("👋 Enhanced Keep-Alive Service stopped")

if __name__ == "__main__":
    main()