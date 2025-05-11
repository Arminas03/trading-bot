import plotly.graph_objects as go
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import math


def get_sharpe_ratio(run, annualisation_const, round_to=4):
    return round(
        run[0].analyzers.return_analyzer.get_sharpe_ratio()
        * math.sqrt(annualisation_const)
        or 0,
        round_to,
    )


def get_sortino_ratio(run, annualisation_const, round_to=4):
    return round(
        run[0].analyzers.return_analyzer.get_sortino_ratio()
        * math.sqrt(annualisation_const)
        or 0,
        round_to,
    )


def get_net_profit(run, round_to=2):
    return round(run[0].analyzers.return_analyzer.get_final_return(), round_to)


def plot_strategy_equity(returns, dates):
    # open_returns = returns[:-1]
    # close_returns = returns[1:]
    #
    # figure = go.Figure(
    #     data=go.Candlestick(
    #         x=dates, open=open_returns, high=returns, low=returns, close=close_returns
    #     )
    # )
    figure = go.Figure(data=go.Scatter(x=dates, y=returns, mode="lines"))
    figure.update_layout(title="Equity", yaxis_title="$")

    return figure


def get_time_return_plot(time_returns, dates, starting_cash):
    for i in range(len(time_returns)):
        if i == 0:
            time_returns[i] = starting_cash
            continue
        time_returns[i] = time_returns[i - 1] * (1 + time_returns[i])

    return plot_strategy_equity(time_returns, dates)


def get_trade_distribution_plot(trade_pnl):
    pnl_figure = go.Figure(
        data=[
            go.Histogram(
                x=[trade_pnl[trade_ref]["pnl"] for trade_ref in trade_pnl.keys()]
            )
        ]
    )
    pnl_figure.update_layout(
        title="Trade P&L", xaxis_title="P&L", yaxis_title="Frequency"
    )

    return pnl_figure


def render_metrics(metrics):
    return [
        dbc.Col(
            html.P([html.Span(f"{metric}: ", className="fw-bold"), value]), width="auto"
        )
        for metric, value in metrics.items()
    ]


def run_dash(metrics, plots, dash_name):
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container(
        [
            html.H1(
                "Backtest Results" + f": {dash_name}" if dash_name else "",
                className="mt-3",
            ),
            dbc.Row(render_metrics(metrics), className="mb-4", justify="start"),
            dcc.Graph(figure=plots["time_return_plot"]),
            dcc.Graph(figure=plots["trade_distribution_plot"]),
        ],
        fluid=True,
    )

    app.run(debug=False)


def strategy_analysis(run, dash_name="", annualisation_const=1):
    metrics = {
        "Net profit": f"${get_net_profit(run)}",
        "Sharpe ratio": get_sharpe_ratio(run, annualisation_const),
        "Sortino ratio": get_sortino_ratio(run, annualisation_const),
    }

    plots = {
        "time_return_plot": get_time_return_plot(
            list(run[0].analyzers.return_analyzer.get_return_dict().values()),
            list(run[0].analyzers.return_analyzer.get_return_dict().keys()),
            run[0].analyzers.return_analyzer.get_starting_cash(),
        ),
        "trade_distribution_plot": get_trade_distribution_plot(
            run[0].analyzers.trade_pnl_analyzer.get_analysis()
        ),
    }

    run_dash(metrics, plots, dash_name)
