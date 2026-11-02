"""Seven-block chat report (docs/PRICE_ACTION_ENGINE.md section 8)."""
from __future__ import annotations

from engine.price_action.models import PriceActionReport, TradeDecision


def build_chat_report(report: PriceActionReport) -> str:
    """Format PriceActionReport into the mandatory 7-block chat layout."""
    ms = report.market_structure
    tp = report.trade_plan
    fc = report.fimathe_confluence

    decision_pt = {
        TradeDecision.BUY_SETUP: "COMPRA (setup)",
        TradeDecision.SELL_SETUP: "VENDA (setup)",
        TradeDecision.WAIT: "AGUARDAR",
    }.get(tp.decision, "AGUARDAR")

    seq = " / ".join(ms.sequence) if ms.sequence else "não identificável"
    swings_txt = ", ".join(
        f"{s.label.value}@{s.price}" for s in ms.swings[-6:]
    ) if ms.swings else "não identificável"

    lines = [
        "### 1. LEITURA DO MERCADO",
        f"- Ativo: {report.asset or 'não identificável na imagem'}",
        f"- Timeframe: {report.timeframe or 'não identificável na imagem'}",
        f"- Qualidade da imagem: {report.input_quality.value}",
        f"- Tendência (regime): {report.market_regime.value}",
        f"- Bias: {report.trend_bias.value}",
        f"- Timeframe superior: {report.higher_timeframe_status}",
        "",
        "### 2. ESTRUTURA",
        f"- Swings recentes: {swings_txt}",
        f"- Sequência: {seq}",
        f"- BOS: {ms.bos or '—'}",
        f"- CHoCH: {ms.choch or '—'}",
        f"- Status da estrutura: {ms.structure_status.value}",
        "",
        "### 3. LINHAS E REGIÕES",
        "- LTA/LTB: ver análise visual (módulo de trendlines quando disponível)",
        "- Canal PA: ver análise visual",
        "- Suportes/Resistências: ver análise visual / zonas Fimathe",
        f"- Rompimento: {report.breakout_status.value}",
        "",
        "### 4. PRICE ACTION",
        f"- Regime: {report.market_regime.value}",
        f"- Bias: {report.trend_bias.value}",
        f"- Confiança: {report.confidence_level}",
        f"- Motivos: {'; '.join(report.confidence_reasons) or '—'}",
        "",
        "### 5. LEITURA FIMATHE",
        f"- Variante: {fc.variant or '—'}",
        f"- Direção Fimathe: {fc.direction}",
        f"- Confluência: {fc.status.value}",
        f"- Notas: {'; '.join(fc.notes) or '—'}",
        "",
        "### 6. PLANO OPERACIONAL",
        f"- Decisão: **{decision_pt}**",
        f"- Tipo de entrada: {tp.entry_type or '—'}",
        f"- Entrada: {tp.entry if tp.entry is not None else 'não definida / aguardar'}",
        f"- Stop: {tp.stop_loss if tp.stop_loss is not None else 'não definido / aguardar'}",
        f"- Takes: {tp.take_profits or 'projeções Fimathe quando houver'}",
        f"- R:R: {tp.risk_reward if tp.risk_reward is not None else '—'}",
        f"- Invalidação: {tp.invalidation or '—'}",
        "",
        "### 7. CONCLUSÃO",
        report.summary or "Aguardando confirmação estrutural e/ou Fimathe.",
    ]
    if report.limitations:
        lines += ["", "**Limitações:**"] + [f"- {x}" for x in report.limitations]
    return chr(10).join(lines)
