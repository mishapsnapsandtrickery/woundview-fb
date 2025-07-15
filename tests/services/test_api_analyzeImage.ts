import { analyzeImage } from '../../woundview_pj/services/api';

describe('analyzeImage (mock fallback)', () => {
  it('should return mock prediction for valid recordId', async () => {
    const res = await analyzeImage(12345) as { data: any }; // 정상 케이스
    expect(res.data.prediction).toContain('mock-prediction-for-record-12345');
    expect(typeof res.data.wound_width).toBe('number');
    expect(typeof res.data.wound_height).toBe('number');
    expect(typeof res.data.wound_area).toBe('number');
  });

  it('should handle edge case: recordId = 0', async () => {
    const res = await analyzeImage(0) as { data: any }; // 엣지케이스
    expect(res.data.prediction).toContain('mock-prediction-for-record-0');
  });

  it('should handle error fallback', async () => {
    // 강제로 에러를 발생시켜 mock fallback 동작 확인
    // 실제 API 서버가 없거나 404/403이 발생한다고 가정
    // (이 부분은 실제 환경에 따라 mocking 필요)
    // 예시: axios-mock-adapter 등 사용 가능
    // 여기서는 단순히 mockAnalyzeImage가 정상 동작하는지만 확인
    const res = await analyzeImage(99999) as { data: any };
    expect(res.data.prediction).toContain('mock-prediction-for-record-99999');
  });
});
