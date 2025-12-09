    def run(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(self.cash)
        cerebro.broker.setcommission(commission=self.commission)

        data_feed = self.load_data()
        cerebro.adddata(data_feed)

        cerebro.addstrategy(SmaCross)

        # ➕ QUANT ANALYZERS
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', timeframe=bt.TimeFrame.Days)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

        print(f"\n💰 Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")

        results = cerebro.run()
        strat = results[0]

        print(f"💰 Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

        # Extract analyzer results
        sharpe = strat.analyzers.sharpe.get_analysis()
        drawdown = strat.analyzers.drawdown.get_analysis()
        trades = strat.analyzers.trades.get_analysis()
        returns = strat.analyzers.returns.get_analysis()

        total_trades = trades.total.total if trades.total else 0
        won = trades.won.total if trades.won else 0
        lost = trades.lost.total if trades.lost else 0
        winrate = (won / total_trades * 100) if total_trades else 0

        # --- Save metrics to JSON ---
        import json

        metrics = {
            "starting_value": self.cash,
            "final_value": cerebro.broker.getvalue(),
            "sharpe_ratio": sharpe.get("sharperatio", None),
            "max_drawdown_pct": drawdown.max.drawdown,
            "max_drawdown_length": drawdown.max.len,
            "total_return": returns.get("rtot", 0),
            "annualized_return": returns.get("rnorm", 0),
            "win_rate": winrate,
            "total_trades": total_trades,
            "winning_trades": won,
            "losing_trades": lost
        }

        with open("results/metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

        print("\n📁 Saved metrics to results/metrics.json")

        # --- Save chart as PNG ---
        figs = cerebro.plot(style="candlestick")
        fig = figs[0][0]
        fig.savefig("results/equity_curve.png")
        print("📊 Saved chart to results/equity_curve.png")
