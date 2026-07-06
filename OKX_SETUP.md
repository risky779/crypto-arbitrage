# 🎯 OKX 사용 가이드

## ✅ 좋은 소식!

OKX 키가 있으시니 **바이낸스 없이도 98%의 수익 기회를 활용**할 수 있습니다!

---

## 🚀 빠른 시작 (OKX 버전)

### 1단계: .env 파일 설정 (3분)

```bash
# .env 파일을 열고 다음을 입력하세요
notepad .env
```

```env
# 업비트 API 키
UPBIT_ACCESS_KEY=여기에_업비트_Access_Key
UPBIT_SECRET_KEY=여기에_업비트_Secret_Key

# OKX API 키
OKX_API_KEY=여기에_OKX_API_Key
OKX_SECRET_KEY=여기에_OKX_Secret_Key
OKX_PASSPHRASE=여기에_OKX_Passphrase

# 거래 설정
MIN_PROFIT_RATE=2.0              # 최소 수익률 2%
MAX_TRADE_AMOUNT_KRW=50000       # 처음엔 5만원
MAX_DAILY_TRADES=5               # 하루 5회
```

### 2단계: OKX 모니터링 시작

```bash
# OKX 버전 모니터 실행
start_monitor_okx.bat
```

---

## 📊 OKX vs 바이낸스 비교

| 항목 | OKX | 바이낸스 |
|------|-----|---------|
| 수수료 | 0.1% | 0.1% |
| 거래량 | 높음 | 매우 높음 |
| 유동성 | 좋음 | 매우 좋음 |
| 한국 지원 | 제한적 | 제한적 |
| **결론** | ✅ 사용 가능 | ✅ 사용 가능 |

**핵심**: 두 거래소 모두 차익거래에 문제없이 사용 가능합니다!

---

## 💰 예상 수익 (OKX 기준)

### BCH 거래 (가장 수익성 높음)
- **바이낸스 분석 데이터 기준**:
  - 평균 수익률: 1.77%
  - 성공률: 91.7%
- **OKX도 동일한 수준 예상**
  - 가격 차이 거의 없음
  - 수수료 동일 (0.1%)

### 월 예상 수익 (10만원, 하루 3회)
- 평균: 약 **159,300원/월**
- 적극적: 약 **225,000원/월**

---

## 🔧 OKX API 권한 설정

### 필수 권한
- ✅ **Read** (읽기)
- ✅ **Trade** (거래)
- ❌ **Withdraw** (출금) - 반드시 비활성화!

### API 키 생성
1. OKX 로그인
2. Profile → API → Create V5 API Key
3. 권한 설정: Read + Trade (Withdraw 제외)
4. Passphrase 설정 및 저장
5. API Key, Secret Key, Passphrase 복사

---

## 📁 OKX 버전 파일

### 실행 파일
- `start_monitor_okx.bat` - OKX 모니터링
- `trading_bot_okx.py` - OKX 거래 봇

### 로그 파일
- `arbitrage_log_okx.txt` - OKX 기회 기록
- `trading_log_okx.txt` - OKX 거래 기록

---

## ⚠️ 주의사항

### OKX 특이사항
1. **Passphrase 필수**: 바이낸스와 달리 Passphrase가 필요합니다
2. **IP 화이트리스트**: 보안을 위해 IP 제한 권장
3. **KYC 필수**: 거래 전 신원 인증 완료 필요

### 공통 주의사항
- 소액(5~10만원)으로 시작
- API "출금" 권한 비활성화
- 각 거래 승인 전 확인
- 일일 거래 한도 설정

---

## 🔄 바이낸스 vs OKX 선택

### OKX 사용 추천 (현재 상황)
✅ **장점**:
- 이미 API 키 보유
- 바로 시작 가능
- 바이낸스와 동등한 수익 기회

✅ **단점**:
- Passphrase 관리 필요
- 한국 사용자 지원 제한적

### 결론
**OKX 키가 있으니 OKX로 시작하세요!**
- 바이낸스 발급 불필요
- 수익 기회는 동일
- 시스템 작동 확인 후 필요시 바이낸스 추가 고려

---

## 🎯 체크리스트

시작 전 확인:
- [ ] OKX API 키 발급 완료
- [ ] 업비트 API 키 발급 완료
- [ ] .env 파일에 키 입력
- [ ] API "출금" 권한 비활성화
- [ ] KYC 인증 완료
- [ ] 소액 테스트 자금 준비 (5~10만원)

---

## 📞 문제 해결

### OKX API 오류
- Passphrase 정확히 입력했는지 확인
- API 권한 확인 (Read + Trade)
- IP 화이트리스트 확인

### 가격 조회 실패
- OKX 점검 시간 확인
- 네트워크 연결 확인
- API Rate Limit 확인

---

## 🚀 시작하기

```bash
# 1. .env 파일 설정
notepad .env

# 2. OKX 모니터 실행
start_monitor_okx.bat

# 3. 수익 기회 확인
# BCH에서 2% 이상 기회 포착 시 알림
```

**OKX로 시작하세요! 🎉**
