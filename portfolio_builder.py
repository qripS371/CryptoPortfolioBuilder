import requests

# Top 5 from real-time searches (Oct 2025): Weighted by promise (30-10%)
COINS = {
    'bitcoin': {'name': 'Bitcoin (BTC)', 'weight': 0.30, 'pred_2026': 150000},
    'ethereum': {'name': 'Ethereum (ETH)', 'weight': 0.25, 'pred_2026': 8000},
    'solana': {'name': 'Solana (SOL)', 'weight': 0.20, 'pred_2026': 400},
    'cardano': {'name': 'Cardano (ADA)', 'weight': 0.15, 'pred_2026': 3},
    'ripple': {'name': 'XRP (Ripple)', 'weight': 0.10, 'pred_2026': 5}
}

def get_price(coin_id):
    """Fetch current USD price from CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data[coin_id]['usd']
    except:
        pass
    return None

def build_portfolio(investment):
    """Build weighted portfolio."""
    total_current = 0
    total_future = 0
    portfolio = []
    
    for coin_id, info in COINS.items():
        price = get_price(coin_id)
        if price:
            allocation = investment * info['weight']
            shares = allocation / price
            future_value = shares * info['pred_2026']
            
            portfolio.append({
                'name': info['name'],
                'weight': f"{info['weight']*100:.0f}%",
                'allocation': round(allocation, 2),
                'current_price': round(price, 2),
                'shares': round(shares, 6),
                'pred_price': info['pred_2026'],
                'future_value': round(future_value, 2)
            })
            
            total_current += allocation
            total_future += future_value
    
    growth_pct = ((total_future - investment) / investment * 100) if investment > 0 else 0
    return portfolio, round(total_current, 2), round(total_future, 2), round(growth_pct, 2)

# Main
if __name__ == "__main__":
    print("🛡️ Weighted Long-Term Crypto Portfolio Builder (Oct 2025 Edition)\n")
    
    try:
        investment = float(input("Enter your investment amount (USD): $"))
    except ValueError:
        print("Invalid input—using $500 as default.")
        investment = 500
    
    portfolio, current_total, future_total, growth = build_portfolio(investment)
    
    print(f"\nYour Weighted Portfolio (Based on Future Promise):\n")
    print("| Crypto      | Weight | Alloc | Curr Price | Shares  | Pred Price | Future Val |")
    print("|-------------|--------|-------|------------|---------|------------|------------|")
    for item in portfolio:
        print(f"| {item['name']:<11} | {item['weight']:<6} | ${item['allocation']:<5} | ${item['current_price']:<10} | {item['shares']:<7} | ${item['pred_price']:,} | ${item['future_value']:<10} |")
    
    print(f"\n**Total Current Value: ${current_total}**")
    print(f"**Est. Value in 1 Year (2026): ${future_total}**")
    print(f"**Projected Growth: +{growth}%** (Hypothetical—volatility ahead!)")
    
    print("\n💡 Tip: Review quarterly. Use tools like Delta app for tracking. Diversification ≠ guarantee.")