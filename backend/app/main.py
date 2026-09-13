from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import ValuationLog

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Valuation & Equity Analytics API",
    version="1.0.0"
)

# Enable CORS for Frontend Communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DCFRequest(BaseModel):
    ticker: str = Field(..., example="AAPL")
    share_price: float = Field(..., gt=0, example=175.0)
    free_cash_flow: float = Field(..., gt=0, example=100000.0) # in thousands
    growth_rate: float = Field(..., ge=0, le=1, example=0.08)   # 8%
    discount_rate: float = Field(..., gt=0, le=1, example=0.10) # 10%
    shares_outstanding: float = Field(..., gt=0, example=1000.0)# in thousands

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "finance-backend"}

@app.post("/api/v1/valuation/dcf")
def calculate_dcf(data: DCFRequest, db: Session = Depends(get_db)):
    # 5-Year DCF Projection Model
    fcf = data.free_cash_flow
    pv_cash_flows = 0.0

    for year in range(1, 6):
        fcf *= (1 + data.growth_rate)
        pv_cash_flows += fcf / ((1 + data.discount_rate) ** year)

    # Terminal Value calculation using Gordon Growth (2% perpetual rate)
    terminal_value = (fcf * 1.02) / (data.discount_rate - 0.02)
    pv_terminal_value = terminal_value / ((1 + data.discount_rate) ** 5)

    enterprise_value = pv_cash_flows + pv_terminal_value
    intrinsic_value = enterprise_value / data.shares_outstanding

    if data.share_price < (intrinsic_value * 0.85):
        status = "UNDERVALUED"
    elif data.share_price > (intrinsic_value * 1.15):
        status = "OVERVALUED"
    else:
        status = "FAIRLY VALUED"

    # Save execution log to DB
    log_entry = ValuationLog(
        ticker=data.ticker.upper(),
        share_price=data.share_price,
        intrinsic_value=round(intrinsic_value, 2),
        valuation_status=status
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    return {
        "ticker": data.ticker.upper(),
        "share_price": data.share_price,
        "intrinsic_value": round(intrinsic_value, 2),
        "status": status,
        "implied_upside_percent": round(((intrinsic_value - data.share_price) / data.share_price) * 100, 2)
    }

@app.get("/api/v1/valuation/history")
def get_history(db: Session = Depends(get_db)):
    return db.query(ValuationLog).order_by(ValuationLog.created_at.desc()).limit(10).all()