# TASK.md

## 완료된 작업
- [x] 백엔드 /predict-image 엔드포인트를 record_id 기반 구조로 개선 (이미지 파일 대신 record_id JSON)
- [x] 프론트엔드 analyzeImage 함수 recordId 기반으로 리팩토링
- [x] mockAnalyzeImage 함수 recordId 기반으로 수정 및 실제 API 응답 구조와 동일하게 맞춤
- [x] analyzeImage 테스트 코드 추가 (정상, 에러, 엣지케이스)
- [x] README에 분석 API 사용법 및 구조 개선 내용 추가
- [x] wound 기록 저장(/record) API 프론트 함수 및 mock 함수 추가
- [x] wound 기록 저장 문서화

## Discovered During Work
- [ ] mockAnalyzeImage 등 mock 함수의 공통화 및 테스트 자동화 필요성 검토
- [ ] API 구조 변경에 따른 프론트엔드 전역 타입/모델 정합성 점검

## TODO
- [ ] (예시) 신규 기능 추가 시, 테스트/문서화 동시 진행 원칙 유지
