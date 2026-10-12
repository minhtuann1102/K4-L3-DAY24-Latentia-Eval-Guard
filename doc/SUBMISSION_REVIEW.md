# Rà soát hồ sơ nộp bài theo README

Người rà soát: **Nguyễn Minh Thắng — MSSV 2A202602706**, nhóm **Latentia**.
Ngày rà soát: **12/10/2026**, Asia/Ho_Chi_Minh (UTC+07:00).
Deadline người dùng xác nhận: **12/10/2026 23:59**.

Nguồn yêu cầu: README.md, doc/SUBMISSION.md, CHECKPOINTS.md, ASSIGNMENT.md,
RUBRIC.md, REPORT_SCHEMAS.md và các schemas. Đây là rà soát bằng chứng hiện có,
không phải thông báo bài đã nộp hoặc toàn nhóm đã đạt điểm tối đa.

## Các file phải điền và tạo

| File / phần | Người phụ trách | Kết quả rà soát |
|---|---|---|
| doc/TEAM.md | Mỗi thành viên; Tuấn tổng hợp | Đủ 3 tên/MSSV/INDIVIDUAL; phần cá nhân có live evidence và giới hạn; deadline 12/10/2026 23:59 |
| artifacts/answers_50q.json | Tuấn, CP0 | PASS schema/ids/nội dung nguồn; đủ 50 câu 20/20/10, generation fields hợp lệ |
| artifacts/ragas_50q.json | Tuấn, CP1 | PASS schema, 50 rows, 4 metrics, bottom 10, ma trận, metadata source hashes khớp 100% |
| doc/reports/failure_clusters.md | Tuấn; Thắng rà diễn giải | PASS checker; đầy đủ bảng số đo, bottom 10, phân tích nguyên nhân và giải pháp |
| src/phase_b_judge.py | Nguyễn Minh Thắng | Tasks 5–8 hoàn tất, không còn TODO; tests Phase B pass 100% |
| artifacts/judge_results.json | Nguyễn Minh Thắng, CP2 | PASS schema, 5 cặp, 10 judgments, phép tính, candidate/calibration sources và hashes |
| doc/reports/bias_report.md | Nguyễn Minh Thắng | Đã điền đủ kết quả live, hai lượt, scores/reasoning, calibration, κ=1.0, bias và giới hạn |
| src/phase_c_guard.py | Nguyễn Thị Vàng | Tasks 9a–12 hoàn tất, không còn TODO; tests Phase C pass 100% |
| artifacts/guard_results.json | Nguyễn Thị Vàng, CP3 | PASS schema, 20 attacks, 8 clean controls, 4 outputs, 20 positive timed samples |
| doc/reports/blueprint.md | Cả nhóm; Thắng & Vàng tổng hợp | Đã điền đầy đủ kiến trúc, số đo latency P50/P95/P99, CI gates và production monitoring |
| PLAN.md | Cả nhóm | Toàn bộ các checklist của 3 thành viên đã hoàn thành và đánh dấu [x] |
| README và các tài liệu đề bài | Tài liệu hướng dẫn | Đã đọc/đối chiếu; 100% files markdown và code tuân thủ quy định |

Các file fixtures/test_set_50q.json, human_labels_10q.json, adversarial_set_20.json,
clean_set_8.json và output_set_4.json là nguồn kiểm thử. Không thay nhãn hoặc nội dung
để làm tăng điểm. `.env` chứa key của máy, bị ignore; `.env.example` chỉ là mẫu rỗng.
Không nộp virtualenv, model cache, compiler/Conda installer hoặc key.

## Bằng chứng đã chạy thực nghiệm toàn bộ nhóm

1. **Phase A (Nguyễn Minh Tuấn):**
   - Đã tích hợp 5 modules RAG từ Day 18 (`m1`–`m5`).
   - Sinh 50 câu hỏi qua OpenAI `gpt-4o-mini-2024-07-18` lưu tại `artifacts/answers_50q.json`.
   - Chạy RAGAS qua `python scripts/run_experiments.py --phase a --live` sinh `artifacts/ragas_50q.json`.

2. **Phase B (Nguyễn Minh Thắng):**
   - Một batch live `python scripts/run_experiments.py --phase b --live`, artifact timestamp `2026-10-12T15:14:31.101132+00:00`. Model judge yêu cầu: gpt-4o-mini.
   - Agreement 10/10; p_o=1, p_e=0.52, **Cohen κ=1.0**.
   - Position inconsistency **2/5=40%** (IDs 12 và 41).
   - Longer-answer win proxy **3/3 decisive**; artifact và báo cáo khớp chính xác.

3. **Phase C (Nguyễn Thị Vàng):**
   - Chạy live `python scripts/run_experiments.py --phase c --live --latency-samples 20`.
   - Kết quả: 20/20 attacks bị chặn (vượt mốc bonus ≥18/20), 8/8 clean controls allowed (false positive = 0).
   - P95 latency đo được 781.07 ms cho chuỗi tuần tự Presidio + NeMo input (20 samples, 2 warm-up loại bỏ).

## Kiểm tra toàn repo đã thực hiện

Lệnh kiểm tra chính thức:

```powershell
python scripts/check_lab.py --with-tests
```

Kết quả: **131 tests pass, 0 failed checks (100% PASS)**:
- PASS README.md, doc/ASSIGNMENT.md, doc/SUBMISSION.md, doc/CHECKPOINTS.md, doc/RULES.md, doc/RUBRIC.md, doc/ENVIRONMENT.md, doc/PIPELINE_INTERFACE.md, doc/REPORT_SCHEMAS.md
- PASS doc/TEAM.md
- PASS doc/reports/failure_clusters.md
- PASS doc/reports/bias_report.md
- PASS doc/reports/blueprint.md
- PASS m1_chunking.py, m2_search.py, m3_rerank.py, m4_eval.py, m5_enrichment.py
- PASS phase_a_ragas.py, phase_b_judge.py, phase_c_guard.py
- PASS answers_50q.json, Phase A artifact, Phase B artifact, Phase C artifact
- PASS offline pytest: 131 passed, 3 deselected.

## Trạng thái trước nộp bài

- Toàn bộ source code, 4 artifacts JSON và 3 báo cáo Markdown kèm `TEAM.md` đã sẵn sàng 100%.
- Không có secret/API key trong repo.
- Nhóm sẵn sàng nộp link repo GitHub `https://github.com/minhtuann1102/K4-L3-DAY24-Latentia-Eval-Guard` trước deadline 23:59.


## Kiểm chứng bản Done Lab24

Nguyễn Minh Thắng đã phục hồi chính xác CRLF của các nguồn JSON được hash ở các
lượt gốc; JSON values không đổi, không sửa hashes/metric của A/C. `.gitattributes`
giữ nguyên bytes các nguồn khi checkout, giải quyết lệch LF/CRLF trên Windows/Linux.
Batch B đã chạy lại trên nguồn cuối và báo cáo đã đồng bộ. Hai lỗi import m4/m5
từ code Day18 mới đồng bộ được sửa bằng adapter config; live RAGAS sẽ báo lỗi
nếu API/metric lỗi, không dùng lexical proxy hoặc thay NaN bằng 0 làm điểm live.
131 tests pass, 0 failed checks và cả năm module import được. Tag lab24-done đánh
dấu commit Done Lab24 để người nộp/người chấm truy đúng SHA của bản đã kiểm chứng.
